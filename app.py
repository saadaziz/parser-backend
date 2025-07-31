from flask import Flask, request, jsonify
from parser import parse_listing
from models import ParsedListing, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from logging_utils import logger
import os

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///parser.db")

app = Flask(__name__)
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def parse_listing(text):
    import re

    data = {}

    # Business Name (assume first non-empty line)
    lines = text.strip().split('\n')
    if lines:
        data["business_name"] = lines[0].strip()

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

    # Real Estate Included
    real_estate = True if re.search(r"real estate.*included", text, re.I) else False
    data["real_estate"] = real_estate

    # Location (grab from Location: or last line if pattern matches City, State)
    loc_match = re.search(r"Location[:\s]*(.*)", text, re.I)
    if loc_match:
        data["location"] = loc_match.group(1).strip()
    else:
        # fallback: last line
        if len(lines) > 1:
            possible_loc = lines[-1].strip()
            if re.match(r".*, [A-Z]{2}$", possible_loc):
                data["location"] = possible_loc

    return data


@app.route("/ping", methods=["GET"])
def ping():
    logger.info("Health check /ping hit")
    return jsonify({"status": "ok"})

@app.route("/parse", methods=["POST"])
def parse():
    req_data = request.get_json(force=True)
    logger.info(f"/parse called with payload: {req_data}")
    text = req_data.get("text", "")
    parsed = parse_listing(text)
    # Save to DB
    session = Session()
    parsed_json = json.dumps(parsed)
    obj = ParsedListing(raw_text=text, parsed_json=parsed_json)
    session.add(obj)
    session.commit()
    logger.info("Parsed listing saved: %s", json.dumps({
        "id": obj.id,
        "raw_text": obj.raw_text,
        "parsed_json": obj.parsed_json,
        "created_at": str(obj.created_at)
    })) 
    
    return jsonify({"parsed": parsed, "id": obj.id})

if __name__ == "__main__":
    test = """Super Prime Branded Gas Station, Portland, OR
Asking Price: $2,100,000
Gross Revenue: $4,800,000
Cash Flow (SDE): $325,000
Real Estate: Included
Location: Portland, OR
"""
    print(parse_listing(test))