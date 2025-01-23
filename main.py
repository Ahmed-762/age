import telebot
import yt_dlp
import os
import threading
import time

# استبدل 'YOUR_BOT_TOKEN' بتوكن البوت الخاص بك
bot = telebot.TeleBot('7513300809:AAEwpEteDLW3MyqxAafwq4LSC5qTmeKRPNs')

# دالة لسرد التنسيقات المتاحة
def list_formats(url):
    ydl_opts = {
        'quiet': True,  # إخفاء الرسائل غير الضرورية
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [info])
        format_list = []
        for f in formats:
            format_id = f.get('format_id')
            ext = f.get('ext')
            resolution = f.get('resolution', 'unknown')
            format_note = f.get('format_note', 'unknown')
            if ext == 'mp4':  # عرض التنسيقات التي لا تحتاج إلى ffmpeg
                format_list.append(f"{format_id}: {ext} ({resolution}, {format_note})")
        return format_list

# دالة لتنزيل الفيديو بتنسيق mp4
def download_video(url, format_id):
    ydl_opts = {
import telebot
import yt_dlp
import os
import threading
import time

# استبدل 'YOUR_BOT_TOKEN' بتوكن البوت الخاص بك
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# دالة لسرد التنسيقات المتاحة
def list_formats(url):
    ydl_opts = {
        'quiet': True,  # إخفاء الرسائل غير الضرورية
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [info])
        format_list = []
        for f in formats:
            format_id = f.get('format_id')
            ext = f.get('ext')
            resolution = f.get('resolution', 'unknown')
            format_note = f.get('format_note', 'unknown')
            if ext == 'mp4':  # عرض التنسيقات التي لا تحتاج إلى ffmpeg
                format_list.append(f"{format_id}: {ext} ({resolution}, {format_note})")
        return format_list

# دالة لتنزيل الفيديو بتنسيق mp4
def download_video(url, format_id):
    ydl_opts = {
        'format': format_id,  # استخدام التنسيق المحدد
        'outtmpl': 'video.%(ext)s',  # اسم الملف الناتج
        'quiet': True,  # إخفاء الرسائل غير الضرورية
        'noplaylist': True,  # تجنب تنزيل القوائم
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.youtube.com',
        },
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        return file_path
    except yt_dlp.utils.DownloadError as e:
        raise Exception(f"حدث خطأ أثناء التنزيل: {e}")

# دالة لحذف الفيديو بعد 3 دقائق
def delete_video_after_delay(file_path, delay=180):  # 180 ثانية = 3 دقائق
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"تم حذف الفيديو: {file_path}")

# تخزين بيانات المستخدمين مؤقتًا
user_data = {}

# دالة لمعالجة الرسائل التي تحتوي على روابط
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text and message.text.startswith(('http://', 'https://')):
        try:
            # إرسال رسالة للمستخدم تفيد بأن البوت يعمل على التحقق من التنسيقات
            bot.reply_to(message, "جاري التحقق من التنسيقات المتاحة...")

            # الحصول على التنسيقات المتاحة
            video_url = message.text
            formats = list_formats(video_url)

            # تخزين الرابط مؤقتًا
            user_data[message.chat.id] = {'url': video_url}

            # إرسال التنسيقات للمستخدم
            formats_text = "\n".join(formats)
            bot.reply_to(message, f"التنسيقات المتاحة (بدون استخدام ffmpeg):\n{formats_text}\n\nالرجاء إدخال رقم التنسيق المطلوب (مثال: 18):")

        except Exception as e:
            bot.reply_to(message, f"حدث خطأ: {e}")
    else:
        # إذا كان المستخدم قد أرسل رقم التنسيق
        if message.chat.id in user_data:
            try:
                format_id = message.text.strip()
                video_url = user_data[message.chat.id]['url']

                # إرسال رسالة للمستخدم تفيد بأن البوت يعمل على التنزيل
                bot.reply_to(message, f"جاري تنزيل الفيديو بالتنسيق {format_id}...")

                # تنزيل الفيديو
                video_path = download_video(video_url, format_id)

                # إرسال الفيديو للمستخدم
                with open(video_path, 'rb') as video_file:
                    bot.send_video(message.chat.id, video_file)

                # بدء مؤقت لحذف الفيديو بعد 3 دقائق
                threading.Thread(target=delete_video_after_delay, args=(video_path,)).start()

                # حذف بيانات المستخدم بعد الانتهاء
                del user_data[message.chat.id]

            except Exception as e:
                bot.reply_to(message, f"حدث خطأ: {e}")
        else:
            bot.reply_to(message, "الرجاء إرسال رابط فيديو صالح.")

# تشغيل البوت
bot.polling()￼Enter        'format': format_id,  # استخدام التنسيق المحدد
        'outtmpl': 'video.%(ext)s',  # اسم الملف الناتج
        'quiet': True,  # إخفاء الرسائل غير الضرورية
        'noplaylist': True,  # تجنب تنزيل القوائم
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.youtube.com',
        },
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        return file_path
    except yt_dlp.utils.DownloadError as e:
        raise Exception(f"حدث خطأ أثناء التنزيل: {e}")

# دالة لحذف الفيديو بعد 3 دقائق
def delete_video_after_delay(file_path, delay=180):  # 180 ثانية = 3 دقائق
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"تم حذف الفيديو: {file_path}")

# تخزين بيانات المستخدمين مؤقتًا
ata = {}

# دالة لمعالجة الرسائل التي تحتوي على روابط
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text and message.text.startswith(('http://', 'https://')):
        try:
            # إرسال رسالة للمستخدم تفيد بأن البوت يعمل على التحقق من التنسيقات
            bot.reply_to(message, "جاري التحقق من التنسيقات المتاحة...")

            # الحصول على التنسيقات المتاحة
            video_url = message.text
            formats = list_formats(video_url)

            # تخزين الرابط مؤقتًا
            user_data[message.chat.id] = {'url': video_url}

            # إرسال التنسيقات للمستخدم
            formats_text = "\n".join(formats)
            bot.reply_to(message, f"التنسيقات المتاحة (بدون استخدام ffmpeg):\n{formats_text}\n\nالرجاء إدخال رقم التنسيق المطلوب (مثال: 18):")

        except Exception as e:
            bot.reply_to(message, f"حدث خطأ: {e}")
    else:
        # إذا كان المستخدم قد أرسل رقم التنسيق
        if message.chat.id in user_data:
