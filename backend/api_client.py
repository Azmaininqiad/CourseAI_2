"""
API client manager with authentication and retry logic
"""
import time
import requests
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from datetime import datetime, timedelta

from config import APIConfig, get_config
from error_handler import ErrorHandler, APIError, ErrorType

@dataclass
class RetryConfig:
    """Configuration for retry logic"""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0

class RateLimiter:
    """Simple rate limiter for API requests"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = []
    
    async def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = datetime.now()
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests if now - req_time < timedelta(minutes=1)]
        
        if len(self.requests) >= self.requests_per_minute:
            # Calculate wait time
            oldest_request = min(self.requests)
            wait_time = 60 - (now - oldest_request).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        self.requests.append(now)

class APIClientManager:
    """Manages API clients with authentication and retry logic"""
    
    def __init__(self):
        self.config = get_config()
        self.error_handler = ErrorHandler()
        self.retry_config = RetryConfig()
        self.rate_limiter = RateLimiter(self.config.rate_limit_per_minute)
        self.logger = logging.getLogger(__name__)
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.timeout = 30
    
    def create_openrouter_headers(self, api_key: str) -> Dict[str, str]:
        """Create headers for OpenRouter API"""
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://courseai.app",
            "X-Title": "CourseAI Course Creator"
        }
    
    def create_openai_headers(self, api_key: str) -> Dict[str, str]:
        """Create headers for OpenAI API"""
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_anthropic_headers(self, api_key: str) -> Dict[str, str]:
        """Create headers for Anthropic API"""
        return {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
    
    def create_gemini_headers(self, api_key: str) -> Dict[str, str]:
        """Create headers for Gemini API"""
        return {
            "Content-Type": "application/json"
        }
    
    def create_authenticated_request(self, provider_config: APIConfig, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Create an authenticated request for the specified provider"""
        
        if provider_config.name == "openrouter":
            headers = self.create_openrouter_headers(provider_config.api_key)
            payload = {
                "model": provider_config.model,
                "messages": messages,
                "max_tokens": 100000,
                "temperature": 0.8,
                "stream": False
            }
        
        elif provider_config.name == "openai":
            headers = self.create_openai_headers(provider_config.api_key)
            payload = {
                "model": provider_config.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": 0.8,
                "stream": False
            }
        
        elif provider_config.name == "anthropic":
            headers = self.create_anthropic_headers(provider_config.api_key)
            # Anthropic has a different message format
            system_message = ""
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append(msg)
            
            payload = {
                "model": provider_config.model,
                "max_tokens": 4000,
                "messages": user_messages,
                "system": system_message if system_message else "You are a helpful assistant."
            }
        
        elif provider_config.name == "gemini":
            headers = self.create_gemini_headers(provider_config.api_key)
            # Gemini has a different message format
            contents = []
            
            for msg in messages:
                if msg["role"] == "user":
                    contents.append({
                        "parts": [{"text": msg["content"]}]
                    })
                elif msg["role"] == "assistant":
                    contents.append({
                        "parts": [{"text": msg["content"]}],
                        "role": "model"
                    })
                # System messages are handled differently in Gemini
            
            payload = {
                "contents": contents,
                "generationConfig": {
                    "maxOutputTokens": 4000,
                    "temperature": 0.8
                }
            }
            
            # Gemini uses API key in URL
            provider_config.base_url = f"{provider_config.base_url}/{provider_config.model}:generateContent?key={provider_config.api_key}"
        
        else:
            raise ValueError(f"Unsupported provider: {provider_config.name}")
        
        return {
            "url": provider_config.base_url,
            "headers": headers,
            "json": payload,
            "timeout": provider_config.timeout
        }
    
    async def execute_with_retry(self, provider_config: APIConfig, messages: List[Dict[str, str]]) -> str:
        """Execute API request with retry logic"""
        
        last_error = None
        
        for attempt in range(self.retry_config.max_attempts):
            try:
                # Rate limiting
                await self.rate_limiter.wait_if_needed()
                
                # Create request
                request_data = self.create_authenticated_request(provider_config, messages)
                
                # Log request (without sensitive data)
                self.logger.info(f"Making API request to {provider_config.name} (attempt {attempt + 1}/{self.retry_config.max_attempts})")
                
                # Make request
                response = self.session.post(**request_data)
                
                # Check for success
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extract content based on provider
                    if provider_config.name in ["openrouter", "openai"]:
                        return result["choices"][0]["message"]["content"]
                    elif provider_config.name == "anthropic":
                        return result["content"][0]["text"]
                    elif provider_config.name == "gemini":
                        return result["candidates"][0]["content"]["parts"][0]["text"]
                
                # Handle error response
                error_data = None
                try:
                    error_data = response.json()
                except:
                    pass
                
                # Create API error
                error_message = f"HTTP {response.status_code}"
                if error_data:
                    error_message = error_data.get("error", {}).get("message", error_message)
                
                api_error = APIError(
                    error_type=self.error_handler.classify_error(Exception(error_message), response.status_code, provider_config.name),
                    status_code=response.status_code,
                    message=error_message,
                    provider=provider_config.name,
                    timestamp=datetime.now(),
                    details=str(error_data) if error_data else None,
                    retry_after=self._get_retry_after(response)
                )
                
                # Check if we should retry
                if not self.error_handler.should_retry(api_error):
                    raise Exception(f"Non-retryable error: {error_message}")
                
                last_error = api_error
                
                # Calculate delay for next attempt
                if attempt < self.retry_config.max_attempts - 1:
                    delay = min(
                        self.retry_config.base_delay * (self.retry_config.exponential_base ** attempt),
                        self.retry_config.max_delay
                    )
                    
                    # Use retry-after header if available
                    if api_error.retry_after:
                        delay = max(delay, api_error.retry_after)
                    
                    self.logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
            
            except requests.exceptions.RequestException as e:
                # Network error
                api_error = APIError(
                    error_type=ErrorType.NETWORK,
                    status_code=0,
                    message=str(e),
                    provider=provider_config.name,
                    timestamp=datetime.now()
                )
                
                last_error = api_error
                
                if attempt < self.retry_config.max_attempts - 1:
                    delay = min(
                        self.retry_config.base_delay * (self.retry_config.exponential_base ** attempt),
                        self.retry_config.max_delay
                    )
                    self.logger.info(f"Network error, retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
            
            except Exception as e:
                # Other errors
                api_error = APIError(
                    error_type=ErrorType.INTERNAL,
                    status_code=500,
                    message=str(e),
                    provider=provider_config.name,
                    timestamp=datetime.now()
                )
                
                last_error = api_error
                break
        
        # All retries exhausted
        if last_error:
            raise Exception(f"API request failed after {self.retry_config.max_attempts} attempts: {last_error.message}")
        else:
            raise Exception("API request failed for unknown reason")
    
    def _get_retry_after(self, response: requests.Response) -> Optional[int]:
        """Extract retry-after header from response"""
        retry_after = response.headers.get('Retry-After')
        if retry_after:
            try:
                return int(retry_after)
            except ValueError:
                pass
        return None
    
    async def call_with_fallback(self, messages: List[Dict[str, str]]) -> str:
        """Call API with automatic fallback to other providers"""
        
        # Get primary provider
        primary_provider = self.config.get_primary_provider()
        if not primary_provider:
            raise Exception("No AI provider configured. Please set up API keys.")
        
        # Try primary provider first
        try:
            self.logger.info(f"Attempting to use primary provider: {primary_provider.name}")
            return await self.execute_with_retry(primary_provider, messages)
        
        except Exception as e:
            self.logger.warning(f"Primary provider {primary_provider.name} failed: {e}")
            
            # Try fallback providers
            fallback_providers = self.config.get_fallback_providers()
            
            for provider in fallback_providers:
                try:
                    self.logger.info(f"Trying fallback provider: {provider.name}")
                    return await self.execute_with_retry(provider, messages)
                
                except Exception as fallback_error:
                    self.logger.warning(f"Fallback provider {provider.name} failed: {fallback_error}")
                    continue
            
            # All providers failed
            raise Exception(f"All AI providers failed. Last error: {e}")
    
    def test_provider_connection(self, provider_config: APIConfig) -> Dict[str, Any]:
        """Test connection to a specific provider"""
        test_messages = [
            {"role": "user", "content": "Hello, this is a test message. Please respond with 'Test successful'."}
        ]
        
        try:
            # Create a simple synchronous test
            request_data = self.create_authenticated_request(provider_config, test_messages)
            response = self.session.post(**request_data)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "provider": provider_config.name,
                    "message": "Connection successful",
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "success": False,
                    "provider": provider_config.name,
                    "error": f"HTTP {response.status_code}",
                    "message": response.text[:200]
                }
        
        except Exception as e:
            return {
                "success": False,
                "provider": provider_config.name,
                "error": str(e),
                "message": "Connection failed"
            }
    
    def test_all_providers(self) -> Dict[str, Any]:
        """Test connection to all configured providers"""
        results = {}
        
        for provider_name in ["openrouter", "openai", "anthropic", "gemini"]:
            provider_config = self.config.get_provider_config(provider_name)
            if provider_config and provider_config.api_key:
                results[provider_name] = self.test_provider_connection(provider_config)
            else:
                results[provider_name] = {
                    "success": False,
                    "provider": provider_name,
                    "error": "Not configured",
                    "message": "API key not provided"
                }
        
        return results

# Global API client instance
api_client = APIClientManager()

# Convenience functions
async def call_ai_api(messages: List[Dict[str, str]]) -> str:
    """Call AI API with automatic provider selection and fallback"""
    return await api_client.call_with_fallback(messages)

def test_api_connections() -> Dict[str, Any]:
    """Test all API connections"""
    return api_client.test_all_providers()