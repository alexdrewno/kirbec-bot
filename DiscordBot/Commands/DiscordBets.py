import discord
import itertools
import re

from datetime import datetime
from .utils import *

# IDEAS
# 0. LOWERING THE BET ID
# 1. BETTING AGAINST ONE PLAYER
# 2. WINRATES
# 3. OTHER STATS

class DiscordBets:
    fire = None

    def __init__(self, fire):
        self.fire = fire

    def createBet(self, guild, user, messageString):
        messageAndOptions = re.findall("\[(.*?)\]", messageString)

        if len(messageAndOptions) != 2:
            return getUsageEmbed("-createbet [[Bet Description]] [[Option 1], [Option 2], ...]\n\nexample: -createbet [I will win this game] [yes, no]")

        try:
            betTitle = messageAndOptions[0]
            betOptionsList = messageAndOptions[1].split(',')
            betOptionsList.sort()
            betId = datetime.now().strftime('%d%H%M%S%f')

            betOptions = {}
            for option in betOptionsList:
                betOptions[option] = 0

            self.fire.postNewBet(guild, user.id, betTitle, betOptions, betId)

            return self.__createBetEmbed(guild, user, betTitle, betOptions, betId)
        except Exception as e:
            print(e)
            return getUsageEmbed("-createbet [[Bet Description]] [[Option 1], [Option 2], ...]\n\nexample: -createbet [I will win this game] [yes, no]")

    def showBetForUser(self, guild, user):
        betDict = self.fire.fetchAllBets(guild)
        curBet = None

        for key in betDict:
            if int(betDict[key]['startedBy']) == user.id:
                if not betDict[key]['completed']:
                    curBet = betDict[key]

        if curBet:
            return self.__createMyBetsEmbed(curBet, user)
        else:
            return self.__createNoBetsEmbed()

    # ---------- MARK: - Private Methods ----------
    def __createBetEmbed(self, guild, user, betTitle, betOptions, betId):
        idString, titleString, amountString = self.__createBetOptionsStrings(betOptions)
        now = datetime.today()
        embed = discord.Embed(title=betTitle, description="Bet Id: " + betId, timestamp=now)
        embed.set_thumbnail(url=user.avatar_url)

        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Num", value=idString)
        embed.add_field(name="Option", value=titleString)
        embed.add_field(name="Total Amount Bet", value=amountString)
        embed.add_field(name="To Bet:", value="-bet [bet id] [option number] [discord points amount]")

        return embed

    def __createMyBetsEmbed(self, curBetDict, user):
        now = datetime.today()
        embed = discord.Embed(title="My Bets", description=" ", timestamp=now)

        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Bet Title", value=curBetDict["betTitle"])
        embed.add_field(name="Bet Amount", value=str(curBetDict["betAmount"]))

        return embed

    def __createNoBetsEmbed(self):
        now = datetime.today()
        embed = discord.Embed(title="Oops!", description="", timestamp=now, colour=discord.Colour.red())

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Error", value="You have no current bets active.\n\nTo create a bet: -bet")

        return embed

    def __createBetOptionsStrings(self, betOptions):
        betOptionIds = ""
        betOptionTitles = ""
        betOptionTotalAmount = ""
        
        betOptionKeys = list(betOptions.keys())

        for i in range(len(betOptionKeys)):
            betOptionIds += str(i+1) + "\n"
            betOptionTitles += betOptionKeys[i] + "\n"
            betOptionTotalAmount += str(betOptions[betOptionKeys[i]]) + "\n"

        return betOptionIds, betOptionTitles, betOptionTotalAmount