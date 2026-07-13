from lingua import Language, LanguageDetectorBuilder

languages = [
    Language.ENGLISH,
    Language.HINDI,
    Language.SPANISH,
    Language.FRENCH,
]

detector = LanguageDetectorBuilder.from_languages(
    *languages
).build()

LANGUAGE_CODES = {
    Language.ENGLISH: ("en", "English"),
    Language.HINDI: ("hi", "Hindi"),
    Language.SPANISH: ("es", "Spanish"),
    Language.FRENCH: ("fr", "French"),
}


def detect_language(text):

    language = detector.detect_language_of(text)

    if language is None:
        return "en", "English"

    return LANGUAGE_CODES.get(
        language,
        ("en", "English")
    )