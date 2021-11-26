import curses
from curses import wrapper
import time # 因為 wpm 計算速度需要有時間因子，故載入 time

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

    # 在頁面中顯示 wpm 計速表
    # 位置放在第二行第一位元，所以是 (1, 0, ...)
    stdscr.addstr(1, 0, f'WPM: {wpm}')

    # 逐一顯示用戶所輸入的字符
    # 運用 enumerate 將每個字符剛好配合 addstr 的 i 位置，產生文字覆蓋效果
    for i, character in enumerate(current):
        
        #建立逐字正確答案字符
        correct_charater = target[i]
        # 只要正確時，顯示綠色(常駐)
        color = curses.color_pair(1)
        # 若輸入的文字不正確，顯示紅色
        if character != correct_charater:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, character, color)

# 建立打字畫面
def wpm_test(stdscr):
    # 建立打字測試字符串
    target_text = "Hello, this is some test text for this app. Please typing as soon as possible."

    # 創建一個收集字符的 list
    current_text = []

    # 建立 wpm 測速效果
    wpm = 0 

    # 建立開始打字時間點 start_time
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        # 經過時間 time_elapsed = 當前時間 - 打字時間點 start_time
        # 用 max 取大小的原因是當 time_elapsed == 0 時 wpm 的公式會出現除以零的現象導致系統錯誤
        time_elapsed = max(time.time() - start_time, 1)
        # 因為 time.time() 只會顯示當前時間，它會一直做改變。
        # 運用此特性就能在時間線上做兩個標記
        # 第一個標記為開始打字時間 start_time 第二個標記為當前時間 time.time()

        # 建立打字測速公式（簡單建立，並非精準，因為重點不在於建立嚴謹的數學公式）
        # 用 round 讓數字保持整數
        wpm = round((len(current_text)) / (time_elapsed / 60) / 5)

        # 進入打字畫面後馬上清空畫面
        stdscr.clear()
        
        # 將文字覆蓋效果放入
        display_text(stdscr, target_text, current_text, wpm)

        stdscr.refresh()

        # 運用 "".join() 效果為產生一個字符串
        # 因為 current_text 會逐字輸入，所以 "".join(current_text) 中的 "" 也會逐漸變多
        # 當 "".join(current_text) 完全等於 target_text 時，產生結束遊戲效果：
        if "".join(current_text) == target_text:
            # 停止計時
            stdscr.nodelay(False)
            # 跳出回圈 while True:
            # 跳出 while True: 意味著結束 wpm_test()，城市就會
            break

        # try 當用戶有輸入字符時 key = stdscr.getkey() 屏且繼續後續程式碼 if ord(key) == 27:...等
        try:
            # 收集用戶輸入的字符，並放入 current_text 中
            key = stdscr.getkey()
        # 若用戶沒有輸入字符，時間依舊繼續 stdscr.nodelay(True) 但會 continue 跳過後續的程式碼，返回 while True: 進入下一個回圈
        except:
            continue

        # 按下鍵盤 esc鍵 或 左鍵後退出遊戲 
        if ord(key) == 27:
            break

        # 按下 back delete 時會產生刪除效果
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            # 刪除的同時把被刪除字元一同從 current_text list 裡面剔除
            if len(current_text) > 0:
                current_text.pop()
        # 若當前字符長度 len(current_text) 小於打字測試字符長度 len(target_text)
        elif len(current_text) < len(target_text):
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
