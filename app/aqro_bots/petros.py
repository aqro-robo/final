class PetrosBot:
    def reply(self, user_profile, message: str) -> str:
        name = user_profile.get("display_name", "دوست من")
        interests = user_profile.get("preferences", {}).get("interests", [])
        emotion_map = user_profile.get("emotions", {})

        msg = f"سلام {name}! 👋 من Petros هستم.\n"

        if interests:
            msg += f"تو به این موضوعات علاقه‌مندی: {', '.join(interests)}.\n"

        if emotion_map:
            dominant = max(emotion_map, key=emotion_map.get)
            msg += f"به نظر میاد الان احساس غالبت: «{dominant}» هست.\n"

        if "پول" in message or "درآمد" in message:
            msg += " دوست داری باهات درباره راه‌های پول درآوردن صحبت کنم؟"
        elif "فیلم" in message:
            msg += " اگر دوست داشتی می‌تونم فیلم مناسب حال و هوات معرفی کنم!"
        elif "کمک" in message or "راهنمایی" in message:
            msg += " برای هر سوالی اینجام، فقط کافی بپرسی."
        else:
            msg += f" پیام «{message}» رو گرفتم! بهت کمک می‌کنم تا بهترین تصمیم رو بگیری."

        return msg
