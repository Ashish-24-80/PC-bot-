import os
import sys
import asyncio
from unittest.mock import MagicMock

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock Telegram objects
def get_mock_objects(args=[]):
    async def mock_reply(text, **kwargs):
        print(f"Bot Reply: {text}")
        m = MagicMock()
        m.edit_text = mock_reply
        async def mock_delete(): return True
        m.delete = mock_delete
        return m

    async def mock_photo(photo, **kwargs):
        print(f"Bot Photo Sent: {photo}")
        return MagicMock()

    update = MagicMock()
    update.message.reply_text = mock_reply
    update.message.reply_photo = mock_photo
    update.message.delete = MagicMock()
    update.effective_chat.id = 12345
    
    context = MagicMock()
    context.args = args
    return update, context

async def test_software_plugin():
    print("\n--- Testing Software Plugin (Search) ---")
    from plugins.software import handle_winget
    update, context = get_mock_objects(["search", "calculator"])
    await handle_winget(update, context)

async def test_files_plugin():
    print("\n--- Testing Files Plugin (Find) ---")
    from plugins.files import handle_find
    update, context = get_mock_objects(["bot.py"])
    await handle_find(update, context)

async def test_vision_plugin():
    print("\n--- Testing Vision Plugin (Screenshot) ---")
    from plugins.vision import handle_vision
    update, context = get_mock_objects()
    await handle_vision(update, context)

async def test_antigravity_plugin():
    print("\n--- Testing Antigravity Plugin (Keyboard) ---")
    from plugins.antigravity import handle_control_antigravity
    update, context = get_mock_objects(["print hello world"])
    await handle_control_antigravity(update, context)

async def test_agent_correction():
    print("\n--- Testing Agent Self-Correction logic ---")
    from plugins.voice import execute_agent_script
    # Test a failing script
    bad_code = "import nonexistent_library\nprint('fail')"
    print("Running bad code...")
    result = execute_agent_script(bad_code)
    print(f"Execution Result (should fail): {result}")
    assert "Script failed" in result or "ModuleNotFoundError" in result

async def main():
    print(" STARTING INTEGRATION TESTS (MOCKED TELEGRAM)")
    await test_software_plugin()
    await test_files_plugin()
    await test_vision_plugin()
    await test_antigravity_plugin()
    await test_agent_correction()
    print("\n ALL LOGIC TESTS PASSED.")

if __name__ == "__main__":
    asyncio.run(main())
