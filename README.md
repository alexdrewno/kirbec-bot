# 🤖 KirbecBot
**KirbecBot is an open source Discord Bot written in Python that currently logs the amount of the time users spend in the Discord server with many more features in progress**
<br/>

## Commands

### ⏱️ Time-Logger 

*Note: KirbecBot increases time only when the user is not AFK, deafened, or muted.*

* ```-todaylog``` Shows the amount of time spent in the Discord server today (12:00AM to 11:59PM)
* ```-weeklog``` Shows the amount of time spent in the Discord server for the past week
* ```-totallog``` Shows the amount of time spent in the Discord server that has been logged by KirbecBot
* ```-mylog``` Shows personalized information for the user

### 💳 Discord Points
*Discord Points are accumulated by spending time in the Discord server and can be spent on guild-defined rewards*

* ```-points``` Shows all of the points for each user in the Discord server
* ```-addreward``` Add a reward for discord points (admins)
* ```-rewards``` Shows a list of all rewards for the Discord server
* ```-redeem``` Redeem a reward 

### 🎲 Discord Bets
*Bet/Make predictions against other users in the Discord server*

* ```-createbet``` Create a bet / prediction
* ```-closebet``` Closes a bet for submission
* ```-completebet``` Completes the bet and pays points to the winner
* ```-allbets``` Shows a list of all **active** bets
* ```-mybets``` Shows a list of all **active** bets for the user
* ```-bet``` Add a bet on a particular prediction option
* ```-showbet``` Shows a particular bet and its options

<br/>

## 🚀 Running KirbecBot on your local machine

### Requirements & Dependencies
* ```google-cloud-firestore``` and your own Firebase database
* ```discord``` and your own discord api key

### Setup
*Installing dependencies*
- ```pip install google-cloud-firestore```
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
 
### Documentation & Styling
- This project uses [The numpy docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html) for documentation formatting and styling. 
- [Pylint](https://www.pylint.org/) is used for code quality

### Comments
> Thank you for checking out the project; please feel free to start a PR with any improvements/changes

> A special thanks to my community discord server for letting me develop and test the bot in the server
