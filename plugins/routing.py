# Global state for media routing
# Note: Gemma was removed due to storage constraints.
# Active local models in C:\llama.cpp\models:
# - MiniCPM5-2B-F16.gguf (Multimodal vision + small text, run-AI -small.bat)
# - qwen2.5-coder-7b-instruct-q4_k_m.gguf (Coding & reasoning, run-AI.bat)

MEDIA_ROUTE = "minicpm" # Default: minicpm. Can be "whisper", "qwen", "gemma4" (legacy alias), or a directory path

def get_media_route():
    global MEDIA_ROUTE
    return MEDIA_ROUTE

def set_media_route(route: str):
    global MEDIA_ROUTE
    MEDIA_ROUTE = route
