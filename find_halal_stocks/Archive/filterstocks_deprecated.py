# Filters all stock tickers available in Yahoo Finance through the yahoo_fin API
# based on Shariah principles

# *** Was using yahoo_fin API to get Market Cap, but that call was causing multiple IndexError failures. 
#     Through pdb, realized that the problem was that the API was checking for Trailing P/E in the tables
#     returned by pandas.read_html in get_stats_valuation. If Trailing P/E was Nan, it always failed. 
#     We don't even care about Trailing P/E or all the other data, just want Market Cap, so a custom function
#     was made.
import yahoo_fin.stock_info as si
import math
import pandas as pd
import time
from urllib.error import HTTPError
import pickle
import urllib
import os

# To run pdb, run "python3 -m pdb filterstocks.py"

#========================================================================================================================
#======================================================================================================= CONSTANTS
#========================================================================================================================
ONE_MILLION = 1000000.0
ONE_BILLION = 1000000000.0
ONE_TRILLION = 1000000000000.0
HALAL_CASH_PERC = 33.3
HALAL_DEBT_PERC = 33.3
HALAL_RECEIVABLES_PERC = 49.0

MAX_TRIES = 1
WAIT_TIME = 10

#========================================================================================================================
#======================================================================================================= HELPER FUNCTIONS
#========================================================================================================================

num_tries = 0 # Global variable to check number of times API errors

# Converts strings such as "2T" and "600B" to the actual numbers
def Convert_To_Number(str_with_suffix):
   # Million
   if (str_with_suffix.endswith("M")):
      return (float(str_with_suffix[:-1]) * ONE_MILLION)
   # Billion
   if (str_with_suffix.endswith("B")):
      return (float(str_with_suffix[:-1]) * ONE_BILLION)
   # Trillion
   if (str_with_suffix.endswith("T")):
      return (float(str_with_suffix[:-1]) * ONE_TRILLION)
   return float(str_with_suffix)
# End Convert_To_Number

# Obtains Market Capitalization from a DataFrame balance sheet
# If Market Cap is NaN, then do not save this ticker
# NOTE: Index 0 means only using most recent yearly data available
def Get_Market_Cap(stats_valuation):
   market_cap = stats_valuation.iat[0,1]
   if (isinstance(market_cap, str)):
      if (stats_valuation.iat[0,1].upper() != "NAN"):
         return stats_valuation.iat[0,1]
      else:
         return None
   elif (isinstance(market_cap, float)):
      if not(math.isnan(stats_valuation.iat[0,1])):
         return str(stats_valuation.iat[0,1])
      else:
         return None
# End Get_Market_Cap

# Obtains total cash from a DataFrame balance sheet
# NOTE: Index 0 means only using most recent yearly data available
def Get_Cash(balance_sheet):
   cash = 0
   rows = balance_sheet.index
   if ("cash" in rows):
      if not(math.isnan(balance_sheet.loc["cash"][0])):
         cash += balance_sheet.loc["cash"][0]
   if ("shortTermInvestments" in rows):
      if not(math.isnan(balance_sheet.loc["shortTermInvestments"][0])):
         cash += balance_sheet.loc["shortTermInvestments"][0]
   if ("longTermInvestments" in rows):
      if not(math.isnan(balance_sheet.loc["longTermInvestments"][0])):
         cash += balance_sheet.loc["longTermInvestments"][0]
   return cash
# End Get_Cash

# Obtains total debt from a DataFrame balance sheet
# NOTE: Index 0 means only using most recent yearly data available
def Get_Debt(balance_sheet):
   debt = 0
   rows = balance_sheet.index
   if ("shortLongTermDebt" in rows):
      if not(math.isnan(balance_sheet.loc["shortLongTermDebt"][0])):
         debt += balance_sheet.loc["shortLongTermDebt"][0]
   if ("longTermDebt" in rows):
      if not(math.isnan(balance_sheet.loc["longTermDebt"][0])):
         debt += balance_sheet.loc["longTermDebt"][0]
   return debt
# End Get_Debt

# Obtains total receivables from a DataFrame balance sheet
# NOTE: RECEIVABLES INCLUDES MORE THAN ACCOUNTS RECEIVABLES WHICH IS REALLY THE VALUE THAT MATTERS
# NOTE: Index 0 means only using most recent yearly data available
def Get_Receivables(balance_sheet):
   receivables = 0
   rows = balance_sheet.index
   if ("netReceivables" in rows):
      if not(math.isnan(balance_sheet.loc["netReceivables"][0])):
         receivables += balance_sheet.loc["netReceivables"][0]
   return receivables
