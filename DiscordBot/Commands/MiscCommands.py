from random import randint
import discord
from datetime import datetime

class MiscCommands:
    """
    All the commands that don't quite fit in anywhere else

    Functions
    __________
    getPatchNotes() -> (str)
        Parses PATCH.txt and returns a string with its contents
    getHelpMessage() -> (str)
        Returns a string of commands the user can do
    getRandomCompliment() -> (str)
        Fun little script that returns a random compliment
    """

    fire = None

    def __init__(self, fire):
        self.fire = fire

    def sendFeedback(self, guild, user, feedbackString):
        self.fire.postFeedback(guild, user, feedbackString)

        return "Thank you for your feedback <3"

    def getPatchNotes(self):
        """
        Parses PATCH.txt and returns a string with its contents

        Returns
        ----------
        s (str): The patch notes string
        """

        with open('../data/PATCH.txt') as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        s = '```'
        for c in content:
            s += c + '\n'
        s += '```'
        return s

    def getHelpMessage(self):
        """
        Returns a string of commands the user can do

        Returns
        ----------
        s (str): Help message string
        """

        timeLoggerStr = ""
        discordPointsStr = ""
        discordBetsStr = ""
        miscStr = ""

        timeLoggerStr += '`-totallog`: gets the tracked minutes in voice\n'
        timeLoggerStr += '`-todaylog`: gets the tracked minutes for the day\n'
        timeLoggerStr += '`-weeklog`: amount of time logged for the last 7 days\n'
        timeLoggerStr += '`-mylog`: some cool stats\n'

        discordPointsStr += '`-points`: shows all of the points for each user in the Discord server\n'
        discordPointsStr += '`-addreward`(admins): add a reward for discord points\n'
        discordPointsStr += '`-rewards`: shows a list of all rewards for the Discord server\n'
        discordPointsStr += '`-redeem`: redeem a reward\n'

        discordBetsStr += '`-createbet`: create a bet / prediction\n'
        discordBetsStr += '`-closebet`: closes a bet for submission\n'
        discordBetsStr += '`-completebet`: completes the bet and pays points to the winner(s)\n'
        discordBetsStr += '`-bet`: bet on an option in a particular prediction\n'
        discordBetsStr += '`-allbets`: shows a list of all active bets\n'
        discordBetsStr += '`-showbet`: shows a particular bet and its options\n'
        discordBetsStr += '`-mybets`: shows a list of all active bets for the user\n'

        miscStr += '`-help`: lists all commands\n'
        miscStr += '`-rob`: :-)\n'
        miscStr += '`-hello`: hey :)\n'

        now = datetime.today()
        embed = discord.Embed(title="Kirbec Bot", description="All of Kirbec Bot's commands", timestamp=now, colour=discord.Colour.purple())

        embed.add_field(name="Time Logger", value=timeLoggerStr, inline=False)
        embed.add_field(name="Discord Points", value=discordPointsStr, inline=False)
        embed.add_field(name="Discord Bets", value=discordBetsStr, inline=False)
        embed.add_field(name="Misc.", value=miscStr, inline=False)

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        return embed

    def getRandomCompliment(self):
        """
        Fun little script that returns a random compliment

        Returns
        ----------
        s (str): Random compliment string
        """

        with open('../../data/Compliments.txt') as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        return content[randint(0,99)]

    def getDonkeyImage(self):
        """
        Fun script that sends a donkey image with a user tagged

        Returns
        ----------
        discord image
        """

        PATH_TO_DONKEY = '../../data/donkey.png'

        return discord.File(PATH_TO_DONKEY)



