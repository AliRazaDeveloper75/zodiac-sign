zodiac_traits = {
    "Aries": "Bold, energetic and born leader.",
    "Taurus": "Stable, loyal and wealth focused.",
    "Gemini": "Smart, communicative and adaptable.",
    "Cancer": "Emotional, caring and intuitive.",
    "Leo": "Confident, ambitious and powerful.",
    "Virgo": "Detail-oriented and analytical.",
    "Libra": "Balanced and charming.",
    "Scorpio": "Intense and passionate.",
    "Sagittarius": "Adventurous and optimistic.",
    "Capricorn": "Disciplined and responsible.",
    "Aquarius": "Innovative and independent.",
    "Pisces": "Spiritual and emotional."
}

def get_zodiac_trait(zodiac):
    return zodiac_traits.get(zodiac, "")
 