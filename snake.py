import curses
from curses import textpad
import random
def create_food(snake,box):
    food=None
    while food is None:
        food = [random.randint(box[0][0]+1,box[1][0]-1),
            random.randint(box[0][1]+1,box[1][1]-1)]
        if food in snake:
            food = None
    return food
def print_score(stdscr,score):
    sh,sw=stdscr.getmaxyx()
    score_text = "Score: {}".format(score)
    stdscr.addstr(0,sw//2-len(score_text),score_text)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(150)
    sh,sw = stdscr.getmaxyx()
    box=[[3,3],[sh-3,sw-3]]
    textpad.rectangle(stdscr,box[0][0],box[0][1],box[1][0],box[1][1])
    snake=[[sh//2,sw//2+1],[sh//2,sw//2],[sh//2,sw//2-1]]
    direction=curses.KEY_RIGHT
    for y,x in snake:
        stdscr.addstr(y,x,'#')

    food = create_food(snake,box)
    stdscr.addstr(food[0],food[1],'*')

    score=0
    print_score(stdscr,score)
    
    while(1):
        key=stdscr.getch()
        if key in [curses.KEY_RIGHT,curses.KEY_LEFT,curses.KEY_UP,curses.KEY_DOWN]:
            direction = key
        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head =[head[0],head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head =[head[0],head[1]-1]
        elif direction == curses.KEY_UP:
            new_head =[head[0]-1,head[1]]
        elif direction == curses.KEY_DOWN:
            new_head =[head[0]+1,head[1]]
        snake.insert(0,new_head)
        stdscr.addstr(new_head[0],new_head[1],'#')
        if snake[0] == food:
            food = create_food(snake,box)
            stdscr.addstr(food[0],food[1],'@')
            score+=1
            print_score(stdscr,score)
        else:
            stdscr.addstr(snake[-1][0],snake[-1][1],' ')
            snake.pop()
        if score>5 and score<=10:
            stdscr.timeout(100)
        if score>10 and score<=20:
            stdscr.timeout(75)
        if score>20:
            stdscr.timeout(50)
        
        if (snake[0][0] in [box[0][0],box[1][0]] or
            snake[0][1] in [box[0][1],box[1][1]] or
            snake[0] in snake[1:]):
            msg = "Game Over!"
            stdscr.addstr(sh//2,sw//2-len(msg)//2,msg)
            stdscr.nodelay(0)
            stdscr.getch()
            break
        stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
