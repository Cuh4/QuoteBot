# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Slash Commands Init
# // ---------------------------------------------------------------------

def start():
    # importing the commands will automatically start them
    # is this a good way to do things? probably not
    from .getRandomQuote import command as _
    from .getRandomUserQuote import command as _
    from .quote import command as _
    from .restart import command as _
    from .searchQuote import command as _