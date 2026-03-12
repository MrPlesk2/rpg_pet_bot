import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
router = Router()

import handlers

dp.include_router(router)

pet_bot = Bot(TOKEN)
