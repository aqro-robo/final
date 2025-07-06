class ZentroxBot:
    def reply(self, user_profile, message: str) -> str:
        msg = "سلام! من Zentrox هستم، ایده‌پرداز کسب درآمد و کارهای جانبی.\n"
        skills = user_profile.get("skills", [])
        if "ایده" in message or "پول" in message:
            if skills:
                msg += f" با توجه به مهارت‌هات ({', '.join(skills)}) چند ایده: فریلنسینگ، آموزش آنلاین، فروش خدمات دیجیتال."
            else:
                msg += " اگر مهارت‌هاتو وارد کنی، می‌تونم ایده‌های بهتری بدم!"
        elif "استارتاپ" in message:
            msg += " دوست داری یک استارتاپ راه بندازی؟ می‌خوای راهنمایی کنم؟"
        else:
            msg += f" پیام «{message}» رو گرفتم، ایده‌ جدید می‌خوای یا راه پول درآوردن؟"
        return msg
