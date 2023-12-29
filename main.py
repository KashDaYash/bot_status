# (C) @KashDaYash 

from os import getenv
from dotenv import load_dotenv
import asyncio 
import time
import datetime
import pytz
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait


load_dotenv()
# Api Strings From my.telegram.org

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Your Session Strings
SESSION = getenv("SESSION_STRING")

# Your Bots Username Without '@' With A Space 1 To Another
BOTS = [i.strip() for i in getenv("BOTS").split(' ')]

# Your Username Without '@'
BOT_OWNER = getenv("BOT_OWNER")

# Your Channel Username Without '@'
UPDATE_CHANNEL = getenv("UPDATE_CHANNEL")
LOGGER_CHAT = -1001989843749
# Message Id Of Your Channel Bot Status Message
STATUS_MESSAGE_ID = int(getenv("STATUS_MESSAGE_ID"))

# Time & Limits
TIME = int(getenv("TIME"))

# Restart My Bot
REBOTS = [i.strip() for i in getenv("BOTS").split(' ')]

app = Client(name="botstatus", session_string=SESSION, api_id=API_ID, api_hash=API_HASH)

async def check_bot_status(app, bot, BOT_OWNER, LOGGER_CHAT):
    print(f"💬 [INFO] Checking @{bot}")
    try:
        TEXT = ""
        x = await app.send_message(bot, '/start')
        await asyncio.create_task(asyncio.sleep(15))
        async for msg in app.get_chat_history(bot, limit=1):
            if x.id == msg.id:
                print(f"⚠️ [WARNING] @{bot} Is Down")
                TEXT = f"❌ - @{bot}\n"
                await app.send_message(LOGGER_CHAT, f"❌ - @{bot} IS DOWN !!")
            else:
                print(f"☑ [INFO] All Good With @{bot}")
                TEXT += f"✅ - @{bot}\n"
    except FloodWait as e:
        print(f"⚠️ [WARNING] FloodWait for {e.x} seconds. Retrying...")
        await asyncio.sleep(e.x)
        TEXT = await check_bot_status(app, bot, BOT_OWNER, LOGGER_CHAT)

    await app.read_chat_history(bot)
    return TEXT

async def check_restart_status(app, re, BOT_OWNER, LOGGER_CHAT):
    print(f"💬 [INFO] Checking @{re}")
    try:
        TEXT = ""
        x = await app.send_message(re, '/start')
        await asyncio.create_task(asyncio.sleep(15))
        async for msg in app.get_chat_history(re, limit=1):
            if x.id == msg.id:
                print(f"⛔ [WARNING] I Can't Restart @{re}")
                TEXT = f"❌ - @{re}\n"
                await app.send_message(LOGGER_CHAT, f"⛔ - I Can't Restart @{re} !!")
            else:
                print(f"✅ [INFO] Restarted @{re}")
                TEXT += f"✅ - @{re}\n"
                await app.send_message(LOGGER_CHAT, f"✅ - @{re} #RESTARTED !!")
    except FloodWait as e:
        print(f"⚠️ [WARNING] FloodWait for {e.x} seconds. Retrying...")
        await asyncio.sleep(e.x)
        TEXT = await check_restart_status(app, re, BOT_OWNER, LOGGER_CHAT)

    await app.read_chat_history(re)
    return TEXT 

async def main():
    async with app:
        while True:
            print("💬 [INFO] Starting To Check Uptime..")
            TEXT = f"<b>👾 @{UPDATE_CHANNEL} Our Bot's Status (Updating Every  {round(TIME // 60// 60)} Hours)</b>\n\n<b>📜 BOTS :</b>\n\n"

            tasks = [check_bot_status(app, bot, BOT_OWNER, LOGGER_CHAT) for bot in BOTS]
            bot_results = await asyncio.gather(*tasks)
            TEXT += ''.join(bot_results)

            #utc_now = datetime.datetime.now(pytz.timezone('UTC')).strftime("%I:%M %p %d/%m/%y")
            in_now = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%y %I:%M:%S %p")

            TEXT += f"\n⏱ <b>LAST UPDATE :</b>\n\n🇮🇳 India: {str(in_now)}"

            taskss = [check_restart_status(app, re, BOT_OWNER, LOGGER_CHAT) for re in REBOTS]
            restart_results = await asyncio.gather(*taskss)

            try:
                await app.edit_message_text(UPDATE_CHANNEL, STATUS_MESSAGE_ID, text=TEXT, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
                print(f"[INFO] Everything Done! Sleeping For {round(TIME / 60)} Hours...")
            except FloodWait as e:
                print(f"⚠️ [WARNING] FloodWait for {e.x} seconds. Retrying...")
                await asyncio.sleep(e.x)

            await asyncio.sleep(TIME)

if __name__ == "__main__":
    asyncio.run(main())