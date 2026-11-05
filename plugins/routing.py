# Global state for media routing

MEDIA_ROUTE = "gemma4" # Default: gemma4. Can be "whisper", "qwen", or a directory path

def get_media_route():
    global MEDIA_ROUTE
    return MEDIA_ROUTE

def set_media_route(route: str):
    global MEDIA_ROUTE
    MEDIA_ROUTE = route
