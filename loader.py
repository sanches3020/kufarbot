from aiogram import Bot, Dispatcher, Router
from config.token import TOKEN
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler


con = sqlite3.connect('my_database.db')
cursor = con.cursor()


dp = Dispatcher()
router = Router()
dp.include_router(router)
bot = Bot(TOKEN)
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')