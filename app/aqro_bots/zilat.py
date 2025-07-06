class ZilatBot:
    def reply(self, user_profile, message: str) -> str:
        msg = "من Zilat هستم؛ منطق‌گرا و کمی طعنه‌زن! 😏\n"
        if "خرافات" in message or "باور" in message:
            msg += " بذار برات منطقی توضیح بدم؛ همیشه اول شواهد رو بررسی کن!"
        elif "طنز" in message or "جوک" in message:
            msg += " دوست داری یه شوخی بامزه بشنوی؟"
        else:
            msg += f" پیام «{message}» رو گرفتم. یادت باشه همیشه همه چیز رو زیر سوال ببر!"
        return msg
