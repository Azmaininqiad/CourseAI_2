"""
Configuration management for CourseAI backend
"""
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class APIConfig:
    """Configuration for API providers"""
    name: str
    api_key: str
    base_url: str
    model: str
    timeout: int = 30
    max_retries: int = 3

@dataclass
class ValidationResult:
    """Result of configuration validation"""
    is_valid: bool
    errors: list
    warnings: list

class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self):
        self.load_environment()
        self._validate_config()
    
    def load_environment(self):
        """Load configuration from environment variables"""
        # Load .env file if it exists (for development)
        env_file = Path('.env')
        if env_file.exists():
            self._load_env_file(env_file)
        
        # OpenRouter configuration (primary)
        self.openrouter_config = APIConfig(
            name="openrouter",
            api_key=os.getenv("OPENROUTER_API_KEY", ""),
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions"),
            model=os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-r1-0528:free"),
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
            max_retries=int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
        )
        
        # Fallback providers
        self.openai_config = APIConfig(
            name="openai",
            api_key=os.getenv("OPENAI_API_KEY", ""),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions"),
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
            max_retries=int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
        )
        
        self.anthropic_config = APIConfig(
            name="anthropic",
            api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1/messages"),
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
            max_retries=int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
        )
        
        self.gemini_config = APIConfig(
            name="gemini",
            api_key=os.getenv("GEMINI_API_KEY", ""),
            base_url=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/models"),
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
            max_retries=int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
        )
        
        # Google API configuration
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.search_engine_id = os.getenv("SEARCH_ENGINE_ID", "")
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY", "")
        
        # Rate limiting configuration
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        
        # Logging configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.enable_debug_logging = os.getenv("DEBUG_LOGGING", "false").lower() == "true"
    
    def _load_env_file(self, env_file: Path):
        """Load environment variables from .env file"""
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Only set if not already in environment
                        if key not in os.environ:
                            os.environ[key] = value.strip('"\'')
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")
    
    def _validate_config(self) -> ValidationResult:
        """Validate the current configuration"""
        errors = []
        warnings = []
        
        # Check if at least one AI provider is configured
        providers_configured = []
        
        if self.openrouter_config.api_key:
            providers_configured.append("OpenRouter")
        else:
            warnings.append("OpenRouter API key not configured")
        
        if self.openai_config.api_key:
            providers_configured.append("OpenAI")
        
        if self.anthropic_config.api_key:
            providers_configured.append("Anthropic")
        
        if self.gemini_config.api_key:
            providers_configured.append("Gemini")
        
        if not providers_configured:
            errors.append("No AI provider API keys configured. Please set at least one of: OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY")
        
        # Check Google API configuration
        if not self.google_api_key:
            warnings.append("Google API key not configured - image search will be disabled")
        
        if not self.search_engine_id:
            warnings.append("Google Search Engine ID not configured - image search will be disabled")
        
        if not self.youtube_api_key:
            warnings.append("YouTube API key not configured - video search will be disabled")
        
        # Validate API key formats
        if self.openrouter_config.api_key and not self.openrouter_config.api_key.startswith(('sk-or-', 'sk-')):
            warnings.append("OpenRouter API key format may be incorrect")
        
        if self.openai_config.api_key and not self.openai_config.api_key.startswith('sk-'):
            warnings.append("OpenAI API key format may be incorrect")
        
        self.validation_result = ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
        
        return self.validation_result
    
    def get_primary_provider(self) -> Optional[APIConfig]:
        """Get the primary AI provider configuration"""
        if self.openrouter_config.api_key:
            return self.openrouter_config
        elif self.gemini_config.api_key:
            return self.gemini_config
        elif self.openai_config.api_key:
            return self.openai_config
        elif self.anthropic_config.api_key:
            return self.anthropic_config
        return None
    
    def get_fallback_providers(self) -> list[APIConfig]:
        """Get list of fallback providers"""
        providers = []
        primary = self.get_primary_provider()
        
        for config in [self.openrouter_config, self.openai_config, self.anthropic_config, self.gemini_config]:
            if config.api_key and config != primary:
                providers.append(config)
        
        return providers
    
    def get_provider_config(self, provider_name: str) -> Optional[APIConfig]:
        """Get configuration for a specific provider"""
        provider_map = {
            "openrouter": self.openrouter_config,
            "openai": self.openai_config,
            "anthropic": self.anthropic_config,
            "gemini": self.gemini_config
        }
        return provider_map.get(provider_name.lower())
    
    def is_media_search_enabled(self) -> bool:
        """Check if media search is properly configured"""
        return bool(self.google_api_key and self.search_engine_id)
    
    def is_youtube_search_enabled(self) -> bool:
        """Check if YouTube search is properly configured"""
        return bool(self.youtube_api_key)
    
    def get_setup_instructions(self) -> str:
        """Get setup instructions for missing configuration"""
        instructions = []
        
        if not self.validation_result.is_valid:
            instructions.append("🔧 Configuration Setup Required:")
            instructions.append("")
            
            for error in self.validation_result.errors:
                instructions.append(f"❌ {error}")
            
            instructions.append("")
            instructions.append("📝 Setup Instructions:")
            instructions.append("")
            
            if not any(config.api_key for config in [self.openrouter_config, self.openai_config, self.anthropic_config, self.gemini_config]):
                instructions.extend([
                    "1. Get an API key from one of these providers:",
                    "   • OpenRouter: https://openrouter.ai/keys",
                    "   • OpenAI: https://platform.openai.com/api-keys",
                    "   • Anthropic: https://console.anthropic.com/",
                    "   • Google Gemini: https://makersuite.google.com/app/apikey",
                    "",
                    "2. Set the environment variable:",
                    "   export OPENROUTER_API_KEY='your-api-key-here'",
                    "   # OR",
                    "   export OPENAI_API_KEY='your-api-key-here'",
                    "",
                    "3. Restart the application",
                    ""
                ])
            
            if self.validation_result.warnings:
                instructions.append("⚠️ Optional Configuration:")
                for warning in self.validation_result.warnings:
                    instructions.append(f"   • {warning}")
        
        return "\n".join(instructions)
    
    def print_status(self):
        """Print current configuration status"""
        print("🔧 Configuration Status:")
        print("=" * 50)
        
        # AI Providers
        print("🤖 AI Providers:")
        providers = [
            ("OpenRouter", self.openrouter_config.api_key, self.openrouter_config.model),
            ("OpenAI", self.openai_config.api_key, self.openai_config.model),
            ("Anthropic", self.anthropic_config.api_key, self.anthropic_config.model),
            ("Gemini", self.gemini_config.api_key, self.gemini_config.model)
        ]
        
        for name, api_key, model in providers:
            status = "✅ Configured" if api_key else "❌ Not configured"
            print(f"  {name}: {status}")
            if api_key:
                print(f"    Model: {model}")
        
        # Media APIs
        print("\n🎬 Media APIs:")
        print(f"  Google Images: {'✅ Configured' if self.google_api_key else '❌ Not configured'}")
        print(f"  YouTube: {'✅ Configured' if self.youtube_api_key else '❌ Not configured'}")
        
        # Validation results
        if self.validation_result.errors:
            print(f"\n❌ Errors ({len(self.validation_result.errors)}):")
            for error in self.validation_result.errors:
                print(f"  • {error}")
        
        if self.validation_result.warnings:
            print(f"\n⚠️ Warnings ({len(self.validation_result.warnings)}):")
            for warning in self.validation_result.warnings:
                print(f"  • {warning}")
        
        if self.validation_result.is_valid:
            print("\n✅ Configuration is valid!")
        else:
            print("\n❌ Configuration has errors that need to be fixed")
            print("\nSetup instructions:")
            print(self.get_setup_instructions())

# Global configuration instance
config = ConfigManager()

# Convenience functions
def get_config() -> ConfigManager:
    """Get the global configuration instance"""
    return config

def is_configured() -> bool:
    """Check if the system is properly configured"""
    return config.validation_result.is_valid

def get_primary_provider() -> Optional[APIConfig]:
    """Get the primary AI provider configuration"""
    return config.get_primary_provider()

def get_setup_instructions() -> str:
    """Get setup instructions for missing configuration"""
    return config.get_setup_instructions()