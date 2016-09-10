# Dumb AI, randomly choice from possible actions
import sys
sys.path.insert(0, '~/Dropbox/SideProjects/snake')

import random
from game import SnakeGame

class AIRandomWalk:
    def __init__(self):
        self.ai = None
    
    def getAction(self, state):
        return random.choice(state.getPossibleActions())

if __name__ == '__main__':
    game = SnakeGame.Game(ai_object=AIRandomWalk)
    print game.run()
