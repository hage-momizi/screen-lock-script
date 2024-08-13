import tkinter as tk
import ctypes
import time
import threading
from pynput import mouse, keyboard

# マウスとキーボードの操作を監視するためのフラグ
activity_detected = False

def on_move(x, y):
    global activity_detected
    activity_detected = True

def on_click(x, y, button, pressed):
    global activity_detected
    activity_detected = True

def on_scroll(x, y, dx, dy):
    global activity_detected
    activity_detected = True

def on_key_press(key):
    global activity_detected
    activity_detected = True

def countdown_and_lock():
    global activity_detected

    # GUIウィンドウを作成
    root = tk.Tk()
    root.title("カウントダウン")
    root.geometry("400x200")
    
    label = tk.Label(root, text="", font=("Arial", 48))
    label.pack(pady=50)
    
    root.attributes("-topmost", True)  # ウィンドウを最前面に
    root.attributes("-fullscreen", True)  # フルスクリーン表示

    # カウントダウンを表示する関数
    def update_countdown(count):
        if count > 0:
            label.config(text=str(count))
            root.after(1000, update_countdown, count - 1)
        else:
            label.config(text="")  # カウントダウン終了後にテキストを消去
            root.attributes("-fullscreen", False)  # フルスクリーンを解除
            root.update()
            start_activity_monitor()

    def start_activity_monitor():
        global activity_detected
        while True:
            if activity_detected:
                # アクティビティが検出された場合にロック画面に移動
                ctypes.windll.user32.LockWorkStation()
                # ソフトウェアを終了
                root.quit()
                break
            time.sleep(0.1)

    # カウントダウンを開始
    update_countdown(3)

    # マウスとキーボードのリスナーを開始
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_key_press)

    mouse_listener.start()
    keyboard_listener.start()

    # GUIメインループの開始
    root.mainloop()

    # リスナーを停止
    mouse_listener.stop()
    keyboard_listener.stop()

if __name__ == "__main__":
    countdown_and_lock()
