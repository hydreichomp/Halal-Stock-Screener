# Halal-Stock-Screener

Basics of using this screener:

First, run find_halal_stocks/filterstocks_new.py to check every ticker on Yahoo Finance for Shariah compliance.
Passing tickers are stored by Market Cap in find_halal_stocks/halal_tickers.txt
Note that although I wish I could guarantee I catch everything, this script is not robust enough i.e.
some tickers that should be halal will get filtered out or some tickers that are deemed halal are actually haram.
There are many, many reasons this could occur (a company financials just became good in the most recent quarter, but have not been compliant over the past year;
the filter criteria for haram words in a company's business description is too harsh or not harsh enough;
there are haram businesses that have not been filtered out;
etc)
Nevertheless, IA, the list generated is a pretty good and usable set of companies to look into

Second, run find_wsb_dd/filterwsb.py to check the most recent 1000 DD posts on WSB, check each ticker mentioned in the title,
check if such ticker is in the halal list above, and then aggregate all tickers and correponding DD posts and email them to yourself.
For the email part, make sure to open the code and replace my email information with yours. The ports are valid for Yahoo - a quick
search shows you what ports will work for your email service. Also, you need to turn on two factor authentication to get a special
code that allows your personal email to recognize and receive emails being sent like this.
This also can give false negatives/positives with the wrong ticker picked out from the title for instance, but its pretty accurate 95% of the time.

I actualy have this run once a week on Sundays at 8:00 pm. To set this up on Mac, do the following:
I used LaunchAgents and from the little I found out, it looks like these run better as root. So, copy
filterwsb.py and halal_tickers.txt to /Applications. Make your own version of com.hasanashqeen.wsb-dd.plist and place it
in /Library/LaunchAgents/. Open the plist and also make the "Standard" diretories referenced in /tmp. These are very useful for debugging.
I would like to give credit for this /tmp/ directory idea in the plist but I forget now where I found it.
It took quite a long time and much frustation to figure this next part out, but credit goes to
https://joelsenders.wordpress.com/2019/03/14/dear-launchctl-were-all-using-you-wrong/
Run "launchctl bootstrap gui/$userID /Library/LaunchAgents/com.hasanashqeen.wsb-dd.plist"
and it should start working once a week on Sundays. You can change that by modifying the values at the end of the plist.
If you ever want to stop this automated task, just run "launchctl bootout gui/$userID /Library/LaunchAgents/some.company.plist"


The files not referenced are either extra stores of data (text files) or just trial/older versions of the above, such as the
directory send_email. I also apologize for the code - it's mostly clear but still a lot of notes for things to add and areas I
should clean up.
