# Twitter Bot

### Category
Web scraping/automation/data collection

### Purpose
Collect data from Twitter Analytics accounts.

### User needs
Helping out the team's performance analyst automate a process that up until now was done manually. The bot visits 36 individual twitter accounts and collects data that is saved in a .csv file, ready for analysis.

### Data collected
- Followers
- Profile visits
- Mentions
- New followers
- Video analytics (csv download)
- Tweet analytics (csv download)

### File structure
Main file `twitter-bot.py` that imports the following modules
```

twitter-bot.py
|__format_number.py
|__return_mentions.py
|__return_new_followers.py
|__return_profile_visits.py
|__return_followers.py
|__create_csv.py


```

### Dependencies
Built with Python 3.6.4 and the following modules
- [selenium](https://selenium-python.readthedocs.io/index.html)
- datetime
- time
- os
- csv

### Developed by
Kostas Koutoupis ([@kkoutoup](https://github.com/kkoutoup)) for the Web and Publications Unit (WPU) of the Chambers and Committee Office (CCT), House of Commons

