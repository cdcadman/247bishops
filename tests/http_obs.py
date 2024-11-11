"""This tests the website's header security after it is deployed.
It is meant to be run on a schedule."""

import requests


def check_headers():
    response = requests.post(
        "https://observatory-api.mdn.mozilla.net/api/v2/scan?host=247bishops.com",
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
    failures = data["tests_failed"]
    details = data["details_url"]
    if failures > 0:
        raise RuntimeError(
            f"Header security vulnerabilities were detected.  Follow this link for details: {details}"
        )


if __name__ == "__main__":
    check_headers()
