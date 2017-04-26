import sys

import EventManager
import Model.Model as model
import View.View as view
import Controller.Controller as controller

def main(argv):
    evManager = EventManager.EventManager()
    gamemodel = model.GameEngine(evManager, argv[1:])
    keyboard = controller.Keyboard(evManager, gamemodel)
    graphics = view.GraphicalView(evManager, gamemodel)
    gamemodel.run()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))