"""Entry point for running the bot as a module."""

from .main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

