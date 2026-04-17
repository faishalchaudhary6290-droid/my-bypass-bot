import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant

# --- CONFIGURATION ---
API_ID = 32244889  # My.telegram.org se lo
API_HASH = "cb2f194931d477417c78f43c80c3deb2" 
BOT_TOKEN = "8554903983:AAHfNX0a4v4KLP7uymHYdjMRHUVRL3hvPJ8"
CHANNEL_ID = -1003245026048  # Apne channel ki ID dalo (Must be Admin)
CHANNEL_LINK = "https://t.me/ai_smart_tech"

# --- FILE IDS ---
# Pehle bot ko file bhejo, fir uski file_id yahan paste karo
FILES = {
    "ray": "FILE_ID_FOR_STUDYRAY",
    "rare": "FILE_ID_FOR_STUDYRARE",
    "stark": "FILE_ID_FOR_STUDYSTARK",
    "delta": "FILE_ID_FOR_DELTASTUDY"
}

app = Client("BypassBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- HELPER FUNCTION: Check Join ---
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
    
    if await is_subscribed(client, user_id):
        # Main Menu
        await message.reply_text(
            f"👋 Hello **{message.from_user.first_name}**!\n\nMain menu mein aapka swagat hai. Neeche diye gaye buttons se bypass file download karein.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📁 StudyRay", callback_data="get_ray"), InlineKeyboardButton("📁 StudyRare", callback_data="get_rare")],
                [InlineKeyboardButton("📁 StudyStark", callback_data="get_stark"), InlineKeyboardButton("📁 DeltaStudy", callback_data="get_delta")],
                [InlineKeyboardButton("📢 Support Channel", url=CHANNEL_LINK)]
            ])
        )
    else:
        # Force Join Message
        await message.reply_text(
            "❌ **Access Denied!**\n\nBot use karne ke liye aapko hamare channel ko join karna hoga.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("✅ Joined (Refresh)", callback_data="check_join")]
            ])
        )

# --- CALLBACK HANDLER ---
@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data

    # Check Join Button Logic
    if data == "check_join":
        if await is_subscribed(client, user_id):
            await query.answer("Aapka swagat hai! ✅", show_alert=True)
            await query.message.delete()
            await start_cmd(client, query.message)
        else:
            await query.answer("Abhi tak join nahi kiya hai! ❌", show_alert=True)

    # File Delivery Logic
    elif data.startswith("get_"):
        key = data.split("_")[1]
        file_id = FILES.get(key)
        
        if file_id == f"FILE_ID_FOR_{key.upper()}":
            await query.answer("Bhai, pehle file_id to daal code mein! 😂", show_alert=True)
        else:
            await query.answer("Sending File... 🚀")
            await client.send_document(
                chat_id=query.message.chat.id,
                document=file_id,
                caption=f"✅ **{key.capitalize()} Bypass File**\n\nJoin: @{CHANNEL_LINK.split('/')[-1]}"
            )

print("Bot is running... 🚀")
app.run()
  
