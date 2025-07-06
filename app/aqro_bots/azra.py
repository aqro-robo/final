class AzraBot:
    def reply(self, user_profile, message: str) -> str:
        msg = "سلام! من Azra هستم، مسئول امنیت و اینترنت شما.\n"
        if "vpn" in message.lower() or "وی پی ان" in message:
            msg += " برای امنیت بیشتر، استفاده از VPN رو پیشنهاد می‌دم."
        elif "خطر" in message or "امنیت" in message:
            msg += " همه چیز امنه! اگر چیزی غیر عادی دیدی، همینجا اطلاع بده."
        elif "پسورد" in message:
            msg += " هرگز پسوردت رو به هیچ‌کس نده! من همیشه مراقبتم."
        else:
            msg += f" پیام «{message}» رو گرفتم و امنیت رو بررسی کردم."
        return msg
