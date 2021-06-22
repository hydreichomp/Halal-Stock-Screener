import praw
import pandas as pd
import re
import os

# Create a reddit connection
reddit = praw.Reddit(
              client_id = "u0eeGBimucyrkA",
              client_secret = "eGrpPOybs7xTSdIUL3rbzS-VlTFLhQ",
	      user_agent = "hasan_wsb_halal")

# Access WSB
subreddit = reddit.subreddit("wallstreetbets")

## list for df conversion
#_posts = []
#tmpfile = open("tmp.txt", "w")
## return 20 new posts from wallstreetbets
#new_bets = reddit.subreddit("wallstreetbets").new(limit=30)
## return the important attributes
#for post in new_bets:
#    _posts.append(
#        [
#            post.id,
#            post.author,
#            post.title,
#            post.score,
#            post.selftext,
#            post.created,
#        ]
#    )
#
## create a dataframe
#_posts = pd.DataFrame(
#    _posts,
#    columns=[
#        "id",
#        "author",
#        "title",
#        "score",
#        "selftext",
#        "created",
#    ],
#)
#
#_posts["created"] = pd.to_datetime(_posts["created"], unit="s")
#_posts["created date"] = pd.to_datetime(_posts["created"], unit="s").dt.date
#_posts["created time"] = pd.to_datetime(_posts["created"], unit="s").dt.time
#
#print(_posts)
#tmpfile.write(_posts.to_string())
#tmpfile.close()
#
#print()
#print()
#print()

#for submission in reddit.url("https://www.reddit.com/r/wallstreetbets/top/?f=flair_name%3A%22DD%22&t=week"):
#   print(submission)

# Why even store it tbh, just once a week get the top 1000 posts of the week with the DD flair
# Need to use IFTTT or something similar to do so
# Get the most recent new DD posts, want not 100 but 1000 to make sure not missed any
# Might repeat, so store them by title into a text file using functions from filterstocks.py
# Once we have our list, check them against the halal tickers list
# Once we have that halal list of stocks, want to email that to me
# Provide the ticker and a link to the DD for further research
# One problem though, is you need to grab the text of each submission, and find what ticker is being mentioned
# For now, just focus on the title of the submission and build the rest of the pipeline
# Yet another function, but ideas probably exist online. Also, filter out any short or puts for it
# Attach hyperlinks to original post for all sent tickers
# Store halal stock data in a database
# Want to also remove tickers prematurely by industry they are in like TLRY
# You know, you could also search the text of the submission for haram words like weed or gambling to know if haram

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
      
#=============================================================================================================================
#=================================================================================================================== Executive
#=============================================================================================================================


# Get most recent data from WSB and store into list
daily_titles = []
for submission in reddit.subreddit("wallstreetbets").search('flair:DD', sort='new', limit=1000):
   #print(submission.selftext)
   daily_titles.append(submission.title)
   print(submission.title)
print(daily_titles)
print()
print("=================================================================================================================")
print()

# Filter text to now only contain the ticker(s) mentioned
daily_tickers = set() # Define as set in case of multiple instances of same ticker
for title in daily_titles:
   for ticker in Title_To_Halal_Ticker(title):
      daily_tickers.add(ticker)

print()
print()
print()
print("SET OF HALAL TICKERS FOUND")
print(sorted(daily_tickers))

rejected_text.close()
