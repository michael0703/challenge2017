import sys

import EventManager
import Model.main as model
import View.main as view
import Controller.main as controller

def main(argv):
    evManager = EventManager.EventManager()
    gamemodel = model.GameEngine(evManager, argv[1:])
    Control = controller.Control(evManager, gamemodel)
    graphics = view.GraphicalView(evManager, gamemodel)
    gamemodel.run()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))