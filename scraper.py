from playwright.sync_api import sync_playwright
from datetime import datetime
import csv, time

CSV_FILE = "precios.csv"
PRICE_SELECTOR = "div.e2GB-price-text"

def _parse_price(text):
    if not text:
        return None
    clean = text.replace("$", "").replace("COP", "").replace(",", "").replace(".", "").strip()
    digits = "".join(ch for ch in clean if ch.isdigit())
    if not digits:
        return None
    # treat as integer of currency (no decimals)
    return int(digits)

def get_precio_kayak(origen, destino, salida, regreso):
    url = f"https://www.kayak.com.co/flights/{origen}-{destino}/{salida}/{regreso}?sort=bestflight_a"
    prices = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page()
            page.goto(url, timeout=60000)
            # wait up to 20s for prices to appear
            try:
                page.wait_for_selector(PRICE_SELECTOR, timeout=20000)
            except:
                pass
            # small pause to let results load
            time.sleep(2)
            elements = page.query_selector_all(PRICE_SELECTOR)
            for el in elements:
                try:
                    txt = el.inner_text()
                except:
                    txt = None
                val = _parse_price(txt)
                if val:
                    prices.append(val)
            browser.close()
    except Exception as e:
        print("Error scraping:", e)
    if not prices:
        precio_text = "No encontrado"
        precio_val = None
    else:
        precio_val = min(prices)
        precio_text = f"{precio_val}"
    # guardar en CSV
    try:
        with open(CSV_FILE, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), origen, destino, salida, regreso, precio_text])
    except Exception as e:
        print("Error saving CSV:", e)
    return precio_val
