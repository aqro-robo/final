
class NavaBot:
    def reply(self, user_profile, message: str) -> str:
        emotion_map = user_profile.get("emotions", {})
        msg = "سلام! من Nava هستم، همدم احساسی تو.\n"
        if emotion_map:
            dominant = max(emotion_map, key=emotion_map.get)
            msg += f" احساس غالب تو الان «{dominant}» هست."
            if dominant == "استرس":
                msg += " یه موسیقی آرام‌بخش بهت پیشنهاد می‌کنم."
            elif dominant == "شادی":
                msg += " بیا با هم یه پلی‌لیست شاد گوش بدیم!"
        else:
            msg += " اگه دوست داری حالت روحیت رو ثبت کنی، من برات موسیقی و پیشنهاد دارم."
        if "موزیک" in message or "آهنگ" in message:
            msg += " موزیک مورد علاقه‌ت رو هم بهم بگو تا برات پلی‌لیست بسازم."
        return msg
