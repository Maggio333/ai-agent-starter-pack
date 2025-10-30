"""
Pytest global configuration.
- Ensures project root on PYTHONPATH
- Runs async test functions without requiring external plugins (fallback)
"""
import os
import sys
import asyncio
import inspect
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def pytest_runtest_call(item: pytest.Item) -> None:
    """Run async test functions via asyncio if no plugin is present.
    This allows `async def` tests to work without pytest-asyncio.
    """
    test_fn = getattr(item, "obj", None)
    if test_fn and inspect.iscoroutinefunction(test_fn):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Filter only args that the test function accepts
            sig = inspect.signature(test_fn)
            accepted = {k: v for k, v in item.funcargs.items() if k in sig.parameters}
            loop.run_until_complete(test_fn(**accepted))
        finally:
            loop.close()
        # Prevent default execution (already run)
        return