# End Get_Receivables

# Obtains desired ticker data from Yahoo Finance
# Returns a dictionary with the following format (only the right side):
# <ticker>: {"Market Cap": val (with suffix), "Market Cap (Full)": val,
#            "Cash": val, "Debt": val, "Receivables: val,
#            "Cash (%)": percentage, "Debt (%)": percentage, "Receivables (%)": percentage}
# Retuns None if API call fails
def Get_Ticker_Data(ticker):
   
   global num_tries
   if (num_tries == MAX_TRIES):
      print("MAX TRIES HIT, EXITING")
      return None
      # max_tries is reset in Executive
   num_tries = num_tries + 1
   
   print(ticker)

   # Ping API to obtain data sets in Pandas DataFrame format
   try:
      balance_sheet = si.get_balance_sheet(ticker)
   except KeyError:
      # If nothing available, then do not save this ticker
      return None
   except TypeError:
      # Internal API logic failed, do not save this ticker
      return None
   except IndexError:
      # Raised because too many calls to API. Wait 10 seconds and try again
      print('IndexError for', ticker)
      #time.sleep(WAIT_TIME)
      return Get_Ticker_Data(ticker)
   except urllib.error.HTTPError as err:
      if (err.code == 503): # Service Unavailable error
         # Raised because too many calls to API. Wait 10 seconds and try again
         print('HTTP Error Service Unavailable for', ticker)
         #time.sleep(WAIT_TIME)
         return Get_Ticker_Data(ticker)

   try:
      stats_valuation = si.get_stats_valuation(ticker)
   except KeyError:
      return None
   except TypeError:
      return None
   except IndexError:
      print('IndexError for', ticker)
      #time.sleep(WAIT_TIME)
      return Get_Ticker_Data(ticker)
   except urllib.error.HTTPError as err:
      if (err.code == 503):
         print('HTTP Error Service Unavailable for', ticker)
         #time.sleep(WAIT_TIME)
         return Get_Ticker_Data(ticker)
 
   num_tries = 0

   # Obtain desired data from DataFrames
   market_cap = Get_Market_Cap(stats_valuation)
   if (market_cap == None):
      # If Market Cap does not exist, then do not save this ticker
      return None
   cash = Get_Cash(balance_sheet)
   debt = Get_Debt(balance_sheet)
   receivables = Get_Receivables(balance_sheet)

   # Calculations on desired data
   market_cap_full = Convert_To_Number(market_cap)
   cash_perc = round(cash / market_cap_full * 1000.0) / 10.0 # Percentage to the tenths
   debt_perc = round(debt / market_cap_full * 1000.0) / 10.0
   receivables_perc = round(receivables / market_cap_full * 1000.0) / 10.0

   # Return dictionary with desired format
   ticker_data = {}
   ticker_data["Market_Cap"] = market_cap
   ticker_data["Market_Cap_(Full)"] = market_cap_full
   ticker_data["Cash"] = cash
   ticker_data["Debt"] = debt
   ticker_data["Receivables"] = receivables
   ticker_data["Cash_(%)"] = cash_perc
   ticker_data["Debt_(%)"] = debt_perc
   ticker_data["Receivables_(%)"] = receivables_perc
   return ticker_data
# End Get_Ticker_Data

# Save off current dictionary of all tickers for efficiency
# Not human readable, saved as binary to be loaded later
def Save_Tickers(tickers):
   tickers_file = open('all_tickers.txt', 'wb')
   pickle.dump(tickers, tickers_file)
   tickers_file.close()
# End Save_Tickers

# Load saved off tickers from function above
def Load_Tickers():
   if (os.stat('all_tickers.txt').st_size == 0):
      return {} # Cannot load empty file
 
   saved_tickers = {}
   tickers_file = open('all_tickers.txt', 'rb')
   saved_tickers = pickle.loads(tickers_file.read())
   tickers_file.close()
   return saved_tickers
# End Load_Tickers

# Save off current dictionary of bad tickers for efficiency
# Not human readable, saved as binary to be loaded later
def Save_Bad_Tickers(tickers):
   tickers_file = open('bad_tickers.txt', 'wb')
   pickle.dump(tickers, tickers_file)
   tickers_file.close()
# End Save_Bad_Tickers

# Load saved off tickers from function above
def Load_Bad_Tickers():
   if (os.stat('bad_tickers.txt').st_size == 0):
      return {} # Cannot load empty file
 
   saved_tickers = {}
   tickers_file = open('bad_tickers.txt', 'rb')
   saved_tickers = pickle.loads(tickers_file.read())
   tickers_file.close()
   return saved_tickers
