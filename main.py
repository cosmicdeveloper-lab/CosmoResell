from bot import start_bot
import asyncio
from app import start_app
from utils import setup_logger

setup_logger()


async def main():
    await asyncio.gather(start_bot(), start_app())


if __name__ == '__main__':
    asyncio.run(main())
