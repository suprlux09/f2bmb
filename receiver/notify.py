import asyncio
import os
import re
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
userid = os.getenv("TELEGRAM_USER_ID")

# Ensure the token and user ID are available
if not token or not userid:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_USER_ID in the environment variables.")

async def main():
    bot = Bot(token=token)

    # get every file in the directory
    for hostname in os.listdir("./logfiles"):
        for line in open("./logfiles/" + hostname):
            time = re.findall(r"^\d+\-\d+\-\d+\s\d+\:\d+\:\d+", line)[0]
            filter = re.findall(r"\[.*\]", line)[0][1:-1]
            ip_addr = re.findall(r"\d+\.\d+\.\d+\.\d+$", line)[0]

            # send message to telegram
            await bot.send_message(chat_id=userid, text=f"Time: {time}\nFilter: {filter}\nIP: {ip_addr}")
        
if __name__ == '__main__':
    asyncio.run(main())
