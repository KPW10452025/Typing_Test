import curses
from curses import wrapper

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome Typing Speed Test! ", curses.color_pair(3))
    stdscr.addstr("\nPress Any Key To Begin! ", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getkey()

# stdscr: standard output screen
def main(stdscr):

    # 樣式聲明
    # curses.init_pair(編號, curses.COLOR_文字顏色, curses.COLOR_背景顏色)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)

wrapper(main)
