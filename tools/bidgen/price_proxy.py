#!/usr/bin/env python3
"""
Price Proxy Server for Bid Generator
Uses Bing Shopping to find real product prices from multiple retailers.

Run:  python price_proxy.py
Serves on http://localhost:8081

Zero external dependencies — uses only Python standard library.
"""

import http.server
import json
import urllib.request
import urllib.parse
import re
import ssl
import html as html_mod

# ---------------------------------------------------------------------------
# CORS-enabled JSON handler
# ---------------------------------------------------------------------------
class ProxyHandler(http.server.BaseHTTPRequestHandler):

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def log_message(self, fmt, *args):
        print(f"[proxy] {args[0]}")

    # ----- routes ----------------------------------------------------------
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)

        if parsed.path == '/status':
            self._json({
                'status': 'running',
                'sources': ['bing-shopping'],
                'stores': ['menards', 'home depot', 'lowes', 'amazon', 'all retailers']
            })

        elif parsed.path == '/search':
            query = qs.get('q', [''])[0].strip()
            store = qs.get('store', [''])[0].strip().lower()
            if not query:
                self._json({'error': 'Missing ?q= parameter'}, 400)
                return
            print(f"[search] q={query!r} store={store!r}")
            results = search_bing_shopping(query, store)
            self._json({
                'query': query,
                'store': store or 'all',
                'source': 'bing-shopping',
                'count': len(results),
                'results': results
            })

        else:
            self._json({'error': 'Use /search?q=...&store=menards or /status'}, 404)


# ---------------------------------------------------------------------------
# Shared fetch helper
# ---------------------------------------------------------------------------
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'identity',
    'DNT': '1',
}

_ctx = ssl.create_default_context()


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, context=_ctx, timeout=20) as resp:
        return resp.read().decode('utf-8', errors='replace')


# ---------------------------------------------------------------------------
# Bing Shopping scraper  (confirmed working — returns product cards with
# .br-offTtl span[title], .br-price, .br-offSlrTxt)
# ---------------------------------------------------------------------------
def search_bing_shopping(query, store_filter=''):
    """
    Search Bing Shopping for products.
    If store_filter is set (e.g. 'menards'), append it to the query so
    Bing prioritises that retailer's listings.
    """
    search_q = query
    if store_filter and store_filter not in ('all', 'any', ''):
        search_q = f'{query} {store_filter}'

    url = 'https://www.bing.com/shop?q=' + urllib.parse.quote_plus(search_q)

    try:
        raw = fetch(url)
    except Exception as e:
        return [{'desc': f'[Bing Shopping error: {e}]', 'price': 0, 'source': 'error'}]

    results = []

    # ---- Primary: parse product cards ----
    # Structure (confirmed from live HTML):
    #   <div class="br-offTtl ..."><span title="FULL PRODUCT NAME">Truncated…</span></div>
    #   <div class="br-price">$XX.XX</div>
    #   <span class="br-offSlrTxt">Store Name</span>
    card_pattern = re.compile(
        r'<span\s+title="([^"]{5,300})"[^>]*>[^<]*</span>\s*</div>'  # product title
        r'.*?'
        r'<div\s+class="br-price">\s*\$([\d,]+\.?\d*)\s*</div>'       # price
        r'.*?'
        r'(?:<span\s+class="br-offSlrTxt">([^<]{2,60})</span>)?',     # seller (optional)
        re.S
    )

    seen = set()
    for m in card_pattern.finditer(raw):
        name = html_mod.unescape(m.group(1)).strip()
        price_str = m.group(2).replace(',', '')
        seller = html_mod.unescape(m.group(3)).strip() if m.group(3) else ''

        try:
            price = float(price_str)
        except ValueError:
            continue

        if price < 0.01 or price > 100000:
            continue

        # De-duplicate by name
        key = name.lower()[:60]
        if key in seen:
            continue
        seen.add(key)

        results.append({
            'desc': name,
            'price': price,
            'source': seller or 'Bing Shopping',
        })

    # ---- Fallback: broader regex if primary found < 3 ----
    if len(results) < 3:
        # Look for any title="..." followed by a $price within 1000 chars
        fallback_pat = re.compile(
            r'title="([^"]{10,200})"'
            r'(?:(?!title=").){0,800}'
            r'\$([\d,]+\.\d{2})',
            re.S
        )
        for m in fallback_pat.finditer(raw):
            name = html_mod.unescape(m.group(1)).strip()
            price_str = m.group(2).replace(',', '')
            # Filter navigation/junk titles
            if any(x in name.lower() for x in ['search for', 'sign in', 'menu', 'filter', 'sort']):
                continue
            try:
                price = float(price_str)
            except ValueError:
                continue
            if price < 0.50 or price > 100000:
                continue
            key = name.lower()[:60]
            if key in seen:
                continue
            seen.add(key)
            results.append({
                'desc': name,
                'price': price,
                'source': 'Bing Shopping',
            })

    # Apply store filter to results if specified
    if store_filter and store_filter not in ('all', 'any', ''):
        sf = store_filter.lower()
        filtered = [r for r in results if sf in r.get('source', '').lower()]
        # If filter matches some, use those; otherwise return all
        if filtered:
            results = filtered

    return results[:25]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    PORT = 8081
    server = http.server.HTTPServer(('127.0.0.1', PORT), ProxyHandler)
    print(f"""
+================================================+
|  Price Proxy Server -- Bid Generator            |
|  Running on http://localhost:{PORT}                |
|                                                 |
|  Powered by Bing Shopping                       |
|  Endpoints:                                     |
|    GET /search?q=wax+ring                       |
|    GET /search?q=vinyl+plank&store=menards      |
|    GET /search?q=romex+wire&store=home+depot    |
|    GET /status                                  |
|                                                 |
|  Press Ctrl+C to stop                           |
+================================================+
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nProxy stopped.")
        server.server_close()
