import os
from functools import lru_cache

from agents import set_tracing_disabled
from pydantic_settings import BaseSettings, SettingsConfigDict


# Disable tracing
# set_tracing_disabled(disabled=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env")),
        extra="ignore",
    )

    # agent config
    AGENT_CONFIG_FILE: str = "assistant/configs/config_files/agent_configs.yml"
    """Path to the YAML file containing agent configuration settings."""

    # llm config
    AZURE_OPENAI_4o_ENDPOINT: str
    """Endpoint URL for the Azure OpenAI 4o service."""

    AZURE_OPENAI_4o_API_KEY: str
    """API key for authenticating with the Azure OpenAI 4o service."""

    AZURE_OPENAI_4oMINI_ENDPOINT: str
    """Endpoint URL for the Azure OpenAI 4oMini service."""

    AZURE_OPENAI_4oMINI_API_KEY: str
    """API key for authenticating with the Azure OpenAI 4oMini service."""

    AZURE_OPENAI_41_ENDPOINT: str
    """Endpoint URL for the Azure OpenAI 4.1 service."""

    AZURE_OPENAI_41_API_KEY: str
    """API key for authenticating with the Azure OpenAI 4.1 service."""

    GOOGLE_API_KEY: str
    """API key for authenticating with the Google API."""

    # AZURE_OPENAI_EMBEDDING_ENDPOINT: str
    # """Endpoint URL for the Azure OpenAI Embedding service."""

    # AZURE_OPENAI_EMBEDDING_API_KEY: str
    # """API key for authenticating with the Azure OpenAI Embedding service."""


@lru_cache
def get_settings() -> Settings:
    """
    Retrieve the application settings, utilizing caching to improve performance.

    This function returns an instance of the Settings class, which contains
    configuration values for the application. The use of lru_cache ensures
    that the settings are only loaded once and cached for subsequent calls,
    reducing the overhead of repeatedly loading the settings.

    Returns:
        Settings: An instance of the Settings class with the application's configuration.
    """
    return Settings()


if __name__ == "__main__":
    print(get_settings())
