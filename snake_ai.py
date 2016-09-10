# Author: Yu-Wei Lin
# Updated: 2016/09/07

from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

class SnakeAI:
    def __init__(self, win_size=(20,60)):
        self.win_size = win_size
        self.path = []

    def getAction(self, food, snake):
        def action(next_pos, head):
            ''' return the action (RIGHT, LEFT, UP, DOWN)
            '''
            if next_pos[0] == head[0]:
                return KEY_RIGHT if next_pos[1]>head[1] else KEY_LEFT
            return KEY_DOWN if next_pos[0]>head[0] else KEY_UP
        
        def manhattanDistance(p1, p2):
            return sum([abs(x-y) for x, y in zip(p1, p2)])

        actions = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]
        def toFood(snake):
            ''' generator, return a path to food.
            '''
            if snake[0] == food:
                yield []
            
            points = [(snake[0][0] + (action==KEY_DOWN and 1) + (action==KEY_UP and -1), \
                       snake[0][1] + (action==KEY_RIGHT and 1) + (action==KEY_LEFT and -1)) \
                       for action in actions]
            points.sort(key=lambda x: manhattanDistance(x, food))
            
            for next_point in points:
                if next_point not in snake \
                    and next_point[0]!=0 and next_point[0]!=self.win_size[0]-1 \
                    and next_point[1]!=0 and next_point[1]!=self.win_size[1]-1:
                    for p in toFood([next_point]+snake[:-1]):
                        yield [next_point] + p
            # return None if all paths are explored
            yield None

        def isClean(snake):
            ''' check if the empty space is connected.
            '''
            return True

        if len(self.path) == 0:
            for path in toFood(snake):
                if isClean((path+snake)[:len(snake)]):
                    self.path = path[::-1]
                    break
        return action(self.path.pop(), snake[0])

if __name__ == "__main__":
    ai = SnakeAI()
    print ai.getAction((10,20), [(4,10), (4,9), (4,8)])
    print ai.path
