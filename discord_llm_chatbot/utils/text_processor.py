# utils/text_processor.py
import re
import uwuify
from typing import Optional

class TextProcessor:
    @staticmethod
    def process_response_text(text: str) -> str:
        """Removes the '-sent by X' context flags from response."""
        # Remove %(replying to *)%
        text = re.sub(r".(r|R)eplying to\s?.*", "", text)

        # Remove -sent by %USERNAME "anything" space in regex
        text = re.sub(r"[-–(]\s?(?:sent\sby\s)?\"?(v|V)i\s?(v|V)i(#5153)?\"?(:|)\s?[^\s]*\s?", "", text)

        # Remove digits
        text = re.sub(r"#[0-9][0-9][0-9][0-9]", "", text)
        return text

    @staticmethod
    def uwuify_text(text: str, message_content: Optional[str] = None, smiley: bool = True) -> str:
        if message_content and "uwu" in message_content.lower():
            flags = uwuify.SMILEY | uwuify.YU | uwuify.STUTTER
        elif smiley:
            flags = uwuify.SMILEY | uwuify.NOUWU
        else:
            return text

        try:
            return uwuify.uwu(text, flags=flags)
        except Exception:
            return text
