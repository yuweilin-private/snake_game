#!/bin/python
# Wrapper for snake game
# Downloaded From https://gist.github.com/sanchitgangwar/2158089
# Edit: Yu-Wei Lin
# Updated: 2016/9/1

import time
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

class Game:
    '''
        - ai: constuctor takes parameter 'win_size'
            -- has method 'getAction', takes params (food, snake)
    '''
    def __init__(self, is_human = True, ai = None,
            is_show_win=True, win_size = (20,60),
            init_food = None, init_snake = None, init_key=None,
            start_pause = 0.15, min_pause = 0.03, length_pause_ratio = 0.001
        ):
        # game variables
        self.score = 0
        self.snake = [(4,10), (4,9), (4,8)] if init_snake is None else init_snake
        self.food = (10,20) if init_food is None else init_food
        self.key = KEY_RIGHT if init_key is None else init_key

        # game setup
        self.is_human = is_human
        self.AI = ai
        self.is_show_win = is_show_win
        self.win_size = win_size
        
        # variables for pause time, pause = max(start-ratio*length, min_pause)
        self.start_pause = start_pause
        self.min_pause = min_pause
        self.length_pause_ratio = length_pause_ratio

    def run(self):
        if self.is_show_win:
            curses.initscr()
            win = curses.newwin(self.win_size[0], self.win_size[1], 0, 0)
            win.keypad(1)
            curses.noecho()
            curses.curs_set(0)
            win.border(0)
            win.nodelay(1)
        
        if self.AI is not None:
            self.ai = self.AI(self.win_size)

        while self.key != 27:   # jump out of game when press ESC
            if self.is_show_win:    # draw the layout
                win.border(0)
                win.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
                win.addstr(0, 27, ' SNAKE ')
            # pause
            time.sleep(max(self.min_pause, self.start_pause-self.length_pause_ratio*len(self.snake)))

            # action
            pre_key = self.key
            if self.is_human:
                event = win.getch()
                self.key = self.key if event==-1 else event
                if self.key == ord(' '):
                    self.key = -1
                    while self.key != ord(' '):
                        self.key = win.getch()
                    self.key = preKey
                    continue
            else:
                event = win.getch()
                if event == 27:
                    break
                self.key = self.ai.getAction(self.food, self.snake)

            if self.key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:  # if an invalid key is pressed
                self.key = pre_key
            
            # calculate the new coordinates of the head of the snake. 
            # NOTE: len(snake) increases. This will be taken care of later 
            self.snake.insert(0, 
                    (self.snake[0][0] + (self.key==KEY_DOWN and 1) + (self.key==KEY_UP and -1),
                     self.snake[0][1] + (self.key==KEY_RIGHT and 1) + (self.key==KEY_LEFT and -1)))

            # Exit if snake crosses the boundaries
            if self.snake[0][0]==0 or self.snake[0][0]==self.win_size[0]-1 or \
                self.snake[0][1]==0 or self.snake[0][1]==self.win_size[1]-1:
                break

            # Exit if snake runs over itself
            if self.snake[0] in self.snake[1:]: break
            
            # If snake eats the food
            last = None
            if self.snake[0]==self.food:
                self.food = []
                self.score += 1
                while len(self.food)==0:
                    self.food = (randint(1, self.win_size[0]-2), randint(1, self.win_size[1]-2))
                    if self.food in self.snake: self.food = []
            else:
                last = self.snake.pop()
            
            # draw the snake and the food
            if self.is_show_win:
                win.addch(self.food[0], self.food[1], '*')
                if last is not None:
                    win.addch(last[0], last[1], ' ')
                win.addch(self.snake[0][0], self.snake[0][1], '#')
        # curses.endwin()
        print("Score: {0}\n".format(self.score))
        return self.score

from snake_ai import SnakeAI
if __name__ == "__main__":
    game = Game(ai=SnakeAI, is_human=False, start_pause=0.03)
    game.run()
