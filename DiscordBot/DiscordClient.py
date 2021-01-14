import discord
import asyncio

from Fire import Fire
from Commands.TimeLogger import TimeLogger
from Commands.MiscCommands import MiscCommands
from Commands.DiscordPoints import DiscordPoints

class DiscordClient(discord.Client):
    """
    Creates an instance of the "Bot"

    Attributes
    __________
    sharedFire: (Fire obj)
        Instance of the custom Fire class to fetch and update the database
    timeLogger: (TimeLogger obj)
        Instance of the TimeLogger class to display and parse information from
        the database
    miscCommands: (MiscCommands obj)
        Instance of the MiscCommands class to display random Misc. messages

    Functions
    __________
    async on_ready()
        Implementing discord.Client on_ready() that is called when the bot is ready
    async on_message()
        Implementing discord.Client on_message() that is called when a user messages
        in a server (discord.Guild)

    """
    sharedFire = None
    timeLogger = None
    miscCommands = None
    discordPoints = None

    async def on_ready(self):
        """
            Implementing discord.Client on_ready() that is called when the bot is ready

            We do any additional post-initialization set-up here
        """
        print('Logged on as {0}!'.format(self.user))
        self.sharedFire = Fire()
        self.timeLogger = TimeLogger(self.sharedFire)
        self.discordPoints = DiscordPoints(self.sharedFire)
        self.miscCommands = MiscCommands()
        self.loop.create_task(self.__track_time())

    async def __track_time(self):
        """
            Private helper function to help track time

            This function is called on a separate thread and loops every 60 seconds
        """

        await self.wait_until_ready()

        while not self.is_closed():
            try:
                for guild in self.guilds:
                    members = self.__filter_channel_members(guild)
                    self.sharedFire.incrementTimes(guild, members)
                await asyncio.sleep(60)
            except Exception as e:
                print("ERROR: ", str(e))
                await asyncio.sleep(60)

    def __filter_channel_members(self, guild):
        """
            Private helper function to filter members to track

            We do not increment times for individuals that are deafened, muted, or afk
        """

        members = []
        channels = guild.voice_channels

        for cur_channel in channels:
            if cur_channel.members:
                for member in cur_channel.members:
                    if not member.voice.self_deaf and not member.voice.afk and not member.voice.deaf:
                        members.append(member)

        return members

    async def on_message(self, message):
        """
            Implementing discord.Client on_message() that is called when a user messages
            in a server (discord.Guild)

            This is where all of the commands are called for the DiscordClient
        """

        if message.author == self.user:
            return

        if len(message.content) < 1:
            return

        if message.content[0] == '-':
            # ---------- MARK: - Miscellaneous Commands ----------
            if message.content.startswith('-hello'):
                s = 'Hello ' + str(message.author) + '\n' + self.miscCommands.getRandomCompliment()
                await message.channel.send(s)

            elif message.content.startswith('-help'):
                s = self.miscCommands.getHelpMessage()
                await message.channel.send(s)

            elif message.content.startswith('-rob'):
                await message.channel.send("Rob is a qt3.14 :-)")

            elif message.content.startswith('-patch'):
                await message.channel.send(self.miscCommands.getPatchNotes())

            # ---------- MARK: - TimeLogger Commands ----------
            elif message.content.startswith('-totallog'):
                msg = message.content
                msgAndPage = msg.split(" ")
                if len(msgAndPage) == 2:
                    await message.channel.send(embed=await self.timeLogger.getTotalLogEmbed(int(msgAndPage[1]), message.guild))
                else:
    	            await message.channel.send(embed=await self.timeLogger.getTotalLogEmbed(1, message.guild))

            elif message.content.startswith('-todaylog'):
                await message.channel.send(embed=await self.timeLogger.getTodayLogEmbed(message.guild))

            elif message.content.startswith('-weeklog'):
                msg = message.content
                msgAndPage = msg.split(" ")
                if len(msgAndPage) == 2:
                    await message.channel.send(embed=await self.timeLogger.getWeekLogEmbed(int(msgAndPage[1], message.guild)))
                else:
                    await message.channel.send(embed=await self.timeLogger.getWeekLogEmbed(1, message.guild))

            elif message.content.startswith('-mylog'):
                await message.channel.send(embed=self.timeLogger.getMyLogEmbed(message.guild, message.author))

            # ---------- MARK: - DiscordPoints Commands ----------
            elif message.content.startswith('-points'):
                    msg = message.content
                    msgAndPage = msg.split(" ")
                    if len(msgAndPage) == 2:
                        await message.channel.send(embed=await self.discordPoints.getDiscordPointsEmbed(int(msgAndPage[1]), message.guild))
                    else:
        	            await message.channel.send(embed=await self.discordPoints.getDiscordPointsEmbed(1, message.guild))
