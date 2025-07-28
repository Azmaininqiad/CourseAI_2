# Fix Course Generation Authentication Issues - Design Document

## Overview

This design addresses the 401 Unauthorized error occurring during course generation by implementing proper API authentication, robust error handling, and a flexible configuration system. The solution focuses on creating a reliable course generation pipeline that can handle various failure scenarios and provide clear feedback to users.

## Architecture

### High-Level Architecture

```
Frontend (Next.js) 
    ↓ HTTP Request
Backend API (FastAPI)
    ↓ Authenticated Request
OpenRouter API / Alternative AI Providers
    ↓ Response
Backend Processing & Error Handling
    ↓ User-Friendly Response
Frontend Display & User Feedback
```

### Component Interaction Flow

1. **Frontend Request**: User initiates course creation
2. **Backend Validation**: Validate request and check API configuration
3. **API Authentication**: Add proper headers and authentication
4. **Provider Selection**: Choose primary or fallback AI provider
5. **Request Execution**: Make authenticated API call with retry logic
6. **Response Processing**: Handle success/error responses appropriately
7. **User Feedback**: Return meaningful messages to frontend

## Components and Interfaces

### 1. Configuration Manager

**Purpose**: Centralized management of API configurations and environment variables

**Interface**:
```python
class ConfigManager:
    def __init__(self):
        self.openrouter_api_key: str
        self.backup_providers: List[ProviderConfig]
        self.retry_settings: RetryConfig
    
    def validate_config(self) -> ValidationResult
    def get_provider_config(self, provider: str) -> ProviderConfig
    def reload_config(self) -> None
```

**Key Features**:
- Environment variable validation
- Multiple provider support
- Hot-reload capability
- Secure credential handling

### 2. API Client Manager

**Purpose**: Handle authentication and communication with AI providers

**Interface**:
```python
class APIClientManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.clients: Dict[str, APIClient]
    
    def create_authenticated_request(self, provider: str, payload: dict) -> Request
    def execute_with_retry(self, request: Request) -> Response
    def handle_rate_limiting(self, response: Response) -> None
```

**Key Features**:
- Automatic authentication header injection
- Retry logic with exponential backoff
- Rate limiting handling
- Provider failover support

### 3. Error Handler

**Purpose**: Process API errors and convert them to user-friendly messages

**Interface**:
```python
class ErrorHandler:
    def process_api_error(self, error: APIError) -> UserError
    def log_error_context(self, error: Exception, context: dict) -> None
    def should_retry(self, error: APIError) -> bool
    def get_fallback_action(self, error: APIError) -> FallbackAction
```

**Error Categories**:
- Authentication errors (401, 403)
- Rate limiting errors (429)
- Service unavailable errors (503, 504)
- Invalid request errors (400, 422)
- Network errors (timeout, connection)

### 4. Course Generation Service

**Purpose**: Orchestrate the course generation process with proper error handling

**Interface**:
```python
class CourseGenerationService:
    def __init__(self, api_manager: APIClientManager, error_handler: ErrorHandler):
        self.api_manager = api_manager
        self.error_handler = error_handler
    
    def generate_course(self, topic: str, user_id: str) -> GenerationResult
    def resume_generation(self, session_id: str) -> GenerationResult
    def save_progress(self, session_id: str, progress: GenerationProgress) -> None
```

**Key Features**:
- Progress tracking and persistence
- Graceful error recovery
- Resume capability
- WebSocket progress updates

## Data Models

### Configuration Models

```python
@dataclass
class ProviderConfig:
    name: str
    api_key: str
    base_url: str
    model: str
    rate_limit: int
    timeout: int

@dataclass
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
```

### Error Models

```python
@dataclass
class UserError:
    code: str
    message: str
    details: Optional[str]
    suggested_action: Optional[str]
    retry_after: Optional[int]

@dataclass
class APIError:
    status_code: int
    error_type: str
    message: str
    provider: str
    timestamp: datetime
```

### Generation Models

```python
@dataclass
class GenerationProgress:
    session_id: str
    user_id: str
    topic: str
    status: GenerationStatus
    progress_percentage: int
    current_step: str
    completed_modules: List[str]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime

enum GenerationStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
```

## Error Handling Strategy

### Error Classification

1. **Recoverable Errors**: Temporary issues that can be resolved with retry
   - Network timeouts
   - Rate limiting (429)
   - Temporary service unavailability (503)

2. **Configuration Errors**: Issues with setup that require admin intervention
   - Missing API keys
   - Invalid authentication credentials
   - Malformed configuration

3. **User Errors**: Issues with user input or permissions
   - Invalid topic format
   - Insufficient permissions
   - Quota exceeded

4. **System Errors**: Internal application issues
   - Database connection failures
   - File system errors
   - Memory/resource exhaustion

### Error Response Format

```python
{
    "success": false,
    "error": {
        "code": "AUTH_FAILED",
        "message": "Unable to authenticate with AI provider",
        "details": "The API key appears to be invalid or expired",
        "suggested_action": "Please check your OpenRouter API key configuration",
        "retry_after": null,
        "support_reference": "ERR-2024-001"
    },
    "context": {
        "session_id": "sess_123",
        "timestamp": "2024-01-15T10:30:00Z",
        "provider": "openrouter"
    }
}
```

## Testing Strategy

### Unit Tests
- Configuration validation logic
- Error handling and classification
- Retry mechanism behavior
- Authentication header generation

### Integration Tests
- API client authentication flow
- Provider failover scenarios
- Error propagation through layers
- Progress persistence and recovery

### End-to-End Tests
- Complete course generation flow
- Error scenarios with user feedback
- WebSocket progress updates
- Resume functionality

## Security Considerations

### API Key Management
- Store API keys in environment variables only
- Never log or expose API keys in responses
- Implement key rotation support
- Use secure key storage in production

### Request Security
- Validate all user inputs
- Implement request rate limiting
- Add request signing for sensitive operations
- Monitor for suspicious activity patterns

### Error Information Disclosure
- Sanitize error messages before sending to frontend
- Log detailed errors server-side only
- Implement error code mapping for user messages
- Avoid exposing internal system details

## Performance Considerations

### Caching Strategy
- Cache provider configurations
- Implement response caching for similar requests
- Cache authentication tokens when applicable
- Use connection pooling for HTTP clients

### Resource Management
- Implement request queuing for high load
- Set appropriate timeouts for all operations
- Monitor memory usage during generation
- Implement graceful degradation under load

### Monitoring and Metrics
- Track API response times
- Monitor error rates by provider
- Measure generation success rates
- Alert on configuration issues

## Deployment Considerations

### Environment Variables
```bash
# Required
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Optional fallback providers
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Configuration
MAX_RETRY_ATTEMPTS=3
REQUEST_TIMEOUT=30
RATE_LIMIT_PER_MINUTE=60
```

### Health Checks
- API connectivity validation
- Configuration completeness check
- Provider availability monitoring
- Database connection verification

### Logging Configuration
- Structured logging with JSON format
- Separate log levels for different components
- Error aggregation and alerting
- Performance metrics collection

This design provides a robust foundation for fixing the authentication issues while building a scalable and maintainable course generation system.