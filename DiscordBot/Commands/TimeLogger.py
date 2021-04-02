import discord
import os
from datetime import datetime
import datetime as dt

class TimeLogger:
    """
    Parses and formats time information from the Fire class

    Attributes
    __________
    fire (Fire obj): The fire instance where information is fetched/updated

    Functions
    __________
    async getTotalLogEmbed(page, guild) -> (discord.Embed)
        Makes an embedded message with total times for each user
    async getTodayLogEmbed(guild)       -> (discord.Embed)
        Makes an embedded message with times today for each tracked user
    async getWeekLogEmbed(page, guild)  -> (discord.Embed)
        Makes an embedded message with user-times for the week
    async getMyLogEmbed(guild, user)    -> (discord.Embed)
        Makes an embedded message with personalized stats for the discord.User
    """

    fire = None

    def __init__(self, fire):
        self.fire = fire

    async def getTotalLogEmbed(self, page, guild):
        """
        Makes an embedded message with total times for each user

        Parameters
        ----------
        page  : (int)
            Page of the message we want to look at (20 entries per page)
        guild : discord.Guild
            The server that we are tracking

        Returns
        ----------
        discord.Embed
            Embedded message of total times for each user
        """

        d = self.fire.fetchTotalTimes(guild)
        member_dict = await self.fire.fetchAllMembers(guild)

        # This sorts the dictionary by highest-value and converts it to a list
        # It takes form [(user_0.id, value_0) ...(user_n.id, value_n)]
        d = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]

        userString, timeString, rankString, description = await self.__createdEmbedStrings(guild, d, page)

        title = "Total Log"

        return self.__createAggregateLogEmbed(title, description, userString, timeString, rankString)

    async def getTodayLogEmbed(self, guild):
        """
        Makes an embedded message with times today for each tracked user

        Parameters
        ----------
        guild : discord.Guild
            The server that we are tracking

        Returns
        ----------
        discord.Embed
            Embedded message of times today for each user
        """

        l = self.fire.fetchAllDateTimes(guild)
        l = list(l.items())
        userIdAndVal = l[0][1]

        userValDict = sorted(userIdAndVal.items(), key=lambda kv: kv[1])
        userValDict.reverse()

        userString, timeString, rankString, description = await self.__createdEmbedStrings(guild, userValDict, 1)

        title = "Today's Log"

        return self.__createAggregateLogEmbed(title, description, userString, timeString, rankString)

    async def getWeekLogEmbed(self, page, guild):
        """
        Makes an embedded message with total times for each user

        Parameters
        ----------
        page  : (int)
            Page of the message we want to look at (20 entries per page)
        guild : discord.Guild
            The server that we are tracking

        Returns
        ----------
        discord.Embed
            Embedded message of the log for the week for each user
        """

        allDateTimes = self.fire.fetchAllDateTimes(guild)
        allDateTimes = list(allDateTimes.items())

        if len(allDateTimes) < 7:
            return

        firstDate, secondDate, userValDict, = self.__sumUserTimeValues(allDateTimes)
        userValDict = [(k, userValDict[k]) for k in sorted(userValDict, key=userValDict.get, reverse=True)]

        userString, timeString, rankString, description = await self.__createdEmbedStrings(guild, userValDict, 1)

        title = "Week Log (" + secondDate + " - " + firstDate + ")"
        return self.__createAggregateLogEmbed(title, description, userString, timeString, rankString)


    def getMyLogEmbed(self, guild, user):
        """
        Makes an embedded message with personalized stats for the user

        Parameters
        ----------
        guild : discord.Guild
            The server that we are tracking
        user  : discord.Member if in guild, discord.User otherwise
            The user we are getting personalized information for

        Returns
        ----------
        discord.Embed
            Embedded message of personalized information
        """

        date_times_dict = self.fire.fetchAllDateTimes(guild)
        total_times_dict = self.fire.fetchTotalTimes(guild)

        maxDate = ""
        maxVal = 0


        # Gets total time
        user_id_string = str(user.id)
        if not user_id_string in total_times_dict.keys():
            print("Couldn't find user_id in totalTimes")
            return

        totalTime = total_times_dict[user_id_string]

        # Finds maximum value
        for key in date_times_dict:
            val = date_times_dict[key]
            if user_id_string in val and val[user_id_string] > maxVal:
                maxVal = val[user_id_string]
                maxDate = key

        todayVal = 0
        # This whole mumbo-jumbo gets the most recent data and
        # reports how much time was spent for that particular username
        if user_id_string in list(date_times_dict.items())[0][1]:
            todayVal = list(date_times_dict.items())[0][1][user_id_string]

        return self.__createMyLogEmbed(user, totalTime, maxVal, maxDate, todayVal)

    def __createMyLogEmbed(self, user, totalTime, maxTime, maxDate, todayTime):
        """
        Private helper function to create embedded message for the user

        Parameters
        ----------
        user : discord.Member if in guild, discord.User otherwise
            The user we are getting personalized information for
        totalTime : (int)
            The total time logged for the user
        maxTime : (int)
            The maximum amount of time for a single day for the user
        maxDate : (str)
            The date when maxTime occurred
        todayTime: (int)
            The amount of time spent today so far for the user

        Returns
        ----------
        discord.Embed
            Embedded message of time-logger information the user
        """

        user_display_name = user.display_name

        now = datetime.today()
        embed = discord.Embed(timestamp=now)

        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=user_display_name, icon_url=user.avatar_url)
        embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="Total Time", value= self.__createTimeString(totalTime) + "\n", inline=False)
        embed.add_field(name="Time Today", value= self.__createTimeString(todayTime) + "\n", inline=False)
        embed.add_field(name="Longest Day", value= self.__createTimeString(maxTime) + " (" + str(maxDate) + ")\n", inline=False)

        return embed

    def __createAggregateLogEmbed(self, title, description, userString, timeString, rankString):
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
            String representing the list of ordered times
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
        embed.add_field(name="Rank", value=rankString)
        embed.add_field(name="Username", value=userString)
        embed.add_field(name="Time", value=timeString)

        return embed

    async def __createdEmbedStrings(self, guild, sortedList, page):
        """
        Private helper function to create strings for the embedded message

        Parameters
        ----------
        guild : (discord.Guild)
            The server that we are tracking
        sortedList : arr[(key_0, val_0) ...  (key_n, val_n)]
            The sorted (by val) list of key, val pairs where key: user_id, val: time
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
        timeString = ""
        rankString = ""

        if page > pages or page < 0:
            page = 1

        for i in range(0,20):
            shiftedIndex = (page-1)*20 + i
            if shiftedIndex < len(sortedList):
                user_id = sortedList[shiftedIndex][0]
                time = sortedList[shiftedIndex][1]

                if int(user_id) in member_dict.keys():
                    userString += member_dict[int(user_id)] + '\n'
                    timeString += self.__createTimeString(time) + '\n'
                    rankString += str(shiftedIndex+1) + '\n'

        description = "Page " + str(page) + " of " + str(page)

        return userString, timeString, rankString, description

    def __sumUserTimeValues(self, listOfTimeVals):
        """
        Private helper function to sum all times (for the week) for each user

        Parameters
        ----------
        listOfTimeVals: [ (date_0, {user_0, val_0...}) .. (date_n, {user_0, val_0...}) ]
            List of (key,val) pairs where key = date, val = dictionary of users and
            corresponding time values

        Returns
        ----------
        firstDate: (str)
            The beginning of the week date-range
        secondDate: (str)
            The end of the week date-range
        d: dict{user: time_val}
            The summed dictionary of user and corresponding times
        """
        if len(listOfTimeVals) <= 7:
            return {}
        else:
            d = {}
            for i in range(7):
                date = listOfTimeVals[i][0]
                info = listOfTimeVals[i][1]

                if i == 0:
                    firstDate = str(date)
                if i == 6:
                    secondDate = str(date)

                for key in info:
                    val = info[key]
                    hrs = val // 60
                    mins = val % 60

                    if key in d:
                        d[key] += val
                    else:
                        d[key] = val
        return firstDate, secondDate, d

    def __createTimeString(self, val):
        """
        Private helper function to parse minutes to days,hours,minutes

        Parameters
        ----------
        val: (int)
            Number of minutes

        Returns
        ----------
        s: (str)
            Formatted time str in terms of days, months, minutes
        """

        s = ""

        if val == 0:
            return '0 mins '

        days = val // (24*60)
        hrs = (val - days * (24*60)) // 60
        mins = val % 60

        if days > 0:
            s += str(days) + ' days '
        if hrs > 0:
            s += str(hrs) + ' hrs '
        if mins > 0:
            s += str(mins) + ' mins '

        return s
