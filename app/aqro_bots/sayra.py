class SayraBot:
    def reply(self, user_profile, message: str) -> str:
        msg = "سلام! من Sayra هستم، جستجوگر هوشمند Aqro.\n"
        if "خبر" in message or "اطلاعات" in message:
            msg += " بگو دنبال چه موضوعی هستی تا برات خلاصه و بی‌طرف بگم."
        elif "راهنمایی" in message or "تحقیق" in message:
            msg += " سوالت رو شفاف‌تر بپرس تا دقیق‌تر جستجو کنم."
        else:
            msg += f" پیام «{message}» رو گرفتم. بگو دنبال چی هستی؟"
        return msg
