# Fix Course Generation Authentication Issues

## Introduction

The course generation feature is currently failing with a 401 Unauthorized error when attempting to call the OpenRouter API. This prevents users from creating new courses and impacts the core functionality of the application. We need to implement proper API authentication, error handling, and fallback mechanisms to ensure reliable course generation.

## Requirements

### Requirement 1: API Authentication Configuration

**User Story:** As a system administrator, I want the backend to properly authenticate with the OpenRouter API so that course generation requests succeed.

#### Acceptance Criteria

1. WHEN the system starts up THEN it SHALL load the OpenRouter API key from environment variables
2. WHEN making API requests to OpenRouter THEN the system SHALL include proper authentication headers
3. WHEN the API key is missing or invalid THEN the system SHALL log an appropriate error message
4. WHEN the API key is configured correctly THEN course generation requests SHALL succeed

### Requirement 2: Error Handling and User Feedback

**User Story:** As a user, I want to receive clear error messages when course generation fails so that I understand what went wrong and what I can do about it.

#### Acceptance Criteria

1. WHEN an API authentication error occurs THEN the system SHALL return a user-friendly error message
2. WHEN the OpenRouter API is unavailable THEN the system SHALL provide a meaningful error response
3. WHEN rate limits are exceeded THEN the system SHALL inform the user about the limitation
4. WHEN any API error occurs THEN the error SHALL be logged for debugging purposes
5. WHEN displaying errors to users THEN sensitive information like API keys SHALL NOT be exposed

### Requirement 3: API Configuration Management

**User Story:** As a developer, I want a centralized way to manage API configurations so that authentication settings are consistent and secure.

#### Acceptance Criteria

1. WHEN the application starts THEN it SHALL validate all required API configurations
2. WHEN API configurations are missing THEN the system SHALL provide clear setup instructions
3. WHEN multiple AI providers are available THEN the system SHALL support fallback mechanisms
4. WHEN API configurations change THEN the system SHALL reload without requiring a restart

### Requirement 4: Robust Course Generation Flow

**User Story:** As a user, I want the course generation process to be reliable and handle various failure scenarios gracefully.

#### Acceptance Criteria

1. WHEN course generation starts THEN the system SHALL validate all prerequisites before making API calls
2. WHEN an API call fails THEN the system SHALL retry with exponential backoff
3. WHEN all retries are exhausted THEN the system SHALL provide options for manual retry
4. WHEN generation is interrupted THEN the system SHALL save partial progress
5. WHEN resuming generation THEN the system SHALL continue from the last successful step

### Requirement 5: Environment Configuration

**User Story:** As a developer, I want proper environment variable management so that API keys and configurations are handled securely.

#### Acceptance Criteria

1. WHEN deploying the application THEN all required environment variables SHALL be documented
2. WHEN environment variables are missing THEN the system SHALL provide clear error messages
3. WHEN running in development THEN the system SHALL support .env files for local configuration
4. WHEN running in production THEN the system SHALL use secure environment variable injection
5. WHEN API keys are rotated THEN the system SHALL detect and use new keys without restart

### Requirement 6: API Provider Flexibility

**User Story:** As a system administrator, I want the ability to switch between different AI providers so that the system is not dependent on a single service.

#### Acceptance Criteria

1. WHEN OpenRouter is unavailable THEN the system SHALL attempt to use alternative providers
2. WHEN configuring AI providers THEN the system SHALL support multiple provider configurations
3. WHEN a provider fails THEN the system SHALL automatically failover to the next available provider
4. WHEN all providers fail THEN the system SHALL queue requests for later processing
5. WHEN providers have different rate limits THEN the system SHALL respect each provider's limits

### Requirement 7: Monitoring and Logging

**User Story:** As a system administrator, I want comprehensive logging of API interactions so that I can monitor system health and troubleshoot issues.

#### Acceptance Criteria

1. WHEN making API requests THEN the system SHALL log request details (without sensitive data)
2. WHEN receiving API responses THEN the system SHALL log response status and timing
3. WHEN errors occur THEN the system SHALL log full error context for debugging
4. WHEN API usage approaches limits THEN the system SHALL log warnings
5. WHEN generating reports THEN the system SHALL provide API usage statistics