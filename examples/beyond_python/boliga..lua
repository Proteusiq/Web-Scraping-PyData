-- Hello, Lua web scraping
local requests = require('requests')
local inspect = require('inspect')


-- make api call to boliga
local params = {pageSize=50,includeds=1, sort="daysForSale-a"}
local uri = "https://api.boliga.dk/api/v2/search/results"


local response = requests.get{url=uri, params=params}
local json_body, error = response.json()

if error ~= nil then
    print("We got issues " .. error)
else
    print(inspect(json_body))
end
