# 🤖 KirbecBot
**KirbecBot is an open source Discord Bot written in Python that currently logs the amount of the time users spend in the Discord server with many more features in progress**
<br/>

## ⏱️ Time-Logger Commands

*Note: KirbecBot increases time only when the user is not AFK, deafened, or muted.*

* ```-todaylog:``` Shows the amount of time spent in the Discord server today (12:00AM to 11:59PM)
* ```-weeklog :``` Shows the amount of time spent in the Discord server for the past week
* ```-totallog:``` Shows the amount of time spent in the Discord server that has been logged by KirbecBot
* ```-mylog :``` Shows personalized information for the user
<br/>

## 🚀 Running KirbecBot on your local machine

### Requirements & Dependencies
* ```firebase-admin``` and your own Firebase database
* ```discord``` and your own discord api key

### Setup
*Installing dependencies*
- ```pip install firebase-admin```
- ```pip install discord```

*Set the environment variables necessary*
1. Copy your Firebase config file to your environment variables (Look at ```firebase_config.py``` for the necessary variables)
2. Set ```DISCORD_TOKEN``` to your discord API token

*Running the bot*
- ```python3 DiscordBot/main.py```
<br/>

## ℹ️ Additional Information

### Future Extensions
 - [ ] Adding graphs for time spent by user and discord
 - [ ] Logging time by channel
 - [ ] Extending the bot beyond time-logging
 
### Documentation
This project uses [The numpy docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html) for documentation formatting and styling. 

### Comments
> Thank you for checking out the project; please feel free to start a PR with any improvements/changes

> A special thanks to my community discord server for letting me develop and test the bot in the server
