import pygame

import Model.Model as model
from EventManager import *

class Keyboard(object):
    """
    Handles keyboard input.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_EveryTick):
            # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():
                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.evManager.Post(Event_Quit())
                # handle key down events
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.evManager.Post(Event_StateChange(None))
                else:
                    cur_state = self.model.state.peek()
                    if cur_state == model.STATE_MENU:
                        self.ctrl_menu(event)
                    if cur_state == model.STATE_PLAY:
                        self.ctrl_play(event)
                    if cur_state == model.STATE_HELP:
                        self.ctrl_help(event)

    def ctrl_menu(self, event):
        """
        Handles menu key events.
        """
        if event.type == pygame.KEYDOWN:
            # escape pops the menu
            if event.key == pygame.K_ESCAPE:
                self.evManager.Post(Event_StateChange(None))
            # space plays the game
            if event.key == pygame.K_SPACE:
                self.evManager.Post(Event_StateChange(model.STATE_PLAY))

    def ctrl_help(self, event):
        """
        Handles help key events.
        """
        if event.type == pygame.KEYDOWN:
            # space, enter or escape pops help
            if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
                self.evManager.Post(Event_StateChange(None))

    def ctrl_play(self, event):
        """
        Handles play key events.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # escape pops the menu
                self.evManager.Post(Event_StateChange(None))
            # F1 shows the help
            elif event.key == pygame.K_F1:    
                self.evManager.Post(Event_StateChange(model.STATE_HELP))
            else:
                self.evManager.Post(Event_Input(event.key, None))