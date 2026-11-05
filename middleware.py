from config import ADMIN_ID

def admin_only(func):
    """
    Decorator to ensure that only the admin can execute the handler.
    Silently drops requests from unauthorized users.
    """
    async def wrapper(update, context):
        if not update or not update.effective_user or update.effective_user.id != ADMIN_ID:
            return  # silent drop
        return await func(update, context)
    return wrapper
