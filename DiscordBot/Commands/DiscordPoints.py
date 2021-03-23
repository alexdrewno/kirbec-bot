from datetime import datetime
import discord
import itertools
from .utils import formatString, getUsageEmbed

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
    def createNewReward(guild, rewardString) -> (discord.Embed)
        Adds a reward and returns the updated list of rewards as an embedded msg
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
            return getUsageEmbed("-addreward [Desired Reward] [Price of the Reward]\n\nexample: -addreward CSGO with friends 500")

        try:
            rewardCost = int(rewardStringList[len(rewardStringList)-1])
            rewardTitle = self.__parseRewardStringList(rewardStringList)

            self.fire.postNewReward(guild, rewardTitle, rewardCost)

            return self.getRewardsEmbed(guild)
        except Exception as e:
            print("ERROR ", e)
            return getUsageEmbed("-addreward [Desired Reward] [Price of the Reward]\n\nexample: -addreward CSGO with friends 500")

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

    def redeemReward(self, guild, user, reward_id):
        """
        Redeems the desired reward with DiscordPoints
        [@Todo: Ping Users associated with the reward]

        Parameters
        ----------
        guild     : discord.Guild
            The server that we want to get information from
        user      : discord.Member if in guild, discord.User otherwise
            The user that redeemed the reward
        reward_id : Int
            The id of the reward to redeem

        Returns
        ----------
        discord.Embed
            Embedded message with the redeemed reward
        """

        points_dict = self.fire.fetchDiscordPoints(guild)
        rewards_dict = self.fire.fetchAllRewards(guild)
        rewards_list = [(k, rewards_dict[k]) for k in sorted(rewards_dict, key=rewards_dict.get, reverse=True)]

        try:
            # Check to see if the reward_id is within the list of rewards
            if int(reward_id) > len(rewards_list) or int(reward_id) < 1:
                return self.__createNotARewardEmbed()

            reward_title = rewards_list[int(reward_id) - 1][0]
            reward_cost = rewards_list[int(reward_id) - 1][1]

            #Check to see if the user has enough points to redeem the reward
            if points_dict[str(user.id)] and points_dict[str(user.id)] < reward_cost:
                return self.__createNotEnoughPointsEmbed(user, points_dict[str(user.id)])
            else:
                new_points = points_dict[str(user.id)] - reward_cost

                self.fire.postNewDiscordPoints(guild, str(user.id), new_points)

                return self.__createRedeemRewardEmbed(reward_title, reward_cost, user, new_points)
        except Exception as e:
            print(e)
            return getUsageEmbed("-redeemReward [Desired Reward Id]\n\nexample: -redeemReward 3")



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
            numLines, formattedRewardString = formatString(str(rewardsList[i][0]))

            idString += str(i+1) + ("\n" * numLines)
            rewardString += formattedRewardString + "\n"
            costString += str(rewardsList[i][1]) + ("\n" * numLines)

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

    def __createRedeemRewardEmbed(self, reward_title, reward_cost, user, new_points):
        """
        Private function to help create a redeem reward embed

        Parameters
        ----------
        reward_title: string
            Title of the reward to be redeemed
        reward_cost : int
            Cost of the reward to be redeemed
        user        : discord.Member if in guild, discord.User otherwise
            User_id of the user that redeemed the reward

        Returns
        ----------
        discord.Embed
            Embedded message that states the redeemed reward
        """

        title = "Reward Redeemed"
        description = ""
        now = datetime.today()
        embed = discord.Embed(title=title, description=description, timestamp=now)

        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Reward", value=reward_title, inline=False)
        embed.add_field(name="Price", value=reward_cost, inline=False)
        embed.add_field(name="Points Remaining", value=str(new_points), inline=False)

        return embed

    def __createNotEnoughPointsEmbed(self, user, user_points):
        """
        Private function to help create a not enough points embed message

        Parameters
        ----------
        user_points : int
            The amount of points that the user currently has
        user        : discord.Member if in guild, discord.User otherwise
            User that try to redeem the reward

        Returns
        ----------
        discord.Embed
            Embedded message that states that the user doesn't have enough points
        """

        title = "Oops!"
        description = ""
        now = datetime.today()
        embed = discord.Embed(title=title, description=description, timestamp=now, colour=discord.Colour.red())

        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Not enough points", value="You have: " + str(user_points))

        return embed

    def __createNotARewardEmbed(self):
        """
        Private function to help create a "invalid reward id" embed

        Returns
        ----------
        discord.Embed
            Embedded message that states that the reward id is invalid
        """

        title = "Oops!"
        description = ""
        now = datetime.today()
        embed = discord.Embed(title=title, description=description, timestamp=now, colour=discord.Colour.red())

        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Not a reward", value="Please enter a valid reward id")

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
