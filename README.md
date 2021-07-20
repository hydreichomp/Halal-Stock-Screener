# Halal-Stock-Screener

# Basics of Using This Screener:

First, run find_halal_stocks/filterstocks_new.py to check every ticker on Yahoo Finance for Shariah compliance.
Passing tickers are stored by Market Cap in find_halal_stocks/halal_tickers.txt.
Note that although I wish I could guarantee I catch everything, this script is not robust enough i.e.
some tickers that should be halal will get filtered out or some tickers that are deemed halal are actually haram.
There are many, many reasons this could occur (a company financials just became good in the most recent quarter, but have not been compliant over the past year;
the filter criteria for haram words in a company's business description is too harsh or not harsh enough;
there are haram businesses that have not been filtered out, etc).
Nevertheless, IA, the list generated is a pretty good and usable set of companies to further research.

Second, run find_wsb_dd/filterwsb.py to check the most recent 1000 DD posts on WSB, check each ticker mentioned in the title,
check if such ticker is in the halal list above, and then aggregate all tickers and correponding DD posts and email them to yourself.
For the email part, make sure to open the code and replace my email information with yours. The ports are valid for Yahoo - a quick
search shows you what ports will work for your email service. Also, you will need to turn on two factor authentication to get a special
code that allows your personal email to recognize and receive emails being sent like this.
Overall, note that this filter too can give false negatives/positives with for instance, the wrong ticker picked out from the post title, but its pretty accurate 95% of the time.

I actualy have filterwsb.py run once a week on Sundays at 8:00 pm. To set this up on Mac, do the following:
I used LaunchAgents and from the little I found out, it looks like these run better as root. So, copy
filterwsb.py and halal_tickers.txt to /Applications. Make your own version of com.hasanashqeen.wsb-dd.plist and place it
in /Library/LaunchAgents/. Open the plist and also make the "Standard" diretories referenced in /tmp. These are very useful for debugging.
I would like to give credit for this /tmp/ directory idea in the plist but I forget now where I found it.
It took quite a long time and much frustation to figure this next part out, but credit goes to
https://joelsenders.wordpress.com/2019/03/14/dear-launchctl-were-all-using-you-wrong/
Run "launchctl bootstrap gui/$userID /Library/LaunchAgents/com.hasanashqeen.wsb-dd.plist"
and it should start working once a week on Sundays. You can change that by modifying the values at the end of the plist.
If you ever want to stop this automated task, just run "launchctl bootout gui/$userID /Library/LaunchAgents/some.company.plist"

Small disclaimer: The files not referenced are either extra stores of data (text files) or just trial/older versions of the above, such as the
directory send_email. I also apologize for the code - it's mostly clear but still a lot of notes for things to add and areas I
should clean up. And as I have mentioned above - do not take any ticker these scripts give as guaranteed halal. This should just be an initial list
from which you should do your own reserach, inclduing confirming halalness.

# Why I Made This

Partly as a personal project to sharpen my Python skills and partly to automate my own investing research.

But the biggest reason is that when I first started trying to invest in a halal manner, all I could find were buggy apps with ridiculous pay walls,
a very limited number of websites with again ridiculous pay walls, or little to no lists of actual halal tickers on US based stock exchanges. It was quite shocking to me.
The very basic information of just filtering tickers for Shariah standards should exist and be free for all Muslims. People need to realize that the concepts of halal/haram
extend to everything, even your investments and we should all try our best and help each other to stay away from putting our money in areas against our beliefs.
During the ideation and creation of this, I found out about services such as Zoya Finance and others. It's great they exist and I encourage everyone to use them, but I still
standby the idea that a free resource should exist and this is my attempt at it.
