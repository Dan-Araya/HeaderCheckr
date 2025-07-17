def evaluate_headers(headers: dict) -> dict:
    missing = []
    issues = []
    score = 100

    # Normalize header names to Title-Case (e.g. x-frame-options → X-Frame-Options)
    normalized = {k.title(): v for k, v in headers.items()}

    def penalize(header_name, check_fn, issue_message, penalty):
        nonlocal score
        value = normalized.get(header_name)
        if value is None:
            missing.append(header_name)
            score -= penalty
        elif not check_fn(value):
            issues.append(issue_message)
            score -= penalty

    penalize(
        "Content-Security-Policy",
        lambda v: "default-src" in v and "*" not in v and "unsafe-inline" not in v and "unsafe-eval" not in v,
        "CSP is too permissive or missing default-src",
        20
    )

    penalize(
        "X-Frame-Options",
        lambda v: v.strip().upper() in ["DENY", "SAMEORIGIN"],
        "X-Frame-Options should be DENY or SAMEORIGIN",
        10
    )

    penalize(
        "X-Content-Type-Options",
        lambda v: v.strip().lower() == "nosniff",
        "X-Content-Type-Options should be nosniff",
        10
    )

    penalize(
        "Strict-Transport-Security",
        lambda v: "max-age" in v and int([s for s in v.split(";") if "max-age" in s][0].split("=")[1]) >= 15552000,
        "HSTS max-age should be at least 6 months",
        10
    )

    penalize(
        "Referrer-Policy",
        lambda v: "unsafe" not in v.lower(),
        "Referrer-Policy should avoid unsafe values",
        10
    )

    penalize(
        "Permissions-Policy",
        lambda v: True,  # Solo verificamos presencia
        "Permissions-Policy header is missing",
        10
    )

    score = max(score, 0)

    return {
        "score": score,
        "missing": missing,
        "issues": issues
    }
