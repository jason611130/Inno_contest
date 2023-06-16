import tkinter as tk
import time
def plus():
    print("已發送通知請稍後")
    time.sleep(1)
    print("已開啟冷氣")

window = tk.Tk()
window.title('GUI')
window.geometry('380x400')
window.resizable(False, False)


test = tk.Button(text="請求開冷氣",command=plus)
test.pack()
window.mainloop()