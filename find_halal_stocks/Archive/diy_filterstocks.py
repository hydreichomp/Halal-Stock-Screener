import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as ur

# Enter a stock symbol
index = 'AAPL'

# URL link
url_is = 'https://finance.yahoo.com/quote/' + index + '/financials?p=' + index
url_bs = 'https://finance.yahoo.com/quote/' + index + '/balance-sheet?p=' + index
url_cf = 'https://finance.yahoo.com/quote/' + index + '/cash-flow?p=' + index

print(url_bs)

read_data = ur.urlopen(url_bs).read()
print(read_data)
soup_bs = BeautifulSoup(read_data, 'lxml')

print(soup_bs)

print()

text = [entry.text for entry in soup_bs.find_all('div', {'class':'D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined'})]
print(text)

#ls = []
#for l in soup_is.find_all('div'):
#   ls.append(l.string)
#ls = [e for e in ls if e not in ('Operating Expenses', 'Non-recurring Events')] # Exclude these columns
#new_ls = list(filter(None,ls)) # Remove None elements
#
#print(new_ls)
#print(new_ls.index('ttm'))
#
#new_ls = new_ls[15:]
#
#print()
#print(new_ls)
#
#is_data = list(zip(*[iter(new_ls)]*6))
#
#print()
#print(is_data)
