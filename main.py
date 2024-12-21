import requests
from datetime import datetime, timedelta
from parameters import *

browser_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": f"Bearer {BEARER_TOKEN}",
    "content-type": "application/json",
    "origin": "https://www.finanzfluss.de",
    "priority": "u=1, i",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    **browser_headers
    }

def generate_custom_dates(start_date, end_date, interval_value, day_of_execution):
    start = datetime.strptime(start_date, "%d.%m.%Y")
    end = datetime.strptime(end_date, "%d.%m.%Y")
    
    dates = []
    current = start.replace(day=day_of_execution)
    
    while current <= end:
        if current.day == day_of_execution:
            if current.weekday() in [5, 6]:
                current = current + timedelta(days=7-current.weekday())
            dates.append(current.strftime("%Y-%m-%d"))
        
        for _ in range(interval_value):
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
        current = current.replace(day=day_of_execution)
    
    return dates

def search_symbol(isin):
    url1 = f"https://wealthapi.eu/api/v2/symbols?search={isin}"
    r1 = requests.get(url=url1, headers=headers).json()
    if not r1['symbols']:
        _exit(f"Konnte nichts für ISIN {isin} finden")
    search_info = r1['symbols'][0]
    url2 = f"https://wealthapi.eu/api/v2/quotes?securityId={isin}&quoteProvider={search_info['quoteProvider']}"
    r2 = requests.get(url=url2, headers=headers).json()
    search_info = {**search_info, **r2['quotes'][0]}
    return search_info

def get_quote(date, ticker):
    url = f"https://wealthapi.eu/api/v1/historicQuotes/lookup?includeIndexes=false&tickerSymbol={ticker}&quoteProvider=tte&quoteCurrency=EUR&convertToCurrency=EUR&from={date}&to={date}"
    response = requests.get(url, headers=browser_headers)
    historic_quotes = response.json()['historicQuotes']
    first_key = list(historic_quotes.keys())[0]
    return historic_quotes[first_key][0]['value']

def add_transactions(dates_list, ticker_info):
    for date in dates_list:
        print('-'*50)
        print("Füge Transaktion für Datum hinzu:", date)
        try:
            quote = get_quote(date, ticker_info['id'])
        except IndexError:
            print("Kein Kurs für dieses Datum verfügbar")
            continue
        url = "https://wealthapi.eu/api/v1/bookings"

        payload = {
            "accountId": ACCOUNT_ID,
            "performBackgroundTransactionSync": False,
            "autoAssignQuotes": False,
            "createDepotSynchronizationLog": False,
            "createOrUpdateInvestmentParamsList": [
                {
                    "accountId": ACCOUNT_ID,
                    "type": ticker_info['type'],
                    "tickerSymbol": ticker_info['id'],
                    "currency": "EUR",
                    "quoteProvider": ticker_info['quoteProvider'],
                    "quoteCurrency": ticker_info['currency'],
                    "name": ticker_info['name'],
                    "isin": ticker_info['isin'],
                    "createOrUpdateBookingParamsList": [
                        {
                            "numberOfLots": float(INVESTMENT_PER_INTERVAL)/float(quote),
                            "securityPrice": float(quote),
                            "entryQuote": float(quote),
                            "date": date,
                            "exchangeRate": 1,
                            "type": "buy",
                            "commission": 0,
                            "taxAmount": 0,
                            "expensesInEur": True,
                            "commentVisibility": "nobody",
                            "notifyFriends": False,
                        }
                    ],
                }
            ],
        }
        response = requests.post(url, headers=headers, json=payload)
        print("Status Code:", response.status_code)


def _exit(msg):
    print(msg)
    exit()

if __name__ == "__main__":
    try:
        float(INVESTMENT_PER_INTERVAL)
    except ValueError:
        _exit('INVESTMENT_PER_INTERVAL muss eine Zahl sein.')
    try:
        datetime.strptime(START_DATE, "%d.%m.%Y")
        start_date = START_DATE
    except ValueError:
        _exit("START_DATE muss im Format dd.mm.yyyy sein")
    
    if END_DATE == "":
        end_date = datetime.today().strftime("%d.%m.%Y")
    else:
        try:
            datetime.strptime(END_DATE, "%d.%m.%Y")
            end_date = END_DATE
        except ValueError:
            _exit("END_DATE muss im Format dd.mm.yyyy sein")
    
    try:
        interval_value = int(INTERVAL_VALUE)
        day_of_execution = int(DAY_OF_EXECUTION)
    except ValueError:
        _exit('INTERVAL_VALUE und DAY_OF_EXECUTION müssen ganze Zahlen sein (z.B. "1")')

    dates_list = generate_custom_dates(start_date, end_date, interval_value, day_of_execution)
    print("Für folgende Daten werden Transaktionen hinzugefügt:")
    print(dates_list)
    if input("Weiter mit Enter: ") != "":
        _exit("Beende...")
    print(f"Suche {ISIN}...")
    info = search_symbol(ISIN)
    add_transactions(dates_list, info)
    print("Transaktionen erfolgreich hinzugefügt!")
