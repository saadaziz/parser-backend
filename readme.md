
# Parser-Backend (MVP Gas Station Listing Parser)

A microservice for parsing business-for-sale listing text into structured data.\
Focus: Asset-light, modern Python (Flask), RESTful API, SQLAlchemy, and clear logging.

## Features

- **REST API:** `/ping` (health check) and `/parse` (POST listing text, get extracted fields)
- **Structured Output:** Extracts business name, asking price, revenue, SDE/cash flow, real estate flag, location, etc.
- **Database Persistence:** Stores parsed result, raw text, and timestamp in SQLite (easy to upgrade later)
- **Dual Logging:** Logs to both `stderr.log` and stderr (see `logging_utils.py`)
- **Extensible Parser:** RegEx-based field extraction, schema-driven, ready for future NLP or ML upgrades
- **Minimal, testable design:** Easy to unit test and iterate field patterns

---

## Quickstart

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/parser-backend.git
cd parser-backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Set up your environment:

- Edit `.env` as needed (for custom `DATABASE_URL`, etc).

### 2. Run Locally

```bash
python app.py
# App runs at http://localhost:5001
```

### 3. Run Tests

```bash
python test_parser.py
```

---

## REST API Usage

### Health Check

```bash
curl https://aurorahours.com/parser-backend/ping
# Response: {"status": "ok"}
```

### Parse a Listing (cURL)

```bash
curl -X POST "https://aurorahours.com/parser-backend/parse"   -H "Content-Type: application/json"   -d '{"text": "Super Prime Branded Gas Station, Portland, OR\nAsking Price: $2,100,000\nGross Revenue: $4,800,000\nCash Flow (SDE): $325,000\nReal Estate: Included\nLocation: Portland, OR"}'
```

### Parse a Listing (PowerShell)

```powershell
$listing = @"
Super Prime Branded Gas Station, Portland, OR
Asking Price: `$2,100,000
Gross Revenue: `$4,800,000
Cash Flow (SDE): `$325,000
Real Estate: Included
Location: Portland, OR
"@
$body = @{ text = $listing } | ConvertTo-Json
Invoke-RestMethod -Uri "https://aurorahours.com/parser-backend/parse" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

```

```powershell
$result = Invoke-RestMethod -Uri "https://aurorahours.com/parser-backend/parse" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

# Pretty print the result as JSON:
$result | ConvertTo-Json -Depth 4
```

**Typical JSON Response:**

```json
{
  "id": 16,
  "parsed": {
    "business_name": "Super Prime Branded Gas Station, Portland, OR",
    "asking_price": 2100000,
    "revenue": 4800000,
    "sde": 325000,
    "real_estate": true,
    "location": "Portland, OR"
  }
}
```

---

## Extending the Parser

Parsing logic is driven by regular expressions and can be evolved to use spaCy, LLMs, or custom field schemas (see `parser.py`).

- **To add a new field:**
  - Add a new regex/pattern to the schema in `parser.py`.
  - Write a post-processor if special cleanup or logic is needed.
- **To test field extraction:**
  - Edit `test_parser.py` with new/edge case samples, then run: `python test_parser.py`

---

## Logging

- All requests and parse events are logged to both `stderr.log` and stderr. Configure in `logging_utils.py`.

---

## Database

- Default: SQLite (`parser.db`). Set `DATABASE_URL` in `.env` for Postgres, MySQL, etc.

---

## License

MIT License. See `LICENSE` file for details.

---

## Author

Saad Aziz\
[saadaziz.com](https://saadaziz.com)\
*Questions, feature requests, or investor inquiries welcome!*
