from datetime import datetime
import discord

class DiscordPoints:
    """
    Class that parses Discord Points info and interactions

    Attributes
    __________
    fire (Fire obj): The fire instance where information is fetched/updated

    Functions
    __________

    """

    fire = None

    def __init__(self, fire):
        self.fire = fire

    async def getDiscordPointsEmbed(self, page, guild):
        """
        Makes an embedded message with DiscordPoints for each member in the guild

        Parameters
        ----------
        guild : discord.Guild
            The server that we want to get information from

        Returns
        ----------
        discord.Embed
            Embedded message of times today for each user
        """
        d = self.fire.fetchDiscordPoints(guild)

        # This sorts the dictionary by highest-value and converts it to a list
        # It takes form [(user_0.id, value_0) ...(user_n.id, value_n)]
        info_arr = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]

        userString, pointsString, description = await self.__createdEmbedStrings(guild, info_arr, page)

        title = "Discord Points"

        return self.__createEmbed(title, description, userString, pointsString)


    async def __createdEmbedStrings(self, guild, sortedList, page):
        """
        Private helper function to create strings for the embedded message

        Parameters
        ----------
        guild : (discord.Guild)
            The server that we are tracking
        sortedList : arr[(key_0, val_0) ...  (key_n, val_n)]
            The sorted (by val) list of key, val pairs where key: user_id, val: points
        page  : (int)
            Page of the message we want to look at (20 entries per page)

        Returns
        ----------
        discord.Embed
            Formatted information embedded into a message
        """

        member_dict = await self.fire.fetchAllMembers(guild)

        # Max 20 entries / page
        pages = len(sortedList) // 20 + 1

        userString = ""
        pointsString = ""
        rankString = ""

        if page > pages or page < 0:
            page = 1

        for i in range(0,20):
            shiftedIndex = (page-1)*20 + i
            if shiftedIndex < len(sortedList):
                user_id = sortedList[shiftedIndex][0]
                points = sortedList[shiftedIndex][1]

                if int(user_id) in member_dict.keys():
                    userString += member_dict[int(user_id)] + '\n'
                    pointsString += str(points) + '\n'

        description = "Page " + str(page) + " of " + str(page)

        return userString, pointsString, description

    def __createEmbed(self, title, description, userString, pointsString):
        """
        Formats information into an embedded message

        Parameters
        ----------
        title: (str)
            Title for the embedded message
        description: (str)
            Description for the embedded message
        userString: (str)
            String representing the list of ordered users
        timeString: (str)
            String representing the list of ordered points
        rankString: (str)
            String representing the ranks of each user

        Returns
        ----------
        discord.Embed
            Formatted information embedded into a message
        """
        now = datetime.today()
        embed = discord.Embed(title=title, description=description, timestamp=now)

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Username", value=userString)
        embed.add_field(name="Discord Points", value=pointsString)

        return embed
