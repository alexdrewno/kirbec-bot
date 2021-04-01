import discord
import itertools
import re

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
        messageAndOptions = re.findall("\[(.*?)\]", messageString)

        if len(messageAndOptions) != 2:
            return getUsageEmbed("-createbet [[Bet Description]] [[Option 1], [Option 2], ...]\n\nexample: -createbet [I will win this game] [yes, no]")

        try:
            betTitle = messageAndOptions[0]
            betOptionsList = messageAndOptions[1].split(',')
            betOptionsList.sort()

            betOptions = {}
            for option in betOptionsList:
                betOptions[option] = 0

            now = datetime.now()
            betStartedAt = now.strftime("%H:%M on %m/%d/%Y")

            betId = self.fire.postNewBet(guild, user.id, betTitle, betOptions, betStartedAt)

            return self.__createBetEmbed(guild, user, betTitle, betOptions, str(betId), "Open", betStartedAt)
        except Exception as e:
            print(e)
            return getUsageEmbed("-createbet [[Bet Description]] [[Option 1], [Option 2], ...]\n\nexample: -createbet [I will win this game] [yes, no]")

    def closeBet(self, guild, user, betId):
        betDict, error = self.fire.postCloseBet(guild, user, str(betId))

        if error:
            return getOopsEmbed(error)
        else:
            return self.__createBetEmbed(guild, user, betDict['betTitle'], betDict['options'], str(betDict['betId']), "Closed", betDict['startedAt'])

    async def completeBet(self, guild, user, betId, winnerOptionId):
        betDict, userDict, error = await self.fire.postCompleteBet(guild, user, str(betId), winnerOptionId)

        if error:
            return getOopsEmbed(error)
        else:
            return self.__createCompletedBetEmbed(guild, betDict, userDict)

    def bet(self, guild, user, messageString):
        # BetList = [BetId, Option Number, Cost]
        betList = messageString.split(" ")
        if len(betList) == 3:
            betDict, error = self.fire.postBet(guild, user, betList[0], betList[1], int(betList[2]))
        
            if error != None:
                return getOopsEmbed(error)
            else:
                return self.__createBetEmbed(guild, user, betDict['betTitle'], betDict['options'], str(betDict['betId']), "Open", betDict['startedAt'])
        else:
            return getUsageEmbed("-bet [bet id] [option number] [discord points amount]\n\n example: -bet 3 2 500")

    def getAllActiveBets(self, guild):
        betDict = self.fire.fetchAllBets(guild)
        activeBets = []

        for key in betDict: 
            if key != 'numBets' and not betDict[key]['completed']:
                activeBets.append(betDict[key])
        
        if len(activeBets) > 0:
            return self.__createAllBetsEmbed(activeBets)
        else:
            return self.__createNoBetsEmbed()


    def showBetForUser(self, guild, user):
        betDict = self.fire.fetchAllBets(guild)
        activeBets = []

        for key in betDict:
            if key != 'numBets' and int(betDict[key]['startedBy']) == user.id:
                if not betDict[key]['completed']:
                    activeBets.append(betDict[key])

        if len(activeBets) > 0:
            return self.__createMyBetsEmbed(user, activeBets)
        else:
            return self.__createNoBetsEmbed()

    # ---------- MARK: - Private Methods ----------
    def __createBetEmbed(self, guild, user, betTitle, betOptions, betId, betStatus, betStartedAt):
        idString, titleString, amountString = self.__createBetOptionsStrings(betOptions)
        now = datetime.today()

        embed = discord.Embed(title=betTitle, description="Created by: TODO", timestamp=now, colour=discord.Colour.purple())

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Bet Id", value=betId)
        embed.add_field(name="Started At", value=betStartedAt)
        embed.add_field(name="Status", value=betStatus, inline=True)
        embed.add_field(name="Num", value=idString, inline=True)
        embed.add_field(name="Option", value=titleString, inline=True)
        embed.add_field(name="Total Amount Bet", value=amountString, inline=True)
        embed.add_field(name="To Bet:", value="-bet [bet id] [option number] [discord points amount]")

        return embed

    def __createCompletedBetEmbed(self, guild, betDict, userDict):
        userString, amountString = self.__createUserAmountStrings(userDict)

        now = datetime.today()
        embed = discord.Embed(title=betDict['betTitle'], description=" ", timestamp=now, colour=discord.Colour.green())

        embed.add_field(name="Winner", value=betDict["winningOption"], inline=False)
        embed.add_field(name="Winners", value=userString, inline=True)
        embed.add_field(name="Amount Won", value=amountString, inline=True)
        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        return embed

    def __createMyBetsEmbed(self, user, activeBets):
        now = datetime.today()
        embed = discord.Embed(title="My Bets", description=" ", timestamp=now)

        betIds, betTitles, betStatus = self.__getActiveBetsStrings(activeBets)

        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Id", value=betIds)
        embed.add_field(name="Title", value=betTitles)
        embed.add_field(name="Status", value=betStatus)

        return embed
    
    def __createAllBetsEmbed(self, activeBets):
        now = datetime.today()
        embed = discord.Embed(title="All Active Bets", description=" ", timestamp=now)

        betIds, betTitles, betStatus = self.__getActiveBetsStrings(activeBets)

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Id", value=betIds)
        embed.add_field(name="Title", value=betTitles)
        embed.add_field(name="Status", value=betStatus)

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
        
        betOptionKeys = sorted(list(betOptions.keys()))

        for i in range(len(betOptionKeys)):
            betOptionIds += str(i+1) + "\n"
            betOptionTitles += str(betOptionKeys[i]) + "\n"
            betOptionTotalAmount += str(betOptions[betOptionKeys[i]]) + "\n"

        return betOptionIds, betOptionTitles, betOptionTotalAmount
    
    def __createUserAmountStrings(self, userDict):
        usersString = ""
        amountString = ""

        # This sorts the dictionary by highest-value and converts it to a list
        # It takes form [(user_0.id, value_0) ...(user_n.id, value_n)]
        sortedUserDict = [(k, userDict[k]) for k in sorted(userDict, key=userDict.get, reverse=True)]

        for element in sortedUserDict:
            usersString += element[0] + "\n"
            amountString += str(element[1]) + "\n"
        
        return usersString, amountString
    
    def __getActiveBetsStrings(self, activeBets):
        betIds = ""
        betTitles = ""
        betStatus = ""

        activeBets = sorted(activeBets, key=lambda k: k['betId']) 

        for bet in activeBets:
            numLines, formattedBetTitle = formatString(str(bet['betTitle']))
            betIds += str(bet['betId']) + ('\n' * numLines)
            betTitles += formattedBetTitle + '\n'

            if bet['completed']:
                betStatus += 'completed' + ('\n' * numLines)
            elif bet['closed']:
                betStatus += 'closed' + ('\n' * numLines)
            else:
                betStatus += 'open' + ('\n' * numLines)

        return betIds, betTitles, betStatus