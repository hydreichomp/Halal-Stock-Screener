import praw
import pandas as pd
import re
import os

# For sending email
import collections
from datetime import date
import smtplib
from getpass import getpass
from email.mime.text import MIMEText

# Create a reddit connection
reddit = praw.Reddit(
              client_id = "u0eeGBimucyrkA",
              client_secret = "eGrpPOybs7xTSdIUL3rbzS-VlTFLhQ",
	      user_agent = "hasan_wsb_halal")

# Access WSB
subreddit = reddit.subreddit("wallstreetbets")

# Filter out shorts and puts. Look at text instead of titles
# Store halal stock data in a database
# Want to also remove tickers prematurely by industry they are in like TLRY
# You know, you could also search the text of the submission for haram words like weed or gambling to know if haram
# For tickers that are common words like GOLD and A, look for $GOLD and $A to prevent false positives
# Use rejected_text
# Send it to myself once a week

#=============================================================================================================================
#============================================================================================================ Helper Functions
#=============================================================================================================================

rejected_text = open("rejected_text.txt", "a") # Writes will append to file, not overwrite
halal_tickers_list = []

# Takes words from a submission and returns potential tickers
def Words_To_Tickers(words):
   # Want to first reject any submission that is an anti DD, aka buy shorts or puts
   bad_words = ['puts', 'short'] # Just "put" might be too encompassing, but "puts" definitely means negative outlook
   # Clever solution found in Stack Overflow: convert list of words to literally just a string
   # Then you can check any of the bad_words as a substring check
   # any lets you check multiple items at once
   if any(word in str(words) for word in bad_words):
      return []

   potential_tickers = []
   for word in words:
      # TODO: Also need to look for companies fully listed out like Apple instead of AAPL
      # TODO: Filter out words like "short" or "put"
      if (word.isupper() and len(word) <= 5):
         potential_tickers.append(word)
   return potential_tickers

def Parse_Halal_Tickers():
   halal_df_string = open(os.environ['FIND_HALAL_STOCKS'] + '/halal_tickers.txt', "r")
   halal_df = pd.read_csv(halal_df_string, delim_whitespace = True)
   # The row labels contain the ticker names
   return list(halal_df.index.values)
   
def Get_Halal_Tickers(tickers):
   global halal_tickers_list
   if not(halal_tickers_list):
      halal_tickers_list = Parse_Halal_Tickers()

   # DD is commonly used, so if the ticker of DowDuPont $DD is actually mentioned, it's probably done twice so remove DD once
   # Covers 'DD' passing the initial filtering
   if 'DD' in tickers:
      tickers.remove('DD')
   
   good_tickers = []
   for ticker in tickers:
      if ticker in halal_tickers_list:
         good_tickers.append(ticker)
   return good_tickers

def Title_To_Halal_Ticker(title):
   # Ticker is going to 5 or fewer capital letters juxtaposed together
   # Usually is preceded by $ e.g. $JD
   # If not, then maybe can separate each word by spaces, and choose the longest word with capital letters.
   # Store all titles that are rejected to know where this algorithm fails

   # Submission title (TODO: also text) to words
   # re is Python's regular expressions module
   # Filter(func, list) <==> [i for i in list if func(i)]
   # With None, it is equivalent to [i for i in list if i], hence it removes empty strings
   # [...] matches one of the separators listed inside
   # + skips one more delimiters
   # TODO: Might need to keep - or . for weirdly named tickers
   words = list(filter(None, re.split("[ $.!@%^&*()\-_=+\[\]{}:;<>,?/|\\#]+", title)))
   print(words)
   tickers = Words_To_Tickers(words)
   print(tickers)
   halal_tickers = Get_Halal_Tickers(tickers)
   print(halal_tickers)
   return set(halal_tickers)

def Format_Email_Body(daily_tickers):
   # Send an email with this table format:
   # LIST OF TICKERS FOUND THIS WEEK:
   #
   #    AAPL <title 1 with link>
   #    TSLA <title 1 with link> <title 2 with link>
   #    ...

   # Since the body is interpreted as html due to hyperlinks on each title, use html specific characters
   # instead of text specific characters e.g. <br> for \n
   content = 'LIST OF TICKERS FOUND THIS WEEK:<br><br><table>'

   for ticker in daily_tickers:
      content += '<tr><td>' + ticker + '</td>'
      for post_title in daily_tickers[ticker].keys():
         content += '<td><a href="' + daily_tickers[ticker][post_title] + '">' + post_title + '</a></td>'
      content += '</tr>'
   content += '</table>'

   return content
      
#=============================================================================================================================
#=================================================================================================================== Executive
#=============================================================================================================================


# Get most recent data from WSB and store into list
daily_titles = {}
for submission in reddit.subreddit("wallstreetbets").search('flair:DD', sort='new', limit=1000):
   #print(submission.selftext)
   title_url_pair = {}
   title_url_pair[submission.title] = submission.url
   daily_titles[submission.title] = title_url_pair
   print(submission.title)
print(daily_titles)
print()
print("=================================================================================================================")
print()

# Filter text to now only contain the ticker(s) mentioned
daily_tickers = {}
for title in daily_titles:
   for ticker in Title_To_Halal_Ticker(title):
      # Want to store the list of urls for each ticker
      if (daily_tickers.get(ticker)):
         daily_tickers[ticker].update(daily_titles[title])
      else:
         daily_tickers[ticker] = daily_titles[title]

print()
print()
print()
print("SET OF HALAL TICKERS FOUND")
for ticker in daily_tickers:
   print(ticker)
   print(daily_tickers[ticker])

# Send myself an email with each ticker and associated posts
sender = 'hasanashqeen@yahoo.com'
receiver = 'hasanashqeen@yahoo.com'

# One-time password made in Yahoo account
# Only possible after enabling 2-step verification
password = "dyovtnlytudozfsw"

# Format tickers in alphabetical order with correponding links as a table
content = Format_Email_Body(collections.OrderedDict(sorted(daily_tickers.items())))
print()
print()
print()
print(content)
msg = MIMEText(content, 'html')
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = 'WSB DD Weekly Scrape: ' + date.today().strftime("%m/%d/%y")

smtp_server_name = 'smtp.mail.yahoo.com'
port = '587'

if port == '465':
   server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))
else:
   server = smtplib.SMTP('{}:{}'.format(smtp_server_name, port))
   server.starttls() # This is for secure reason

server.login(sender, password)
server.send_message(msg)
server.quit()


rejected_text.close()
