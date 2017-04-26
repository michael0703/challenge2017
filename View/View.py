import pygame

import Model.Model as model
from EventManager import *
from View.ViewConst import *

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """
    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model

        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None
    
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, Event_Initialize):
            self.initialize()
        if isinstance(event, Event_Quit):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        if isinstance(event, Event_EveryTick) and self.isinitialized:
            cur_state = self.model.state.peek()
            if cur_state == model.STATE_MENU:
                self.render_menu()
            if cur_state == model.STATE_PLAY:
                self.render_play()
            if cur_state == model.STATE_HELP:
                self.render_help()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)
    
    def render_menu(self):
        """
        Render the game menu.
        """
        self.screen.fill(Color_White)
        somewords = self.smallfont.render(
                    'You are in the Menu. Space to play. Esc exits.', 
                    True, (0, 255, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()
        
    def render_play(self):
        """
        Render the game play.
        """
        # draw backgound
        self.screen.fill(Color_White)
        pygame.draw.line(self.screen, Color_Blue , (768,0), (768,768), 2)
        pygame.draw.line(self.screen, Color_Black, (256,0), (256,768), 2)
        pygame.draw.line(self.screen, Color_Black, (512,0), (512,768), 2)
        pygame.draw.line(self.screen, Color_Black, (0,256), (768,256), 2)
        pygame.draw.line(self.screen, Color_Black, (0,512), (768,512), 2)

        # draw choose
        for i in range(2):
            player = self.model.player[i]
            for Choose in player.ChooseList:
                if i == 0:
                    pygame.draw.circle(
                        self.screen, Color_Red,
                        (128+Choose[0]*256, 128+Choose[1]*256),
                        100
                    )
                else:
                    pygame.draw.circle(
                        self.screen, Color_Green,
                        (128+Choose[0]*256, 128+Choose[1]*256),
                        100
                    )

        pygame.display.flip()
        
    def render_help(self):
        """
        Render the help screen.
        """
        self.screen.fill(Color_White)
        somewords = self.smallfont.render(
                    'Help is here. space, escape or return.', 
                    True, (0, 255, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()
        
    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """
        result = pygame.init()
        pygame.font.init()
        pygame.display.set_caption(GameCaption)
        self.screen = pygame.display.set_mode(ScreenSize)
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font(None, 40)
        self.isinitialized = True