from datetime import datetime
import discord
import itertools

class DiscordPoints:
    """
    Class that parses Discord Points info and interactions

    Attributes
    __________
    fire (Fire obj): The fire instance where information is fetched/updated

    Functions
    __________
    async getDiscordPointsEmbed(page, guild) -> (discord.Embed)
        Makes an embedded message with total points for each user
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
            Embedded message of Discord Points for each member of the guild
        """
        d = self.fire.fetchDiscordPoints(guild)

        # This sorts the dictionary by highest-value and converts it to a list
        # It takes form [(user_0.id, value_0) ...(user_n.id, value_n)]
        info_arr = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]

        userString, pointsString, description = await self.__createdEmbedStrings(guild, info_arr, page)

        title = "Discord Points"

        return self.__createPointsEmbed(title, description, userString, pointsString)

    def createNewReward(self, guild, rewardString):
        """
        Create new reward for the guild

        Parameters
        ----------
        guild : discord.Guild
            The server that we want to get information from
        rewardString : string
            String with the reward title and cost

        Returns
        ----------
        discord.Embed
            Embedded message of the updated rewards for the server
        """

        rewardStringList = ["".join(x) for _, x in itertools.groupby(rewardString, key=str.isdigit)]

        if len(rewardStringList) < 2:
            return self.getUsageEmbed()

        try:
            rewardCost = int(rewardStringList[len(rewardStringList)-1])
            rewardTitle = self.__parseRewardStringList(rewardStringList)

            self.fire.postNewReward(guild, rewardTitle, rewardCost)

            return self.getRewardsEmbed(guild)
        except:
            return self.getUsageEmbed()

    def getMissingPermissionsEmbed(self):
        """
        Show a message saying that the user does not have the correct permissions

        Returns
        ----------
        discord.Embed
            Embedded message saying the user doesn't have the correct permissions
        """

        now = datetime.today()
        embed = discord.Embed(title="Sorry!", description="", timestamp=now)

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Missing Permissions", value="Oops.. you have to be an admin to use this command")

        return embed


    def getRewardsEmbed(self, guild):
        """
        Get all of the current rewards for the guild

        Parameters
        ----------
        guild : discord.Guild
            The server that we want to get information from

        Returns
        ----------
        discord.Embed
            Embedded message with all of the rewards for the guild
        """

        rewards_dict = self.fire.fetchAllRewards(guild)

        if rewards_dict == {}:
            return self.__noRewardsEmbed(guild)

        rewardsList = [(k, rewards_dict[k]) for k in sorted(rewards_dict, key=rewards_dict.get, reverse=True)]

        idString, rewardsString, costsString = self.__getRewardsEmbedStrings(rewardsList)

        return self.__createRewardsEmbed(idString, rewardsString, costsString)


    def getUsageEmbed(self):
        """
        Show the usage for addReward

        Parameters
        ----------
        guild : discord.Guild
            The server that we want to get information from

        Returns
        ----------
        discord.Embed
            Embedded message with the usage for addReward
        """

        now = datetime.today()
        embed = discord.Embed(title="Oops!", description="", timestamp=now)

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Usage", value="-addreward [Desired Reward] [Price of the Reward]\n\nexample: -addreward CSGO with friends 500")

        return embed


    # ---------- MARK: - Private Functions ----------
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

    def __createPointsEmbed(self, title, description, userString, pointsString):
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


    def __noRewardsEmbed(self, guild):
        """
        Private function that shows that there are no rewards yet for the guild

        Parameters
        ----------
        guild : discord.Guild
            The server that we want to get information from

        Returns
        ----------
        discord.Embed
            Embedded message that states no rewards are in the guild
        """

        now = datetime.today()
        embed = discord.Embed(title="Oops!", description="", timestamp=now)

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="No Rewards Set Yet!", value="To add a reward:\n-addreward [Desired Reward] [Price of the Reward]")

        return embed

    def __getRewardsEmbedStrings(self, rewardsList):
        """
        Private function that gets formatted strings for the list of rewards

        Parameters
        ----------
        rewardsList: [(reward_title_0, cost_0)...]
            List of rewards sorted by the highest cost

        Returns
        ----------
        idString: string
            String representing the id's of the rewards separated by '\n'
        rewardString: string
            String representing the title of the rewards separated by '\n'
        costString: string
            String representing the costs of the rewards separated by '\n'
        """

        idString = ""
        rewardString = ""
        costString = ""

        for i in range(len(rewardsList)):
            idString += str(i+1) + "\n"
            rewardString += str(rewardsList[i][0]) + "\n"
            costString += str(rewardsList[i][1]) + "\n"

        return idString, rewardString, costString

    def __createRewardsEmbed(self, idString, rewardString, costString):
        """
        Private function to help create a rewards embed

        Parameters
        ----------
        idString: string
            String representing the id's of the rewards separated by '\n'
        rewardString: string
            String representing the title of the rewards separated by '\n'
        costString: string
            String representing the costs of the rewards separated by '\n'

        Returns
        ----------
        discord.Embed
            Embedded message that states all of the rewards
        """

        title = "Discord Point Rewards"
        description = ""
        now = datetime.today()
        embed = discord.Embed(title=title, description=description, timestamp=now)

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="ID", value=idString)
        embed.add_field(name="Reward", value=rewardString)
        embed.add_field(name="Price", value=costString)

        return embed

    def __parseRewardStringList(self, rewardStringList):
        """
        Private function to recreate reward title

        Parameters
        ----------
        rewardStringList: list(String)
            List of strings representing the title

        Returns
        ----------
        s: string
            The reward title string
        """
        s = ""
        for i in range(len(rewardStringList)-1):
            s += rewardStringList[i]

        return s
