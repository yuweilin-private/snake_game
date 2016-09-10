import time
import curses
import random
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

ACTIONS = [KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN]
END_KEY = 27 # ESC

class GameState:
    def __init__(self, win_size, food=None, snake=None, score=0):
        self.win_size = win_size
        self.score = score
        self.food = food if food is not None else \
                random.choice([(x,y) for x in range(1, win_size[0]-1) for y in range(1,win_size[1]-1)])
        self.snake = snake if snake is not None else \
                (random.choice([(x,y) for x in range(win_size[0]//3, win_size[0]//3*2) 
                    for y in range(win_size[1]//3,win_size[1]//3*2) if (x,y)!=self.food]))

    def copy(self):
        return GameState(win_size=self.win_size, food=self.food, snake=self.snake, score=self.score)

    def getEmptySpace(self):
        ''' return the points that are not occupied by the snake.
        '''
        snakeSet = set(self.snake)
        return set([(i, j) for i in range(1, self.win_size[0]-1) for j in range(1, self.win_size[1]-1) \
                      if (i, j) not in snakeSet])

    def getPossibleActions(self):
        return [action for action in ACTIONS if self.copy.nextState(action)]

    def nextState(self, action):
        ''' Update the snake and food based on the given action. 
            return True if the game continues, otherwise False
        '''
        new_head = (self.snake[0][0] + (action==KEY_DOWN and 1) + (action==KEY_UP and -1), \
                    self.snake[0][1] + (action==KEY_RIGHT and 1) + (action==KEY_LEFT and -1))
        if new_head == self.food:
            self.snake = (new_head,) + self.snake
            self.food = random.choice(self.getEmptySpace)
        else:
            self.snake = (new_head,) + self.snake[:-1]
        return (not self.endGame())

    def endGame(self):
        ''' the game ends when snake collides with itself or the walls.
        '''
        return (self.snake[0] in self.snake[1:]) or \
               self.snake[0][0]==0 or self.snake[0][0]==self.win_size[0]-1 or \
               self.snake[0][1]==0 or self.snake[0][1]==self.win_size[1]-1 

class Game:
    def __init__(self, ai_object = None, 
            is_show_win=True, win_size=(20,60),
            food=None, snake = None,
            pause=(0.15, 0.03, 0.001)):

        self.state = GameState(win_size, food, snake)
        self.action = random.choice(self.state.getPossibleActions())

        self.ai_object = ai_object

        self.is_show_win = is_show_win
        self.pause = pause

    def pauseTime(self):
        return self.pause[0] if self.ai_object is not None else \
                max(self.pause[1], self.pause[0]-self.pause[2]*len(self.state.snake))

    def 
