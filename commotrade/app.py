import yfinance as yf
from flask import Flask, jsonify
from prometheus_client import start_http_server, Gauge
import threading
import time

app = Flask(__name__)

# --- BLOOMBERG-STYLE METRICS ---
PRICE_GAUGE = Gauge('commodity_price', 'Real-time market price', ['symbol'])
SIGNAL_GAUGE = Gauge('trade_signal', '1=BUY, -1=SELL, 0=HOLD', ['symbol'])
LATENCY_GAUGE = Gauge('data_latency_ms', 'Feed latency in ms')

# Global Cache to prevent API rate limits
MARKET_DATA = {
    'CL=F': {'price': 0.0, 'signal': 'HOLD', 'name': 'Crude Oil'},
    'GC=F': {'price': 0.0, 'signal': 'HOLD', 'name': 'Gold'}
}

def fetch_market_data():
    """Background thread to mimic a Real-Time Data Feed"""
    while True:
        start_time = time.time()
        try:
            # Fetch Real Data for Oil and Gold
            tickers = yf.Tickers('CL=F GC=F')
            
            for symbol in ['CL=F', 'GC=F']:
                # Get fast price
                ticker_info = tickers.tickers[symbol].fast_info
                price = ticker_info['last_price']
                prev_close = ticker_info['previous_close']
                
                # --- ANALYTICS (The "Bloomberg" Value) ---
                # Simple algo: If price dropped > 1% below close, BUY.
                change_pct = ((price - prev_close) / prev_close) * 100
                if change_pct < -0.5:
                    signal = "BUY"
                    signal_val = 1
                elif change_pct > 0.5:
                    signal = "SELL"
                    signal_val = -1
                else:
                    signal = "HOLD"
                    signal_val = 0
                
                # Update Cache & Metrics
                MARKET_DATA[symbol]['price'] = round(price, 2)
                MARKET_DATA[symbol]['signal'] = signal
                
                PRICE_GAUGE.labels(symbol=symbol).set(price)
                SIGNAL_GAUGE.labels(symbol=symbol).set(signal_val)
                
            # Measure Latency
            latency = (time.time() - start_time) * 1000
            LATENCY_GAUGE.set(latency)
            
            print(f"Updated: Oil=${MARKET_DATA['CL=F']['price']} Gold=${MARKET_DATA['GC=F']['price']}")
            
        except Exception as e:
            print(f"Data Feed Error: {e}")
            
        time.sleep(10) # Refresh every 10s to be polite to Yahoo

# Start Data Feed in Background
threading.Thread(target=fetch_market_data, daemon=True).start()

@app.route('/terminal')
def terminal_view():
    """Mimics the JSON feed a Frontend Terminal would consume"""
    return jsonify({
        "status": "connected",
        "feed_source": "Yahoo Finance (Simulated Bloomberg Pipe)",
        "market_data": MARKET_DATA,
        "news_ticker": [
            "OPEC meets tomorrow to discuss supply cuts",
            "Gold rallies as inflation data causes concern",
            "Tech stocks volatile ahead of earnings"
        ]
    })

if __name__ == '__main__':
    start_http_server(8000) # Prometheus Scrape Endpoint
    app.run(host='0.0.0.0', port=5000)