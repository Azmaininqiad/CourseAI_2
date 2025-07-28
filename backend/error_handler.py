"""
Error handling system for CourseAI backend
"""
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ErrorType(Enum):
    """Types of errors that can occur"""
    AUTHENTICATION = "authentication"
    RATE_LIMIT = "rate_limit"
    NETWORK = "network"
    VALIDATION = "validation"
    CONFIGURATION = "configuration"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    QUOTA_EXCEEDED = "quota_exceeded"
    INTERNAL = "internal"
    UNKNOWN = "unknown"

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class APIError:
    """Structured API error information"""
    error_type: ErrorType
    status_code: int
    message: str
    provider: str
    timestamp: datetime
    details: Optional[str] = None
    retry_after: Optional[int] = None
    support_reference: Optional[str] = None

@dataclass
class UserError:
    """User-friendly error information"""
    code: str
    message: str
    details: Optional[str] = None
    suggested_action: Optional[str] = None
    retry_after: Optional[int] = None
    support_reference: Optional[str] = None

class ErrorHandler:
    """Centralized error handling and processing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """Set up structured logging"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def classify_error(self, error: Exception, status_code: int = None, provider: str = "unknown") -> ErrorType:
        """Classify an error based on its characteristics"""
        error_message = str(error).lower()
        
        # Authentication errors
        if status_code == 401 or "unauthorized" in error_message or "invalid api key" in error_message:
            return ErrorType.AUTHENTICATION
        
        if status_code == 403 or "forbidden" in error_message:
            return ErrorType.AUTHENTICATION
        
        # Rate limiting
        if status_code == 429 or "rate limit" in error_message or "too many requests" in error_message:
            return ErrorType.RATE_LIMIT
        
        # Network errors
        if status_code in [502, 503, 504] or "connection" in error_message or "timeout" in error_message:
            return ErrorType.NETWORK
        
        # Provider unavailable
        if status_code == 503 or "service unavailable" in error_message:
            return ErrorType.PROVIDER_UNAVAILABLE
        
        # Validation errors
        if status_code in [400, 422] or "validation" in error_message or "invalid request" in error_message:
            return ErrorType.VALIDATION
        
        # Quota exceeded
        if "quota" in error_message or "limit exceeded" in error_message:
            return ErrorType.QUOTA_EXCEEDED
        
        # Configuration errors
        if "configuration" in error_message or "missing" in error_message:
            return ErrorType.CONFIGURATION
        
        return ErrorType.UNKNOWN
    
    def create_api_error(self, error: Exception, status_code: int = None, provider: str = "unknown") -> APIError:
        """Create a structured API error from an exception"""
        error_type = self.classify_error(error, status_code, provider)
        
        # Extract retry-after header if available
        retry_after = None
        if hasattr(error, 'response') and hasattr(error.response, 'headers'):
            retry_after = error.response.headers.get('Retry-After')
            if retry_after:
                try:
                    retry_after = int(retry_after)
                except ValueError:
                    retry_after = None
        
        return APIError(
            error_type=error_type,
            status_code=status_code or 500,
            message=str(error),
            provider=provider,
            timestamp=datetime.now(),
            details=self._get_error_details(error),
            retry_after=retry_after,
            support_reference=self._generate_support_reference()
        )
    
    def _get_error_details(self, error: Exception) -> Optional[str]:
        """Extract detailed error information"""
        if hasattr(error, 'response'):
            try:
                response = error.response
                if hasattr(response, 'json'):
                    error_data = response.json()
                    return str(error_data.get('error', {}).get('message', ''))
                elif hasattr(response, 'text'):
                    return response.text[:500]  # Limit length
            except:
                pass
        return None
    
    def _generate_support_reference(self) -> str:
        """Generate a unique support reference ID"""
        import uuid
        return f"ERR-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    def process_api_error(self, api_error: APIError) -> UserError:
        """Convert API error to user-friendly error"""
        error_mappings = {
            ErrorType.AUTHENTICATION: {
                "code": "AUTH_FAILED",
                "message": "Authentication failed with AI provider",
                "details": "The API key appears to be invalid or expired",
                "suggested_action": "Please check your API key configuration and ensure it's valid"
            },
            ErrorType.RATE_LIMIT: {
                "code": "RATE_LIMITED",
                "message": "Request rate limit exceeded",
                "details": "Too many requests have been made in a short period",
                "suggested_action": f"Please wait {api_error.retry_after or 60} seconds before trying again"
            },
            ErrorType.NETWORK: {
                "code": "NETWORK_ERROR",
                "message": "Network connection error",
                "details": "Unable to connect to the AI service",
                "suggested_action": "Please check your internet connection and try again"
            },
            ErrorType.PROVIDER_UNAVAILABLE: {
                "code": "SERVICE_UNAVAILABLE",
                "message": "AI service is temporarily unavailable",
                "details": "The AI provider is experiencing technical difficulties",
                "suggested_action": "Please try again in a few minutes"
            },
            ErrorType.QUOTA_EXCEEDED: {
                "code": "QUOTA_EXCEEDED",
                "message": "API quota exceeded",
                "details": "Your API usage limit has been reached",
                "suggested_action": "Please check your API usage limits or upgrade your plan"
            },
            ErrorType.VALIDATION: {
                "code": "INVALID_REQUEST",
                "message": "Invalid request parameters",
                "details": "The request contains invalid or missing parameters",
                "suggested_action": "Please check your input and try again"
            },
            ErrorType.CONFIGURATION: {
                "code": "CONFIG_ERROR",
                "message": "Configuration error",
                "details": "The system is not properly configured",
                "suggested_action": "Please check the system configuration and API keys"
            },
            ErrorType.INTERNAL: {
                "code": "INTERNAL_ERROR",
                "message": "Internal system error",
                "details": "An unexpected error occurred in the system",
                "suggested_action": "Please try again or contact support if the problem persists"
            },
            ErrorType.UNKNOWN: {
                "code": "UNKNOWN_ERROR",
                "message": "An unexpected error occurred",
                "details": "The system encountered an unknown error",
                "suggested_action": "Please try again or contact support"
            }
        }
        
        mapping = error_mappings.get(api_error.error_type, error_mappings[ErrorType.UNKNOWN])
        
        return UserError(
            code=mapping["code"],
            message=mapping["message"],
            details=mapping["details"],
            suggested_action=mapping["suggested_action"],
            retry_after=api_error.retry_after,
            support_reference=api_error.support_reference
        )
    
    def should_retry(self, api_error: APIError) -> bool:
        """Determine if an error should trigger a retry"""
        retryable_errors = {
            ErrorType.NETWORK,
            ErrorType.PROVIDER_UNAVAILABLE,
            ErrorType.RATE_LIMIT
        }
        
        # Don't retry authentication or validation errors
        non_retryable_errors = {
            ErrorType.AUTHENTICATION,
            ErrorType.VALIDATION,
            ErrorType.CONFIGURATION
        }
        
        if api_error.error_type in non_retryable_errors:
            return False
        
        if api_error.error_type in retryable_errors:
            return True
        
        # For unknown errors, retry if status code suggests it might be temporary
        if api_error.error_type == ErrorType.UNKNOWN:
            return api_error.status_code >= 500
        
        return False
    
    def get_fallback_action(self, api_error: APIError) -> str:
        """Get suggested fallback action for an error"""
        fallback_actions = {
            ErrorType.AUTHENTICATION: "switch_provider",
            ErrorType.RATE_LIMIT: "wait_and_retry",
            ErrorType.NETWORK: "retry_with_backoff",
            ErrorType.PROVIDER_UNAVAILABLE: "switch_provider",
            ErrorType.QUOTA_EXCEEDED: "switch_provider",
            ErrorType.VALIDATION: "fix_request",
            ErrorType.CONFIGURATION: "fix_config",
            ErrorType.INTERNAL: "retry_later",
            ErrorType.UNKNOWN: "retry_with_backoff"
        }
        
        return fallback_actions.get(api_error.error_type, "contact_support")
    
    def log_error_context(self, error: Exception, context: Dict[str, Any]) -> None:
        """Log error with full context for debugging"""
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "traceback": traceback.format_exc()
        }
        
        self.logger.error(f"Error occurred: {error_info}")
    
    def create_error_response(self, api_error: APIError) -> Dict[str, Any]:
        """Create a standardized error response"""
        user_error = self.process_api_error(api_error)
        
        return {
            "success": False,
            "error": {
                "code": user_error.code,
                "message": user_error.message,
                "details": user_error.details,
                "suggested_action": user_error.suggested_action,
                "retry_after": user_error.retry_after,
                "support_reference": user_error.support_reference
            },
            "context": {
                "timestamp": api_error.timestamp.isoformat(),
                "provider": api_error.provider,
                "error_type": api_error.error_type.value
            }
        }
    
    def handle_course_generation_error(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle course generation specific errors"""
        # Log the error with context
        self.log_error_context(error, context)
        
        # Create API error
        status_code = getattr(error, 'status_code', None)
        provider = context.get('provider', 'unknown')
        api_error = self.create_api_error(error, status_code, provider)
        
        # Create user-friendly response
        response = self.create_error_response(api_error)
        
        # Add course generation specific context
        response["context"].update({
            "session_id": context.get("session_id"),
            "topic": context.get("topic"),
            "step": context.get("current_step")
        })
        
        return response

# Global error handler instance
error_handler = ErrorHandler()

# Convenience functions
def handle_error(error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Handle an error and return user-friendly response"""
    return error_handler.handle_course_generation_error(error, context or {})

def should_retry_error(error: Exception, status_code: int = None, provider: str = "unknown") -> bool:
    """Check if an error should trigger a retry"""
    api_error = error_handler.create_api_error(error, status_code, provider)
    return error_handler.should_retry(api_error)

def get_fallback_action(error: Exception, status_code: int = None, provider: str = "unknown") -> str:
    """Get fallback action for an error"""
    api_error = error_handler.create_api_error(error, status_code, provider)
    return error_handler.get_fallback_action(api_error)