def evaluate_headers(headers: dict) -> bool:
    SECURITY_HEADERS = [
        "content-security-policy",
        "strict-transport-security",
        "x-content-type-options",
        "x-frame-options",
        "referrer-policy",
        "permissions-policy"
    ]

    headers = {k.lower(): v for k, v in headers.items()}
    present_headers = []
    ausent_headers = []

    for header in SECURITY_HEADERS:
        if header in headers:
            present_headers.append(header)
        else:
            ausent_headers.append(header)

    print(f"{present_headers} están presentes ✅")
    print(f"{ausent_headers} están ausentes ❌")

    site_punctuation = 100
    if "content-security-policy" in ausent_headers:
        site_punctuation -= 25
    if "strict-transport-security" in ausent_headers:
        site_punctuation -= 20
    if "x-frame-options" in ausent_headers:
        site_punctuation -= 20
    if "x-content-type-options" in ausent_headers:
        site_punctuation -= 15
    if "referrer-policy" in ausent_headers:
        site_punctuation -= 10
    if "permissions-policy" in ausent_headers:
        site_punctuation -= 10

    if site_punctuation > 95:
        nivel = "Excelente"
        emoji = "🛡️"
    elif site_punctuation > 80:
        nivel = "Buena"
        emoji = "🔒"
    elif site_punctuation > 50:
        nivel = "Regular"
        emoji = "⚠️"
    else:
        nivel = "Mala"
        emoji = "💀"

    return {
        "score": site_punctuation,
        "level": nivel,
        "emoji": emoji,
        "present": present_headers,
        "missing": ausent_headers,
        "recommendations": (
            [f"Agrega el header '{ausent_headers[0]}' para mejorar la seguridad."]
            if len(ausent_headers) == 1 else
            [f"Agrega los headers {', '.join(f'\"{h}\"' for h in ausent_headers)} para mejorar la seguridad."]
        )
    }
