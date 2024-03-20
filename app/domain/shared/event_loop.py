import asyncio
from asyncio import AbstractEventLoop


def get_or_create_event_loop() -> AbstractEventLoop:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError as error:
        if "no running event loop" not in str(error):
            raise error from error
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop
