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

    def createBet(self, guild, userId, messageString):
        messageStringList = ["".join(x) for _, x in itertools.groupby(messageString, key=str.isdigit)]

        if len(messageStringList) < 2:
            return getUsageEmbed("-bet [Bet Description] [Bet Amount]\n\nexample: -bet I will win this game 500")

        try:
            betAmount = int(messageStringList[len(messageStringList)-1])
            betTitle = self.__parseTitleStringList(messageStringList)

            self.fire.postNewBet(guild, userId, betTitle, betAmount)
        except:
            return getUsageEmbed("-bet [Bet Description] [Bet Amount]\n\nexample: -bet I will win this game 500")

    # ---------- MARK: - Private Methods ----------
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
