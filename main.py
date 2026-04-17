import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant

# --- RENDER KEEP ALIVE CODE ---
server = Flask('')
@server.route('/')
def home(): return "Bot is Alive"
def run(): server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- CONFIGURATION ---
API_ID = 32244889 
API_HASH = "cb2f194931d477417c78f43c80c3deb2"
BOT_TOKEN = "8554903983:AAHFNX0a4v4KLP7uymHydjMRHUVRL3hvPJ8"
CHANNEL_ID = -1003245026048 
CHANNEL_LINK = "https://t.me/ai_smart_tech"

# --- FILE IDS ---
FILES = {
    "ray": "BQACAgEAAxkBAAMXaeEtBTpV96Q1KcpYNedjQo1dz28AAsUFAAJHYBFHjo2XjLgSmFUeBA",
    "rare": "BQACAgEAAxkBAAMbaeEtZTU6_6chae0_3qH86v9y6gAC_wUAAkdgEUfG6a_Wp4Yj1R4E",
    "stark": "BQACAgEAAxkBAAMZaeEtCqkloGUKCt2ePeEsDSDjDSAAsYFAAJHYBFHAcK9W25KamweBA",
    "delta": "BQACAgEAAxkBAAMVaeEr8j3BkyFfgBavgr6_Hg4MWVkAAkIGAAloFQlHkYCOJSMNyeUeBA"
}

app = Client("BypassBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- HELPERS ---
async def is_subscribed(client, user_id):
    try:
        await client.get_chat_member(CHANNEL_ID, user_id)
        return True
    except UserNotParticipant: return False
    except: return False

# --- COMMANDS ---
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    if not await is_subscribed(client, user_id):
        return await message.reply_text(
            "❌ **Access Denied!**\n\nBot use karne ke liye hamare channel ko join karein.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("✅ Joined (Refresh)", callback_data="check_join")]
            ])
        )
    
    await message.reply_text(
        f"👋 Hello **{message.from_user.first_name}**!\n\nMain menu mein swagat hai. Buttons se bypass file download karein.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📁 StudyRay", callback_data="file_ray"), InlineKeyboardButton("📁 StudyRare", callback_data="file_rare")],
            [InlineKeyboardButton("📁 StudyStark", callback_data="file_stark"), InlineKeyboardButton("📁 DeltaStudy", callback_data="file_delta")],
            [InlineKeyboardButton("📢 Support Channel", url=CHANNEL_LINK)]
        ])
    )

@app.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data

    if data == "check_join":
        if await is_subscribed(client, user_id):
            await query.answer("Shukriya join karne ke liye! ✅")
            await start(client, query.message)
        else:
            await query.answer("Abhi tak join nahi kiya hai! ❌", show_alert=True)

    elif data.startswith("file_"):
        key = data.split("_")[1]
        file_id = FILES.get(key)
        if file_id:
            await query.message.reply_document(file_id)
            await query.answer("File bheji ja rahi hai...")
        else:
            await query.answer("File nahi mili! ❌", show_alert=True)

# --- START BOT ---
if __name__ == "__main__":
    keep_alive() # Render ko zinda rakhne ke liye
    print("Bot is running... 🚀")
    app.run()
            
