"""
Disclaimer Framework — Python Implementation

vnstock-advisor mandatory disclaimer for all surfaces.
Vietnamese is authoritative; English is courtesy translation.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class DisclaimerText:
    """Immutable disclaimer text for a locale."""
    full: str
    short: str

# Single source of truth — mirrors docs/compliance/disclaimer.md
DISCLAIMERS: Dict[str, DisclaimerText] = {
    "vi-VN": DisclaimerText(
        full=(
            "⚠️ **Thông tin chỉ mang tính chất tham khảo, không phải lời khuyên đầu tư.**\n\n"
            "Dữ liệu và phân tích trên vnstock-advisor được cung cấp nhằm mục đích thông tin "
            "và nghiên cứu cá nhân. Chúng tôi không đảm bảo tính chính xác, đầy đủ hoặc kịp "
            "thời của dữ liệu. Mọi quyết định đầu tư dựa trên thông tin này đều do bạn tự "
            "chịu rủi ro. Vui lòng tham khảo ý kiến chuyên gia tài chính độc lập trước khi "
            "đầu tư."
        ),
        short="⚠️ Chỉ mang tính chất tham khảo — Không phải lời khuyên đầu tư."
    ),
    "en-US": DisclaimerText(
        full=(
            "⚠️ **Information for reference only — not financial advice.**\n\n"
            "Data and analysis on vnstock-advisor are provided for informational and "
            "personal research purposes only. We do not guarantee the accuracy, "
            "completeness, or timeliness of the data. All investment decisions based on "
            "this information are at your own risk. Please consult a qualified independent "
            "financial advisor before investing."
        ),
        short="⚠️ Reference only — Not financial advice."
    ),
}

DEFAULT_LOCALE = "vi-VN"
SUPPORTED_LOCALES = frozenset(DISCLAIMERS.keys())


def get_disclaimer(locale: str = DEFAULT_LOCALE, variant: str = "full") -> str:
    """
    Get disclaimer text for locale and variant.

    Args:
        locale: Locale code (vi-VN, en-US). Falls back to DEFAULT_LOCALE.
        variant: "full" or "short"

    Returns:
        Disclaimer text string.
    """
    if locale not in SUPPORTED_LOCALES:
        locale = DEFAULT_LOCALE
    disclaimer = DISCLAIMERS[locale]
    return disclaimer.full if variant == "full" else disclaimer.short


def get_all_disclaimers(variant: str = "full") -> Dict[str, str]:
    """
    Get disclaimer object with all supported locales.

    Used for API response `meta.disclaimer` field.

    Args:
        variant: "full" or "short"

    Returns:
        Dict mapping locale -> disclaimer text.
    """
    return {locale: get_disclaimer(locale, variant) for locale in SUPPORTED_LOCALES}


def build_meta_disclaimer(variant: str = "full") -> Dict[str, str]:
    """
    Build the `meta.disclaimer` object for API responses.

    Returns:
        Dict with vi-VN and en-US keys, ready for JSON serialization.
    """
    return get_all_disclaimers(variant)