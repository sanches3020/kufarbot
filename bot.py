import logging
from loader import *                
import asyncio


import handlers.users.start
import handlers.users.add
import handlers.users.delete

from script.update_task import recreate_tasks

async def main():
    scheduler.start()  
    recreate_tasks()
    await dp.start_polling(bot, allowed_updates= dp.resolve_used_update_types()) 

if __name__ == '__main__':  
    logging.basicConfig(level=logging.DEBUG)
asyncio.run(main())

