# List of tickers that fail aka return IndexError
# SALM
# APP
# JFR
# RBA
# GB
# ALLY
# SRI
# BOOT
# AUBAP
# NYMTP

import pandas as pd
import lxml
from lxml import html
import requests



ticker = 'NXR'

stats_site = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker

page = requests.get(stats_site)
tree = html.fromstring(page.content)
market_cap_nodes = tree.xpath("//td[@data-test='MARKET_CAP-value']/span/text()")[0]
print(market_cap_nodes)
