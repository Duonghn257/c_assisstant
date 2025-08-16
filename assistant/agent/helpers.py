from enum import Enum

from agents.extensions.models.litellm_model import LitellmModel

from ..configs import get_settings


class Model(str, Enum):
    AZURE_OPENAI_41 = "azure/gpt-4.1"
    AZURE_OPENAI_4o = "azure/gpt-4o"
    AZURE_OPENAI_4oMINI = "azure/gpt-4o-mini"
    GEMINI_2_FLASH = "gemini/gemini-2.0-flash"
    GEMINI_25_FLASH = "gemini/gemini-2.5-flash"


def init_llm(model: Model) -> LitellmModel:
    settings = get_settings()
    if model == Model.AZURE_OPENAI_4o:
        return LitellmModel(
            model,
            base_url=settings.AZURE_OPENAI_4o_ENDPOINT,
            api_key=settings.AZURE_OPENAI_4o_API_KEY,
        )
    elif model == Model.AZURE_OPENAI_4oMINI:
        return LitellmModel(
            model,
            base_url=settings.AZURE_OPENAI_4oMINI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_4oMINI_API_KEY,
        )
    elif model == Model.AZURE_OPENAI_41:
        return LitellmModel(
            model,
            base_url=settings.AZURE_OPENAI_4oMINI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_4oMINI_API_KEY,
        )
    elif model == Model.GEMINI_2_FLASH:
        return LitellmModel(model, api_key=settings.GOOGLE_API_KEY)
    elif model == Model.GEMINI_25_FLASH:
        return LitellmModel(model, api_key=settings.GOOGLE_API_KEY)
    else:
        raise ValueError(f"Unsupported model: {model}")
