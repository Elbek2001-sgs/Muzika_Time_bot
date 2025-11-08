import telebot
import requests
import os

# 🔑 O'zingning bot tokeningni shu yerga yoz
BOT_TOKEN = "BU_YERGA_TOKENNI_YOZ"
bot = telebot.TeleBot(BOT_TOKEN)

# 🎵 /start buyrug'i
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom 🎧\nMenga YouTube, Instagram yoki TikTok link yuboring — men sizga MP3 yoki MP4 qilib yuboraman!")

# 📥 Linkni qabul qilish
@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()

    if "youtube.com" in url or "youtu.be" in url:
        download_youtube(url, message)
    elif "tiktok.com" in url:
        download_tiktok(url, message)
    elif "instagram.com" in url:
        download_instagram(url, message)
    else:
        bot.reply_to(message, "❌ Noto‘g‘ri link. Faqat YouTube, TikTok yoki Instagram link yuboring.")

# 🎬 YouTube yuklab olish
def download_youtube(url, message):
    bot.reply_to(message, "⏳ YouTube’dan yuklanmoqda...")

    api = f"https://api.akuari.my.id/downloader/youtube?link={url}"
    r = requests.get(api).json()

    try:
        title = r['title']
        mp3 = r['mp3']
        mp4 = r['mp4']

        bot.send_message(message.chat.id, f"🎵 {title}")
        bot.send_audio(message.chat.id, mp3)
        bot.send_video(message.chat.id, mp4)
    except:
        bot.reply_to(message, "❌ YouTube videoni yuklab bo‘lmadi.")

# 🎥 TikTok yuklab olish
def download_tiktok(url, message):
    bot.reply_to(message, "⏳ TikTok’dan yuklanmoqda...")
    api = f"https://api.akuari.my.id/downloader/tiktok?link={url}"
    r = requests.get(api).json()

    try:
        video = r['video']
        bot.send_video(message.chat.id, video)
    except:
        bot.reply_to(message, "❌ TikTok videoni yuklab bo‘lmadi.")

# 📸 Instagram yuklab olish
def download_instagram(url, message):
    bot.reply_to(message, "⏳ Instagram’dan yuklanmoqda...")
    api = f"https://api.akuari.my.id/downloader/instagram?link={url}"
    r = requests.get(api).json()

    try:
        media = r['url']
        bot.send_video(message.chat.id, media)
    except:
        bot.reply_to(message, "❌ Instagram videoni yuklab bo‘lmadi.")

# 🚀 Botni ishga tushirish
bot.polling()
