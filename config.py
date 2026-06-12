API_KEY = "OPENROUTER_TOKEN"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
PRESET = "@preset/byok-model"
MODEL_NAME = "GEMINI_FLASH_3"



MODEL_SLUGS = {
    "GLM_5": "z-ai/glm-5",
    "KIMI_K2": "moonshotai/kimi-k2-thinking",
    "MINIMAX_M2": "minimax/minimax-m2",
    "GPT_120B": "openai/gpt-oss-120b",
    "GPT_20B": "openai/gpt-oss-20b",
    "GEMINI_FLASH_3.5": "google/gemini-3.5-flash",
    "GEMINI_FLASH_3": "google/gemini-3-flash-preview",
    "GEMINI_LITE_3.1": "google/gemini-3.1-flash-lite",
    "GEMINI_PRO_3.1": "google/gemini-3.1-pro-preview",
    "GEMINI_PRO_2.5": "google/gemini-2.5-pro",
    "QWEN_CODER": "qwen/qwen3-coder",
}
MODEL = MODEL_SLUGS[MODEL_NAME]