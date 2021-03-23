import discord
import itertools

from datetime import datetime
from .utils import *

# IDEAS
# 1. BETTING AGAINST ONE PLAYER
# 2. WINRATES
# 3. OTHER STATS

class DiscordBets:
    fire = None

    def __init__(self, fire):
        self.fire = fire

    def createBet(self, guild, user, messageString):
        messageStringList = ["".join(x) for _, x in itertools.groupby(messageString, key=str.isdigit)]

        if len(messageStringList) < 2:
            return getUsageEmbed("-bet [Bet Description] [Bet Amount]\n\nexample: -bet I will win this game 500")

        try:
            betAmount = int(messageStringList[len(messageStringList)-1])
            betTitle = self.__parseTitleStringList(messageStringList)

            self.fire.postNewBet(guild, user.id, betTitle, betAmount)

            return self.__createBetEmbed(guild, user, betTitle, betAmount)
        except:
            return getUsageEmbed("-bet [Bet Description] [Bet Amount]\n\nexample: -bet I will win this game 500")

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
    def __createBetEmbed(self, guild, user, betTitle, betAmount):
        now = datetime.today()
        embed = discord.Embed(title="My Bets", description=" ", timestamp=now)

        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Bet Title", value=betTitle, inline=False)
        embed.add_field(name="Bet Amount", value=str(betAmount), inline=False)
        embed.add_field(name="Voting", value="To vote, react below.", inline=False)

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

    def __parseTitleStringList(self, betTitleStringList):
        """
        Private function to recreate bet title

        Parameters
        ----------
        rewardStringList: list(String)
            List of strings representing the title

        Returns
        ----------
        s: string
            The bet title string
        """
        s = ""
        for i in range(len(betTitleStringList)-1):
            s += betTitleStringList[i]

        return s
