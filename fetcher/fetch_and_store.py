import os
import requests
import logging
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from time import sleep

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SYMBOL = os.getenv("SYMBOL", "GOOG")

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ALPHA_URL = "https://www.alphavantage.co/query"


# -------------------------
# PARSER FOR FREE ENDPOINT
# -------------------------
def parse_daily(json_data):
    key = None
    for k in json_data.keys():
        if "Time Series" in k:
            key = k
            break
    
    if not key:
        raise ValueError("Unexpected format: No 'Time Series' key found.")

    ts = json_data[key]
    rows = []

    for date_str, metrics in ts.items():
        rows.append({
            "symbol": json_data.get("Meta Data", {}).get("2. Symbol", SYMBOL),
            "date": date_str,
            "open": float(metrics.get("1. open", "0") or 0),
            "high": float(metrics.get("2. high", "0") or 0),
            "low": float(metrics.get("3. low", "0") or 0),
            "close": float(metrics.get("4. close", "0") or 0),
            "adjusted_close": float(metrics.get("4. close", "0") or 0),   # since free API does not provide adjusted close
            "volume": int(metrics.get("5. volume", "0") or 0),
        })

    return rows


# -------------------------
# UPSERT DATA TO DATABASE
# -------------------------
def upsert_rows(conn, rows):
    if not rows:
        return 0

    with conn.cursor() as cur:
        query = """
        INSERT INTO stock_data (symbol, date, open, high, low, close, adjusted_close, volume)
        VALUES %s
        ON CONFLICT (symbol, date)
        DO UPDATE SET 
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            adjusted_close = EXCLUDED.adjusted_close,
            volume = EXCLUDED.volume;
        """

        tuples = [
            (r["symbol"], r["date"], r["open"], r["high"], r["low"],
             r["close"], r["adjusted_close"], r["volume"])
            for r in rows
        ]

        execute_values(cur, query, tuples)

    conn.commit()
    return len(rows)


# -------------------------
# FETCH → PARSE → STORE
# -------------------------
def fetch_and_store(logger=None):
    logger = logger or logging

    if not API_KEY:
        logger.error("API key missing. Set ALPHA_VANTAGE_API_KEY in .env")
        return {"status": "error", "reason": "no_api_key"}

    params = {
        "function": "TIME_SERIES_DAILY",   # fixed - free endpoint
        "symbol": SYMBOL,
        "apikey": API_KEY,
        "outputsize": "compact",
    }

    # -------------------------
    # RETRY LOOP (handles slow API)
    # -------------------------
    for attempt in range(3):
        try:
            logger.info(f"Fetching URL: {ALPHA_URL} with params {params}")
            resp = requests.get(ALPHA_URL, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            logger.info(f"API response keys: {list(data.keys())}")
            break
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            sleep(2)
    else:
        return {"status": "error", "reason": "fetch_failed"}

    # -------------------------
    # HANDLE API ERRORS
    # -------------------------
    if "Error Message" in data:
        logger.error(f"API Error: {data['Error Message']}")
        return {"status": "error", "api_error": data["Error Message"]}

    if "Note" in data:
        logger.warning(f"API Notice: {data['Note']}")
        return {"status": "rate_limited", "message": data["Note"]}

    # -------------------------
    # PARSE JSON
    # -------------------------
    try:
        rows = parse_daily(data)
    except Exception as e:
        logger.exception("Parsing failed: %s", e)
        return {"status": "error", "parse_failed": str(e)}

    # -------------------------
    # DATABASE STORE
    # -------------------------
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
    except Exception as e:
        logger.exception("DB connection failed: %s", e)
        return {"status": "error", "db_connection_failed": str(e)}

    try:
        count = upsert_rows(conn, rows)
        logger.info(f"Upserted {count} rows for {SYMBOL}")
        conn.close()
        return {"status": "success", "inserted": count}
    except Exception as e:
        logger.exception("Upsert failed: %s", e)
        conn.close()
        return {"status": "error", "upsert_failed": str(e)}