# End Load_Bad_Tickers

# Filters DataFrame of tickers for only Halal stocks
# Returns DataFrame of permissible tickers
# Assumes cash, debt, and receivables percentages are available
def Get_Halal_Tickers(tickers):
   cash_check = tickers[tickers['Cash_(%)'] <= HALAL_CASH_PERC]
   debt_check = cash_check[cash_check['Debt_(%)'] <= HALAL_DEBT_PERC]
   recv_check = debt_check[debt_check['Receivables_(%)'] <= HALAL_RECEIVABLES_PERC]
   return recv_check
# End Get_Halal_Tickers

#========================================================================================================================
#======================================================================================================= EXECUTIVE
#========================================================================================================================

# Open text files for saving data
all_tickers_file = open("all_tickers_readable.txt", "w")
halal_tickers_file = open("halal_tickers.txt", "w")

# Debugging errors
#print(Get_Ticker_Data("ADSK"))

# Nasdaq stocks
nasdaq_list = si.tickers_nasdaq()
print("Tickers in Nasdaq:", len(nasdaq_list))

# S&P 500 stocks
sp500_list = si.tickers_sp500()
print("Tickers in S&P 500:", len(sp500_list))

# Other stocks
other_list = si.tickers_other()
print("Tickers in Other:", len(other_list))

total_tickers = len(nasdaq_list) + len(sp500_list) + len(other_list)
print("Total Tickers:", total_tickers)

# Loop through all tickers and store in a dictionary
# <ticker>: {"Market_Cap": val (with suffix), "Market_Cap_(Full)": val,
#            "Cash": val, "Debt": val, "Receivables: val,
#            "Cash_(%)": percentage, "Debt_(%)": percentage, "Receivables_(%)": percentage}
all_tickers = Load_Tickers() # Contains all <ticker>, load previously found ones
print("Tickers loaded:", len(all_tickers))

bad_tickers = Load_Bad_Tickers()
print("Tickers rejected:", len(bad_tickers))

# Concatenate all tickers
tickers_list = nasdaq_list + sp500_list + other_list
tickers_list.remove('')

# Only keep all tickers not found yet
all_tickers_list = list(all_tickers.keys())
tickers_list = set(tickers_list).difference(all_tickers_list)
bad_tickers_list = list(bad_tickers.keys())
tickers_list = set(tickers_list).difference(bad_tickers_list)
print("Tickers left:", len(tickers_list))

failed_tickers = []
for ticker in tickers_list:
   #time.sleep(WAIT_TIME)
   ticker_data = Get_Ticker_Data(ticker)
   if (ticker_data != None):
      all_tickers_file.write(ticker + ' : ' + str(ticker_data) + '\n') # Save data to text file
      all_tickers[ticker] = ticker_data
      Save_Tickers(all_tickers)
   else:
      if (num_tries == MAX_TRIES):
         num_tries = 0
         failed_tickers.append(ticker)
         continue
      else:
         bad_tickers[ticker] = None
         Save_Bad_Tickers(bad_tickers)

# These tickers had some type of error above
# Now, only exit once they all have been checked in some way
print("=============================== CHECKING FAILED TICKERS")
while (len(failed_tickers) > 0):
   for ticker in failed_tickers:
      ticker_data = Get_Ticker_Data(ticker)
      if (ticker_data != None):
         all_tickers_file.write(ticker + ' : ' + str(ticker_data) + '\n') # Save data to text file
         all_tickers[ticker] = ticker_data
         Save_Tickers(all_tickers)
         failed_tickers.remove(ticker)
         print("FAILED TICKER REMOVED")
      else:
         if (num_tries == MAX_TRIES):
            num_tries = 0
            continue
         else:
            bad_tickers[ticker] = None
            Save_Bad_Tickers(bad_tickers)
            failed_tickers.remove(ticker)
            print("FAILED TICKER REMOVED")
   
# Print all tickers as rows, sorted by Market Cap
all_tickers_df = pd.DataFrame(all_tickers).transpose().sort_values(by = "Market_Cap_(Full)").iloc[::-1]
# Filter for Halal stocks
halal_tickers = Get_Halal_Tickers(all_tickers_df)
print(halal_tickers)

# Save halal tickers to text file
halal_tickers_file.write(halal_tickers.to_string())

# Close text files
all_tickers_file.close()
halal_tickers_file.close()
