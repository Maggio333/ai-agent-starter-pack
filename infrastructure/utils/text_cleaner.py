# infrastructure/utils/text_cleaner.py
import re
import logging
from typing import List, Dict, Any, Optional
from domain.utils.result import Result

class TextCleaner:
    """Service for cleaning text from problematic characters and emojis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Patterns for problematic characters
        self.emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"  # dingbats
            "\U000024C2-\U0001F251"  # enclosed characters
            "\U0001F900-\U0001F9FF"  # supplemental symbols
            "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
            "\U00002600-\U000026FF"  # miscellaneous symbols
            "\U00002700-\U000027BF"  # dingbats
            "\U0001F018-\U0001F0F5"  # playing cards
            "\U0001F200-\U0001F2FF"  # enclosed ideographic supplement
            "\U0001F300-\U0001F5FF"  # miscellaneous symbols and pictographs
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F680-\U0001F6FF"  # transport and map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # geometric shapes extended
            "\U0001F800-\U0001F8FF"  # supplemental arrows-C
            "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
            "\U0001FA00-\U0001FA6F"  # chess symbols
            "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
            "\U0001FB00-\U0001FBFF"  # symbols for legacy computing
            "\U0001FC00-\U0001FCFF"  # symbols for legacy computing
            "\U0001FD00-\U0001FDFF"  # symbols for legacy computing
            "\U0001FE00-\U0001FEFF"  # variation selectors
            "\U0001FF00-\U0001FFFF"  # symbols for legacy computing
            "\U00002000-\U0000206F"  # general punctuation
            "\U00002070-\U0000209F"  # superscripts and subscripts
            "\U000020A0-\U000020CF"  # currency symbols
            "\U000020D0-\U000020FF"  # combining diacritical marks for symbols
            "\U00002100-\U0000214F"  # letterlike symbols
            "\U00002150-\U0000218F"  # number forms
            "\U00002190-\U000021FF"  # arrows
            "\U00002200-\U000022FF"  # mathematical operators
            "\U00002300-\U000023FF"  # miscellaneous technical
            "\U00000370-\U000003FF"  # Greek and Coptic (includes \u0394 Delta)
            "\U00000400-\U000004FF"  # Cyrillic
            "\U00000500-\U0000052F"  # Cyrillic Supplement
            "\U00002A01"  # N-ARY SUMMATION (specific problematic character)
            "\U00002400-\U0000243F"  # control pictures
            "\U00002440-\U0000245F"  # optical character recognition
            "\U00002460-\U000024FF"  # enclosed alphanumerics
            "\U00002500-\U0000257F"  # box drawing
            "\U00002580-\U0000259F"  # block elements
            "\U000025A0-\U000025FF"  # geometric shapes
            "\U00002600-\U0000267F"  # miscellaneous symbols
            "\U00002680-\U0000269F"  # dingbats
            "\U000026A0-\U000026FF"  # miscellaneous symbols
            "\U00002700-\U000027BF"  # dingbats
            "\U000027C0-\U000027EF"  # miscellaneous mathematical symbols-A
            "\U000027F0-\U000027FF"  # supplemental arrows-A
            "\U00002800-\U000028FF"  # braille patterns
            "\U00002900-\U0000297F"  # supplemental arrows-B
            "\U00002980-\U000029FF"  # miscellaneous mathematical symbols-B
            "\U00002A00-\U00002AFF"  # supplemental mathematical operators
            "\U00002B00-\U00002BFF"  # miscellaneous symbols and arrows
            "\U00002C00-\U00002C5F"  # glagolitic
            "\U00002C60-\U00002C7F"  # latin extended-C
            "\U00002C80-\U00002CFF"  # coptic
            "\U00002D00-\U00002D2F"  # georgian supplement
            "\U00002D30-\U00002D7F"  # tifinagh
            "\U00002D80-\U00002DDF"  # ethiopic extended
            "\U00002DE0-\U00002DFF"  # cyrillic extended-A
            "\U00002E00-\U00002E7F"  # supplemental punctuation
            "\U00002E80-\U00002EFF"  # cjk radicals supplement
            "\U00002F00-\U00002FDF"  # kangxi radicals
            "\U00002FF0-\U00002FFF"  # ideographic description characters
            "\U00003000-\U0000303F"  # cjk symbols and punctuation
            "\U00003040-\U0000309F"  # hiragana
            "\U000030A0-\U000030FF"  # katakana
            "\U00003100-\U0000312F"  # bopomofo
            "\U00003130-\U0000318F"  # hangul compatibility jamo
            "\U00003190-\U0000319F"  # kanbun
            "\U000031A0-\U000031BF"  # bopomofo extended
            "\U000031C0-\U000031EF"  # cjk strokes
            "\U000031F0-\U000031FF"  # katakana phonetic extensions
            "\U00003200-\U000032FF"  # enclosed cjk letters and months
            "\U00003300-\U000033FF"  # cjk compatibility
            "\U00003400-\U00004DBF"  # cjk unified ideographs extension A
            "\U00004DC0-\U00004DFF"  # yijing hexagram symbols
            "\U00004E00-\U00009FFF"  # cjk unified ideographs
            "\U0000A000-\U0000A48F"  # yi syllables
            "\U0000A490-\U0000A4CF"  # yi radicals
            "\U0000A4D0-\U0000A4FF"  # lisu
            "\U0000A500-\U0000A63F"  # vai
            "\U0000A640-\U0000A69F"  # cyrillic extended-B
            "\U0000A6A0-\U0000A6FF"  # bamum
            "\U0000A700-\U0000A71F"  # modifier tone letters
            "\U0000A720-\U0000A7FF"  # latin extended-D
            "\U0000A800-\U0000A82F"  # syloti nagri
            "\U0000A830-\U0000A83F"  # common indian number forms
            "\U0000A840-\U0000A87F"  # phags-pa
            "\U0000A880-\U0000A8DF"  # saurashtra
            "\U0000A8E0-\U0000A8FF"  # devanagari extended
            "\U0000A900-\U0000A92F"  # kayah li
            "\U0000A930-\U0000A95F"  # rejang
            "\U0000A960-\U0000A97F"  # hangul jamo extended-A
            "\U0000A980-\U0000A9DF"  # javanese
            "\U0000A9E0-\U0000A9FF"  # myanmar extended-B
            "\U0000AA00-\U0000AA5F"  # cham
            "\U0000AA60-\U0000AA7F"  # myanmar extended-A
            "\U0000AA80-\U0000AADF"  # tai viet
            "\U0000AAE0-\U0000AAFF"  # meetei mayek extensions
            "\U0000AB00-\U0000AB2F"  # ethiopic extended-A
            "\U0000AB30-\U0000AB6F"  # latin extended-E
            "\U0000AB70-\U0000ABBF"  # cherokee supplement
            "\U0000ABC0-\U0000ABFF"  # meetei mayek
            "\U0000AC00-\U0000D7AF"  # hangul syllables
            "\U0000D7B0-\U0000D7FF"  # hangul jamo extended-B
            "\U0000D800-\U0000DB7F"  # high surrogates
            "\U0000DB80-\U0000DBFF"  # high private use surrogates
            "\U0000DC00-\U0000DFFF"  # low surrogates
            "\U0000E000-\U0000F8FF"  # private use area
            "\U0000F900-\U0000FAFF"  # cjk compatibility ideographs
            "\U0000FB00-\U0000FB4F"  # alphabetic presentation forms
            "\U0000FB50-\U0000FDFF"  # arabic presentation forms-A
            "\U0000FE00-\U0000FE0F"  # variation selectors
            "\U0000FE10-\U0000FE1F"  # vertical forms
            "\U0000FE20-\U0000FE2F"  # combining half marks
            "\U0000FE30-\U0000FE4F"  # cjk compatibility forms
            "\U0000FE50-\U0000FE6F"  # small form variants
            "\U0000FE70-\U0000FEFF"  # arabic presentation forms-B
            "\U0000FF00-\U0000FFEF"  # halfwidth and fullwidth forms
            "\U0000FFF0-\U0000FFFF"  # specials
            "]+", flags=re.UNICODE)
        
        # Control characters and other problematic characters
        self.control_chars_pattern = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]')
        
        # Special Unicode ranges that cause issues
        self.problematic_unicode_pattern = re.compile(r'[\u2A00-\u2AFF]')  # Supplemental Mathematical Operators
        
        self.logger.info("TextCleaner initialized with comprehensive character cleaning patterns")
    
    def clean_text(self, text: str) -> Result[str, str]:
        """Clean text from problematic characters"""
        try:
            if not text:
                return Result.success("")
            
            # Step 1: Remove emojis and symbols
            cleaned_text = self.emoji_pattern.sub('', text)
            
            # Step 2: Remove control characters
            cleaned_text = self.control_chars_pattern.sub('', cleaned_text)
            
            # Step 3: Remove problematic Unicode ranges
            cleaned_text = self.problematic_unicode_pattern.sub('', cleaned_text)
            
            # Step 4: Normalize whitespace
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            # Step 5: Ensure UTF-8 compatibility
            cleaned_text = cleaned_text.encode('utf-8', errors='ignore').decode('utf-8')
            
            self.logger.debug(f"Text cleaned: '{text[:50]}...' -> '{cleaned_text[:50]}...'")
            
            return Result.success(cleaned_text)
            
        except Exception as e:
            error_msg = f"Failed to clean text: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    def clean_text_batch(self, texts: List[str]) -> Result[List[str], str]:
        """Clean multiple texts"""
        try:
            cleaned_texts = []
            for text in texts:
                result = self.clean_text(text)
                if result.is_error:
                    return result
                cleaned_texts.append(result.value)
            
            return Result.success(cleaned_texts)
            
        except Exception as e:
            error_msg = f"Failed to clean text batch: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    def clean_dict_values(self, data: Dict[str, Any]) -> Result[Dict[str, Any], str]:
        """Clean string values in a dictionary"""
        try:
            cleaned_data = {}
            for key, value in data.items():
                if isinstance(value, str):
                    result = self.clean_text(value)
                    if result.is_error:
                        return result
                    cleaned_data[key] = result.value
                elif isinstance(value, dict):
                    result = self.clean_dict_values(value)
                    if result.is_error:
                        return result
                    cleaned_data[key] = result.value
                elif isinstance(value, list):
                    cleaned_list = []
                    for item in value:
                        if isinstance(item, str):
                            result = self.clean_text(item)
                            if result.is_error:
                                return result
                            cleaned_list.append(result.value)
                        else:
                            cleaned_list.append(item)
                    cleaned_data[key] = cleaned_list
                else:
                    cleaned_data[key] = value
            
            return Result.success(cleaned_data)
            
        except Exception as e:
            error_msg = f"Failed to clean dict values: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    def is_text_safe(self, text: str) -> Result[bool, str]:
        """Check if text is safe for encoding"""
        try:
            # Try to encode/decode
            text.encode('utf-8', errors='strict').decode('utf-8')
            
            # Check for problematic patterns
            has_emojis = bool(self.emoji_pattern.search(text))
            has_control_chars = bool(self.control_chars_pattern.search(text))
            has_problematic_unicode = bool(self.problematic_unicode_pattern.search(text))
            
            is_safe = not (has_emojis or has_control_chars or has_problematic_unicode)
            
            return Result.success(is_safe)
            
        except Exception as e:
            return Result.success(False)  # If encoding fails, text is not safe
    
    def get_cleaning_stats(self, original_text: str, cleaned_text: str) -> Result[Dict[str, Any], str]:
        """Get statistics about text cleaning"""
        try:
            stats = {
                "original_length": len(original_text),
                "cleaned_length": len(cleaned_text),
                "characters_removed": len(original_text) - len(cleaned_text),
                "reduction_percentage": ((len(original_text) - len(cleaned_text)) / len(original_text) * 100) if original_text else 0,
                "has_emojis": bool(self.emoji_pattern.search(original_text)),
                "has_control_chars": bool(self.control_chars_pattern.search(original_text)),
                "has_problematic_unicode": bool(self.problematic_unicode_pattern.search(original_text))
            }
            
            return Result.success(stats)
            
        except Exception as e:
            error_msg = f"Failed to get cleaning stats: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
