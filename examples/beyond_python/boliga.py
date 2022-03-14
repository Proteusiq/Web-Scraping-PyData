# Hello, Python web scraping
import requests
from pprint import pprint as inspect


# make api call to boliga
params = dict(pageSize=50, includeds=1, sort="daysForSale-a")
uri = "https://api.boliga.dk/api/v2/search/results"


try:
    response = requests.get(url=uri, params=params)
    json_body = response.json()
    error = None

except requests.exceptions.JSONDecodeError as e:
    error = e.__class__.__name__

if error != None:
    print(f"We got issue {error}")
else:
    inspect(json_body)
