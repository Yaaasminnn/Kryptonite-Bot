import datetime

#add in ansi colour codes

def logMsg(message):
    """
    Logs messages by printing them and giving us the datetime.

    :param message: message we want to print
    """

    now = datetime.datetime.now().replace(microsecond=0)
    print(f"[{now}]: {message}")
