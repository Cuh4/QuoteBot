# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Events Init
# // ---------------------------------------------------------------------

# // ---- Imports
from helpers.general import events as _events

# // Main
class events:
    on_message = _events.event("message_event").save()
    on_ready = _events.event("on_ready").save()
    
# // ---- Import event handlers
# we do this after loading the events otherwise shit goes crazy
from . import on_message
from . import on_ready