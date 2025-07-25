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
