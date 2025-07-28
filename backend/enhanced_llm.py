"""
Enhanced LLM wrapper with proper authentication and error handling
"""
import asyncio
from typing import List, Dict, Any
from crewai.llms.base_llm import BaseLLM

from api_client import call_ai_api
from error_handler import handle_error
from config import get_config

class EnhancedLLM(BaseLLM):
    """Enhanced LLM wrapper with proper authentication and error handling"""

    def __init__(self, **kwargs):
        # Get the primary provider's model
        config = get_config()
        primary_provider = config.get_primary_provider()
        
        if not primary_provider:
            raise Exception("No AI provider configured. Please set up API keys.")
        
        super().__init__(model=primary_provider.model)
        self.config = config

    def call(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """Make API call with proper authentication and error handling"""
        try:
            # Check if we're already in an async context
            try:
                loop = asyncio.get_running_loop()
                # We're in an async context, create a task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, call_ai_api(messages))
                    result = future.result()
                return result
            except RuntimeError:
                # No running loop, safe to create one
                result = asyncio.run(call_ai_api(messages))
                return result
        
        except Exception as e:
            # Handle error and return user-friendly message
            error_response = handle_error(e, {
                "provider": self.config.get_primary_provider().name if self.config.get_primary_provider() else "unknown",
                "messages": len(messages),
                "model": self.model
            })
            
            # Return error message that will be visible to the user
            error_msg = error_response["error"]["message"]
            details = error_response["error"]["details"]
            suggested_action = error_response["error"]["suggested_action"]
            
            return f"Error generating content: {error_msg}\n\nDetails: {details}\n\nSuggested action: {suggested_action}"

    async def acall(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """Async version of call method"""
        try:
            return await call_ai_api(messages)
        except Exception as e:
            error_response = handle_error(e, {
                "provider": self.config.get_primary_provider().name if self.config.get_primary_provider() else "unknown",
                "messages": len(messages),
                "model": self.model
            })
            
            error_msg = error_response["error"]["message"]
            details = error_response["error"]["details"]
            suggested_action = error_response["error"]["suggested_action"]
            
            return f"Error generating content: {error_msg}\n\nDetails: {details}\n\nSuggested action: {suggested_action}"