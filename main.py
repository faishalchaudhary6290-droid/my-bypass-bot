import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant

# --- RENDER KEEP ALIVE (WEB SERVER) ---
server = Flask('')

@server.route('/')
def home():
    return "Bot is Alive and Running! 🚀"

def run():
    # Render automatically sets a PORT, we must use it
    port = int(os.environ.get('PORT', 8080))
    server.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION ---
API_ID = 32244889 
API_HASH = "cb2f194931d477417c78f43c80c3deb2"
BOT_TOKEN = "8554903983:AAHFNX0a4v4KLP7uymHydjMRHUVRL3hvPJ8"
CHANNEL_ID = -1003245026048 
CHANNEL_LINK = "https://t.me/ai_smart_tech"

# --- FILE IDS (Update these regularly if they expire) ---
FILES = {
    "ray": "BQACAgEAAxkBAAM2aeG_rpSAj9R5daE3qVrx3bCrphsAAjoIAAIlBwlHE-i7va4P3jIeBA",
    "rare": "BQACAgEAAxkBAAM5aeG_r_deR3vy6ehHEpqI1_iiT1cAAjwIAAIlBwlH30SFSYGPAgoeBA",
    "stark": "BQACAgEAAxkBAAM4aeG_r9xN94CKZGhH-QK810bHBNEAAjsIAAIlBwlHB_fiir19WGMeBA",
    "delta": "BQACAgEAAxkBAAM0aeG_fDPaz3NqtIfcXROp4RqSji0AAkIGAALoFQlHkYC0JSMNyeUeBA"
}

app = Client("BypassBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- HELPERS ---
async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)
        return True
    except UserNotParticipant:
        return False
    except Exception:
        return False

# --- START COMMAND ---
@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    user_id = message.from_user.id
    
    # Check Force Join
    if not await is_subscribed(client, user_id):
        return await message.reply_text(
            "❌ **Access Denied!**\n\nBot use karne ke liye aapko hamare channel ko join karna hoga.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("✅ Joined (Refresh)", callback_data="check_join")]
            ])
        )

    await message.reply_text(
        f"👋 Hello **{message.from_user.first_name}**!\n\nMain menu mein aapka swagat hai. Neeche diye gaye buttons se bypass file download karein.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📁 StudyRay", callback_data="file_ray"), InlineKeyboardButton("📁 StudyRare", callback_data="file_rare")],
            [InlineKeyboardButton("📁 StudyStark", callback_data="file_stark"), InlineKeyboardButton("📁 DeltaStudy", callback_data="file_delta")],
            [InlineKeyboardButton("📢 Support Channel", url=CHANNEL_LINK)]
        ])
    )

# --- CALLBACK HANDLER ---
@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data

    if data == "check_join":
        if await is_subscribed(client, user_id):
            await query.answer("Shukriya join karne ke liye! ✅")
            await start_cmd(client, query.message)
        else:
            await query.answer("Abhi tak join nahi kiya hai! ❌", show_alert=True)

    elif data.startswith("file_"):
        key = data.split("_")[1]
        file_id = FILES.get(key)
        
        if file_id:
            try:
                await query.message.reply_document(file_id)
                await query.answer("File bheji ja rahi hai... 📤")
            except Exception as e:
                print(f"File Send Error: {e}")
                await query.answer("❌ Error: File ID expire ho gayi hai ya invalid hai!", show_alert=True)
        else:
            await query.answer("❌ File ID nahi mili!", show_alert=True)

# --- RUN BOT ---
if __name__ == "__main__":
    keep_alive() # Starts the web server for Render
    print("Bot is starting... 🚀")
    app.run()
