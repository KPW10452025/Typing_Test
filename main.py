import curses
from curses import wrapper

# 建立開始畫面
def start_screen(stdscr):
    # 清空畫面
    stdscr.clear()

    # 在 stdscr 添加文字：語法 .addstr(空幾行, 空幾個字符, "內容", 使用樣式聲明)
        # 空幾行：0 表內容會出現在第一行、1 表內容會空一行後出現在第二行
        # 空幾個字符：0 表內容會出現在該行第一個字符位、1 容會空一個字符後出現在該行第二個字符位
        # 內容：會出現在 stdscr 上面的內容
        # 使用樣式聲明：curses.color_pair(聲明編號)
    stdscr.addstr(0, 0, "Welcome Typing Speed Test! ", curses.color_pair(3))
    stdscr.addstr(1, 0, "Press Any Key To Begin! ", curses.color_pair(1))

    # 刷新頁面，讓 stdscr.addstr 內容生效
    stdscr.refresh()

    # 用戶輸入任意馬後結束程式
    stdscr.getkey()

# 建立文字覆蓋效果
def display_text(stdscr, target, current, wpm=0):
    # 顯示字符串
    stdscr.addstr(target)

    # 逐一顯示用戶所輸入的字符
    # 運用 enumerate 將每個字符剛好配合 addstr 的 i 位置，產生文字覆蓋效果
    for i, character in enumerate(current):
        stdscr.addstr(0, i, character, curses.color_pair(1))

# 建立打字畫面
def wpm_test(stdscr):
    # 建立打字測試字符串
    target_text = "Hello, this is some test text for this app. Please typing as soon as possible."

    # 創建一個收集正確字符的 list
    current_text = []

    while True:
        # 進入打字畫面後馬上清空畫面
        stdscr.clear()
        
        # 將文字覆蓋效果放入
        display_text(stdscr, target_text, current_text)

        stdscr.refresh()

        # 收集用戶輸入的字符，並放入 current_text 中
        key = stdscr.getkey()

        # 按下鍵盤 esc鍵 或 左鍵後退出遊戲 
        if ord(key) == 27:
            break

        # 按下 back delete 時會產生刪除效果
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            # 刪除的同時把被刪除字元一同從 current_text list 裡面剔除
            if len(current_text) > 0:
                current_text.pop()
        else:
            # 用戶每輸入字元都會將字元放入 current_text list
            current_text.append(key)

# stdscr: standard output screen
def main(stdscr):

    # 樣式聲明
    # curses.init_pair(編號, curses.COLOR_文字顏色, curses.COLOR_背景顏色)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    wpm_test(stdscr)

wrapper(main)
