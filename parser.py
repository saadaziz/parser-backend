import re

def parse_listing_deprecate(text):
    # You will replace this with spaCy, BERT, etc. later!
    data = {}
    price_match = re.search(r"Asking Price[:\s]*\$?([\d,]+)", text)
    if price_match:
        data["asking_price"] = int(price_match.group(1).replace(",", ""))

    revenue_match = re.search(r"Revenue[:\s]*\$?([\d,]+)", text)
    if revenue_match:
        data["revenue"] = int(revenue_match.group(1).replace(",", ""))

    # ...add more fields as needed...
    return data

FIELD_SCHEMA = {
    "business_name": {
        "patterns": [r"^(.*)\n"],   # First line, or customize!
        "post": lambda v, text: v.strip() if v else None,
    },
    "asking_price": {
        "patterns": [r"Asking Price[:\s]*\$?([\d,]+)", r"Price[:\s]*\$?([\d,]+)"],
        "post": lambda v, _: float(v.replace(",", "")) if v else None,
    },
    "revenue": {
        "patterns": [r"Gross Revenue[:\s]*\$?([\d,]+)"],
        "post": lambda v, _: float(v.replace(",", "")) if v else None,
    },
    "sde": {
        "patterns": [r"Cash Flow.*?([\d,]+)", r"SDE.*?([\d,]+)", r"EBITDA.*?([\d,]+)"],
        "post": lambda v, _: float(v.replace(",", "")) if v else None,
    },
    "real_estate": {
        "patterns": [
            r"real estate[\s:]*included",
            r"property[\s:]*included",
            r"includes real estate[\s:]*included",
        ],
        "post": lambda v, text: bool(v),
    },
    "location": {
        "patterns": [r"Location[:\s]*(.*)", r"\b([A-Za-z\s,]+, [A-Z]{2})\b"],
        "post": lambda v, _: v.strip() if v else None,
    },
    # ...add more fields
}

def normalize_newlines(text):
    # Handles \r, \r\n, \n, and PowerShell backticks `n
    return re.sub(r'(\r\n|\r|\n|`n)', '\n', text)

def parse_listing(text):
    text = normalize_newlines(text)
    data = {}

    # Business Name (assume first non-empty line)
    lines = text.strip().split('\n')
    for line in lines:
        if line.strip():
            data["business_name"] = line.strip()
            break

    # Asking Price
    price_match = re.search(r"Asking Price[:\s]*\$?([\d,]+)", text, re.I)
    if price_match:
        data["asking_price"] = int(price_match.group(1).replace(",", ""))

    # Gross Revenue
    rev_match = re.search(r"Gross Revenue[:\s]*\$?([\d,]+)", text, re.I)
    if rev_match:
        data["revenue"] = int(rev_match.group(1).replace(",", ""))

    # SDE/Cash Flow
    sde_match = re.search(r"Cash Flow.*?\$([\d,]+)", text, re.I)
    if not sde_match:
        sde_match = re.search(r"SDE.*?\$([\d,]+)", text, re.I)
    if sde_match:
        data["sde"] = int(sde_match.group(1).replace(",", ""))

    # Robust Real Estate Included (flexible: catches "real estate: included", "property included", "includes real estate", etc.)
    real_estate_patterns = [
        r"real estate[:\s\-]*included",
        r"property[:\s\-]*included",
        r"includes real estate",
        r"includes property",
    ]
    data["real_estate"] = any(re.search(pat, text, re.I) for pat in real_estate_patterns)

    # Location (grab from Location: or last line if pattern matches City, State)
    loc_match = re.search(r"Location[:\s]*(.*)", text, re.I)
    if loc_match:
        data["location"] = loc_match.group(1).strip()
    else:
        # fallback: last non-empty line that looks like a city, state
        for line in reversed(lines):
            if re.match(r".*, [A-Z]{2}$", line.strip()):
                data["location"] = line.strip()
                break

    return data


