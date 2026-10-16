from lookups import check_ssl

tests = [
    "google.com",              # real, trusted        → expect 1
    "self-signed.badssl.com",  # self-made ID card    → expect 0
    "expired.badssl.com",      # expired ID card      → expect 0
    "neverssl.com",            # no HTTPS at all      → expect -1
    "abcxyz-fake-site-12345.com",  # doesn't exist    → expect -1
]

for d in tests:
    print(d, "→ SSL:", check_ssl(d))