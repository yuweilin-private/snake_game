# Author: Yu-Wei Lin
# Updated: 2016/09/07

from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

class SnakeAI:
    def __init__(self, win_size):
        self.win_size = win_size
        self.path = []

    def getAction(self, food, snake):
        def action(next_pos, head):
            ''' return the action (RIGHT, LEFT, UP, DOWN)
            '''
            if next_pos[0] == head[0]:
                return KEY_RIGHT if next_pos[1]>head[1] else KEY_LEFT
            return KEY_DOWN if next_pos[0]>head[0] else KEY_UP

        def toFood(snake):
            ''' generator, return a path to food.
            '''
            if snake[0] == 

        def isClean(snake):
            ''' check if the empty space is connected.
            '''
            pass

        if len(self.path) == 0:
            for path in toFood(snake):
                if isClean(path):
                    self.path = path[::-1]
                    break
        return action(self.path.pop(), snake[0])
