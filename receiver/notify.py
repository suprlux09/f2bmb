import asyncio
import os
import re
from dotenv import load_dotenv
from datetime import datetime
from telegram import Bot
from models import *

# Load environment variables
load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
userid = os.getenv("TELEGRAM_USER_ID")

if not token or not userid:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_USER_ID in the environment variables.")

async def main():
    print(datetime.now())
    bot = Bot(token=token)

    # get every file in the directory
    for hostname in os.listdir("./logfiles"):
        # 등록되지 않은 노드면 패스
        try:
            node = Node.get(Node.node_name == hostname)
        except Node.DoesNotExist:
            continue

        for line in open("./logfiles/" + hostname):
            time = re.findall(r"^\d+\-\d+\-\d+\s\d+\:\d+\:\d+", line)[0]
            filter = re.findall(r"\[.*\]", line)[0][1:-1]
            ip_addr = re.findall(r"\d+\.\d+\.\d+\.\d+", line)[0]
            action = re.findall(r"(Found|Ban)$", line)[0]

            # db 작업
            # 등록되지 않은 규칙이면 등록
            try:
                rule = Rule.get(Rule.filter == filter, Rule.node_name == node)
            except Rule.DoesNotExist:
                rule = Rule.create(filter=filter, node_name=node, notify_found=True, notify_ban=True)
        
            # 로그, IP 저장
            try:
                ip = DetectedIP.get(DetectedIP.ip_addr == ip_addr)
            except DetectedIP.DoesNotExist:
                ip = DetectedIP.create(ip_addr=ip_addr)
 
            Log.create(detected_at=datetime.strptime(time, "%Y-%m-%d %H:%M:%S"), 
                       filter=filter, node_name=node, ip_addr=ip, action=action)
            
            # send message to telegram
            # 규칙에 따라 메시지 전송
            if (action == "Found" and rule.notify_found) or (action == "Ban" and rule.notify_ban):
                await bot.send_message(chat_id=userid, text=f"Node: {hostname}\nTime: {time}\nFilter: {filter}\nIP: {ip_addr}\n Action: {action}")
        
if __name__ == '__main__':
    asyncio.run(main())
