import pygame

from EventManager import *
from Model.GameObject import *
from Model.StateMachine import *

class GameEngine(object):
    """
    Tracks the game state.
    """
    def __init__(self, evManager, AIList):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
            running (bool): True while the engine is online. Changed via Event_Quit().
            state (StateMachine()): control state change, stack data structure.
            AIList (list.str): all AI name list.
            player (list.player()): all player object.
            TurnTo (int): current player
        """
        self.evManager = evManager
        evManager.RegisterListener(self)

        self.running = False
        self.state = StateMachine()
        self.AIList = AIList
        self.player = []
        self.TurnTo = 0

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """
        if isinstance(event, Event_Initialize):
            self.SetAI()
        if isinstance(event, Event_Quit):
            self.running = False
        if isinstance(event, Event_StateChange):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.evManager.Post(Event_Quit())
            else:
                # push a new state on the stack
                self.state.push(event.state)
        if isinstance(event, Event_Input):
            pass

    def SetAI(self):
        for i in range(2):
            if self.AIList[i]:
                self.player.append( player( self.AIList[i] ) )

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(Event_Initialize())
        self.state.push(STATE_MENU)
        while self.running:
            newTick = Event_EveryTick()
            self.evManager.Post(newTick)