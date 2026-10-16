from lookups import check_dns, check_whois

for d in ["google.com", "www.google.com", "abcxyz-fake-site-12345.com"]:
    print(d, "→ DNS:", check_dns(d), "| Age, RegLength:", check_whois(d))