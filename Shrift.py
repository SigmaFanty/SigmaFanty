# meta developer: @QzKat
# meta banner: ShriftMod - автоформатирование исходящих сообщений: жирный, курсив, моно, цитата, скрытый, жирный курсив, кодовый 

import re
import logging
from .. import loader, utils

@loader.tds
class ShriftMod(loader.Module):
    """
    Модуль ShriftMod - автоформатирование исходящих сообщений: жирный, курсив, моно, цитата, скрытый, жирный курсив, кодовый
    """
    strings = {
        "name": "ShriftMod",
        "help": (
            "🪐 Модуль ShriftMod загружен (๑•‌ ヮ •‌๑)\n"
            "ℹ️ Модуль ShriftMod - автоформатирование исходящих сообщений: жирный, курсив, моно, цитата, скрытый, жирный курсив, кодовый \n\n"
            "▫️ 0bold Включить/выключить шрифт жирного текста.\n"
            "▫️ 0bolditalic Включить/выключить шрифт жирного курсива.\n"
            "▫️ 0code Включить/выключить режим кода.\n"
            "▫️ 0hidden включить/выключить режим скрытого текста.\n"
            "▫️ 0italic Включить/выключить шрифт курсив.\n"
            "▫️ 0mono Включить/выключить шрифт моно.\n"
            "▫️ 0quote Включить/выключить режим цитирования.\n\n"
            "🫶 Разработчик: @QzKat"
        )
    }

    def __init__(self):
        self.mode = None  

    async def client_ready(self, client, db):
        self.client = client

    async def _toggle_mode(self, message, new_mode: str, mode_descr: str):
        if self.mode == new_mode:
            self.mode = None
            await message.edit(f"Режим «{mode_descr}» выключен.", parse_mode="html")
        else:
            self.mode = new_mode
            await message.edit(f"Режим форматирования установлен: {mode_descr}", parse_mode="html")

    async def boldcmd(self, message):
        """Включить/выключить шрифт жирного текста."""
        await self._toggle_mode(message, "bold", "<b>жирный</b>")

    async def italiccmd(self, message):
        """Включить/выключить шрифт курсив."""
        await self._toggle_mode(message, "italic", "<i>курсив</i>")

    async def monocmd(self, message):
        """Включить/выключить шрифт моно."""
        await self._toggle_mode(message, "mono", "<code>моно</code>")

    async def quotecmd(self, message):
        """Включить/выключить режим цитирования."""
        await self._toggle_mode(message, "quote", "<blockquote>цитата</blockquote>")

    async def hiddencmd(self, message):
        """Включить/выключить режим скрытого текста."""
        await self._toggle_mode(message, "hidden", "<tg-spoiler>скрытый</tg-spoiler>")

    async def bolditaliccmd(self, message):
        """Включить/выключить шрифт жирного курсива."""
        await self._toggle_mode(message, "bolditalic", "<b><i>жирный курсив</i></b>")

    async def codecmd(self, message):
        """Включить/выключить режим кода."""
        await self._toggle_mode(message, "codeblock", "```кодовый```")

    async def watcher(self, message):
        if self.mode is None:
            return

        text = message.raw_text
        text = re.sub(r'</?(?:b|i|code|tg-spoiler|blockquote)>', '', text, flags=re.IGNORECASE)

        if self.mode == "bold":
            new_text = f"<b>{text}</b>"
            parse_mode = "html"
        elif self.mode == "italic":
            new_text = f"<i>{text}</i>"
            parse_mode = "html"
        elif self.mode == "mono":
            new_text = f"<code>{text}</code>"
            parse_mode = "html"
        elif self.mode == "quote":
            new_text = f"<blockquote>{text}</blockquote>"
            parse_mode = "html"
        elif self.mode == "hidden":
            new_text = f"<tg-spoiler>{text}</tg-spoiler>"
            parse_mode = "html"
        elif self.mode == "bolditalic":
            new_text = f"<b><i>{text}</i></b>"
            parse_mode = "html"
        elif self.mode == "codeblock":
            new_text = f"```{text}```"
            parse_mode = "md"
        else:
            return

        try:
            await message.edit(new_text, parse_mode=parse_mode)
        except Exception as e:
            logging.error("ShriftMod: не удалось отредактировать сообщение", exc_info=e)