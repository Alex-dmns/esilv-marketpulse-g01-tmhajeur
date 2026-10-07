from pathlib import Path
import csv
import json


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]

    print("=== MarketPulse ===")
    print()
    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Last price: {instrument_latest['close']} {instrument['currency']}")
    print()
    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Last level: {benchmark_latest['close']}")
    print()
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()
    print("Observations")
    print(f"{instrument['ticker']}: {len(instrument_prices)}")
    print(f"{benchmark['ticker']}: {len(benchmark_prices)}")



if __name__ == "__main__":
    main()



with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
    instruments = json.load(file)

#print(type(instruments))
#print(instruments.keys())


instrument = instruments["instrument"]
benchmark = instruments["benchmark"]


#print(instrument["ticker"])
#print(instrument["name"])
#print(instrument["currency"])

#print(benchmark["ticker"])
#print(benchmark["name"])



def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))

prices = load_prices()

#print(type(prices))
#print(type(prices[0]))
#print(prices[0])




#print(prices[0]["close"])
#print(type(prices[0]["close"]))

close = float(prices[0]["close"])


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]

instrument_prices = filter_prices(
    prices,
    instrument["ticker"],
)

benchmark_prices = filter_prices(
    prices,
    benchmark["ticker"],
)


#print(len(instrument_prices))
#print(len(benchmark_prices))

def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])

'''print(f"{instrument['ticker']} First Close -> {get_first_close(instrument_prices)}")
print(f"{instrument['ticker']} Last Close  -> {get_last_close(instrument_prices)}")
print(f"{benchmark['ticker']} First Close -> {get_first_close(benchmark_prices)}")
print(f"{benchmark['ticker']} Last Close  -> {get_last_close(benchmark_prices)}")'''




def display_market_summary(asset, prices, show_currency=True):
    currency_str = f" {asset['currency']}" if show_currency else ""
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Observations : {len(prices)}")
    print(f"First close : {get_first_close(prices):.2f}{currency_str}")
    print(f"Last close  : {get_last_close(prices):.2f}{currency_str}")


display_market_summary(instrument, instrument_prices)
display_market_summary(benchmark, benchmark_prices, show_currency=False)