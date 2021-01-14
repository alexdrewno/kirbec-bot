from random import randint

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

        s = 'Commands: \n\n'
        s += '`-help`: lists all commands\n'
        s += '`-patch`: gets patch notes for past couple of releases\n'
        s += '`-hello`: hey :)\n'
        s += '`-totallog`: gets the tracked minutes in voice\n'
        s += '`-todaylog`: gets the tracked minutes for the day\n'
        s += '`-weeklog`: amount of time logged for the last 7 days\n'
        s += '`-mylog`: some cool stats\n'
        s += '`-rob`: :-)\n'

        return s

    def getRandomCompliment(self):
        """
        Fun little script that returns a random compliment

        Returns
        ----------
        s (str): Random compliment string
        """

        with open('../data/Compliments.txt') as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        return content[randint(0,99)]
