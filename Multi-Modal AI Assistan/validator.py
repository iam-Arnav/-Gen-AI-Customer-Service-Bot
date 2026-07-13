def validate_response(answer):

    answer_lower = answer.lower()

    uncertain_words = [
        "cannot determine",
        "can't determine",
        "not sure",
        "unclear",
        "possibly",
        "maybe",
        "might",
        "cannot confirm",
        "unable to",
        "insufficient",
        "not enough information"
    ]

    for word in uncertain_words:

        if word in answer_lower:
            return "Low"

    medium_words = [
        "appears",
        "seems",
        "likely",
        "probably"
    ]

    for word in medium_words:

        if word in answer_lower:
            return "Medium"

    return "High"


def confidence_message(level):

    if level == "High":
        return "🟢 High confidence — the answer is strongly supported by the image."

    if level == "Medium":
        return "🟡 Medium confidence — most of the answer is supported, but some parts involve reasonable interpretation."

    return "🔴 Low confidence — there isn't enough visual evidence to answer confidently."