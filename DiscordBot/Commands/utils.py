from datetime import datetime
import discord

def formatString(oldStr):
    """
    Format string into separate lines
    
    *NOTE* 
    The newStr already has new lines and the developer should use the numLines return
    to align any other strings to the newStr

    Parameters
    ----------
    oldStr: string
        Old string to be Formatted

    Returns
    ----------
    numLines: int
        Number of lines the new string will take up
    newStr: string
        New string with new lines
    """

    LINE_LENGTH = 32
    strList = oldStr.split(" ")

    numLines = 1
    newStr = ""
    curLen = 0

    for word in strList:
        if (len(word) + curLen) > LINE_LENGTH:
            numLines += 1
            curLen = len(word) + 1
            newStr += ("\n" + word + " ")
        else:
            curLen += (len(word) + 1)
            newStr += (word + " ")

    return numLines, newStr

def getOopsEmbed(errorString):
    """
    Show the usage for addReward

    Parameters
    ----------
    errorString : String
        A string representing the error that occurred

    Returns
    ----------
    discord.Embed
        Embedded message with the error message
    """

    now = datetime.today()
    embed = discord.Embed(title="Oops!", description="", timestamp=now, colour=discord.Colour.red())

    embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.add_field(name="There was an error", value=errorString)

    return embed

def getUsageEmbed(usageString):
    """
    Show the usage for a particular command

    Parameters
    ----------
    usageString : String
        The usage string info for the command

    Returns
    ----------
    discord.Embed
        Embedded message with the usage info
    """

    now = datetime.today()
    embed = discord.Embed(title="Oops!", description="", timestamp=now, colour=discord.Colour.orange())

    embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.add_field(name="Usage", value=usageString)

    return embed

def getMissingPermissionsEmbed(errorString):
    """
    Show a message saying that the user does not have the correct permissions

    Returns
    ----------
    discord.Embed
        Embedded message saying the user doesn't have the correct permissions
    """

    now = datetime.today()
    embed = discord.Embed(title="Sorry!", description="", timestamp=now, colour=discord.Colour.red())

    embed.set_footer(text="Kirbec Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.add_field(name="Missing Permissions", value=errorString)

    return embed
