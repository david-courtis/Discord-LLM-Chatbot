# utils/text_processor.py
import re
from typing import Dict, Optional

import uwuify


class TextProcessor:
    @staticmethod
    def parse_message(text: str) -> Optional[Dict[str, str]]:
        """Parses structured message format into components."""
        pattern = r"<\|start\|>\nauthor: (.*?)\nmessage: (.*?)\nreply_to: (.*?)\n<\|end\|>"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return {
                "author": match.group(1).strip(),
                "message": match.group(2).strip(),
                "reply_to": None if match.group(3) == "null" else match.group(3).strip()
            }
        return None

    @staticmethod
    def process_response_text(text: str) -> str:
        """Extracts just the message content from a structured response."""
        parsed = TextProcessor.parse_message(text)
        if parsed:
            print(text)
            return parsed["message"]

        # Fallback to original cleanup if parsing fails
        text = re.sub(r".(r|R)eplying to\s?.*", "", text)

        # Remove -sent by %USERNAME "anything" space in regex
        text = re.sub(
            r"[-–(]\s?(?:sent\sby\s)?\"?(v|V)i\s?(v|V)i(#5153)?\"?(:|)\s?[^\s]*\s?",
            "",
            text,
        )

        # Remove digits
        text = re.sub(r"#[0-9][0-9][0-9][0-9]", "", text)
        return text

    @staticmethod
    def uwuify_text(
        text: str, message_content: Optional[str] = None, smiley: bool = True
    ) -> str:
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