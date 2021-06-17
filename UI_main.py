# coding=UTF-8
import des_mode as dm
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import os
import time
from threading import Thread
from random import *

#宣告變數
ui_is_done = False
FILE = ''

# ==================== 確認檔案是否完整生成 ==================
def getSize(filename):
    if os.path.isfile(filename): 
        st = os.stat(filename)
        return st.st_size
    else:
        return -1

def wait_finish(file_path):
    global loading_is_Done
    current_size = getSize(file_path)
    while current_size !=getSize(file_path) or getSize(file_path)==0:
        current_size =getSize(file_path)
        time.sleep(100)
    print("output.txt is Done!")
# ===========================================================

# ==================== 按鈕事件 =============================
# 選擇檔案 (按鈕事件)
def choose_file():
    global FILE,ui_is_done
    if ui_is_done:
        file = filedialog.askopenfilename(title = '選擇明文文本',filetypes = [('text','*.txt')])
        FILE = file
        if file != '':
            file_path.configure(text=file)
            f = open(file, 'r', encoding='utf-8')
            text = f.read(700)
            f.close()
            file_text.configure(state='normal')
            file_text.delete('1.0',"end")
            file_text.insert('1.0', text)
            file_text.configure(state='disable')
        else:
            file_path.configure(text='尚未開啟檔案...')

# 輸入檔案路徑開啟 (按鈕事件)
def open_input_file_window():
    global ui_is_done
    if ui_is_done:
        if FILE != '':
            idx = FILE.rfind("/") 
            os.startfile(FILE[:idx])
        else:
            messagebox.showinfo("Pop up", "請先選擇檔案")

# 輸出檔案路徑開啟 (按鈕事件)
def open_output_file_window():
    global ui_is_done
    if ui_is_done:
        os.startfile(os.path.dirname(os.path.abspath(__file__)) + './result')

# 執行 DES (按鈕事件)
def DES_go():
    try:
        t = Thread(target=DES_main)
        t.start()
        output_text.configure(state='normal')
        output_text.delete('1.0',"end")
        output_text.insert('1.0', '資料'+combo2.get()+'中。。。請勿關閉視窗!')
        output_text.configure(state='disable')

    except:
        messagebox.showinfo("Pop up", "加解密執行緒執行錯誤")

# 隨機 key 生成器 (按鈕事件)
def rand_key():
    randomKey =  "".join([choice("0123456789ABCDEF") for i in range(8)])     
    key_entry.delete(0,"end")
    key_entry.insert(0, randomKey)  
    f = open('key.txt', 'w', encoding='utf-8')
    f.write(randomKey)
    f.close()  
# ===========================================================

# ==================== 監聽事件 =============================
#當輸入的 key 改變時 (key輸入欄位監聽事件)
def text_changed(event):
    global ui_is_done
    if ui_is_done:
        t = text.get().strip()
        f = open('key.txt', 'w', encoding='utf-8')
        f.write(t)
        f.close()
# ===========================================================

# DES執行函式
def DES_main():
    global FILE,ui_is_done
    if ui_is_done:
        if len(key_entry.get()) == 8:
            if FILE != '':
                try:
                    mode=combo1.get()
                    if combo2.get() == '加密':
                        dm.DES(FILE, 'enc',mode)
                        file_path = os.path.dirname(os.path.abspath(__file__)) + '/result/Cipher_output.txt'
                        wait_finish(file_path)
                        f = open(file_path, 'r', encoding='utf-8')
                        text = f.read(1000)
                        f.close()
                        output_text.configure(state='normal')
                        output_text.delete('1.0',"end")
                        output_text.insert('1.0', text)
                        output_text.configure(state='disable')
                    else:
                        dm.DES(FILE, 'dec',mode)
                        file_path = os.path.dirname(os.path.abspath(__file__)) + '/result/Decrypt_output.txt'
                        wait_finish(file_path)
                        f = open(file_path, 'r', encoding='utf-8')
                        text = f.read(1000)
                        f.close()
                        output_text.configure(state='normal')
                        output_text.delete('1.0',"end")
                        output_text.insert('1.0', text)
                        output_text.configure(state='disable')
                except:
                    output_text.configure(state='normal')
                    output_text.delete('1.0',"end")
                    output_text.configure(state='disable')
                    messagebox.showinfo("Pop up", "操作失敗，可能源自於編碼錯誤")
                
            else:
                output_text.configure(state='normal')
                output_text.delete('1.0',"end")
                output_text.configure(state='disable')
                messagebox.showinfo("Pop up", "請先選擇檔案")
        else:
            output_text.configure(state='normal')
            output_text.delete('1.0',"end")
            output_text.configure(state='disable')
            messagebox.showinfo("Pop up", "金鑰請輸入8個字元")

# ============================ UI編排 ================================= 
if __name__ == '__main__':

    #自動生成 result資料夾 跟 key.txt
    path = './result'
    if not os.path.isdir(path):
        os.makedirs(path)
    path = 'key.txt'
    if not os.path.isfile(path):
        f = open(path, 'w')
        f.close()

    #主視窗創建
    window = tk.Tk()
    window.title('DES')
    window.geometry('500x800')
    window.resizable(width=0, height=0)

    #創建各分區與相應 UI元件
    '''
    UI部分由八個分區(frame)組成，此八個分區由上而下排列:
    1. 檔案選擇
    2. key輸入與隨機生成
    3. 模式 與 加解密選擇
    4. 預覽提示文字 與 開啟檔案夾按鈕 
    5. 代處理文件預覽區
    6. 執行按鈕
    7. 預覽提示文字 與 開啟檔案夾按鈕
    8. 已處裡文件預覽區
    '''
    frame1 = tk.Frame(window)
    frame1.grid(row=0, column=0, sticky='w')
    tk.Button(frame1,text='選擇檔案', command=choose_file).pack(side='left',pady=10,padx=10)
    file_path = tk.Label(frame1, text='尚未開啟檔案...')
    file_path.pack(side='left')

    frame2 = tk.Frame(window)
    frame2.grid(row=1, column=0, sticky='w')
    tk.Label(frame2, text='Key：').pack(side='left',pady=5,padx=10)
    text = tk.StringVar()
    key_entry = tk.Entry(frame2, font=('Arial', 12), textvariable=text)
    key_entry.bind('<KeyRelease>', text_changed)
    key_entry.pack(side='left')
    tk.Button(frame2,text='隨機生成',command=rand_key).pack(side='left',padx=10, pady=5)
    tk.Label(frame2, text='(必須為8字元)').pack(side='left',pady=5,padx=10)

    frame3 = tk.Frame(window)
    frame3.grid(row=2, column=0, sticky='w')
    tk.Label(frame3, text='模式：').pack(side='left',pady=5,padx=10)
    combo1 = ttk.Combobox(frame3,values=['ECB', 'CBC', 'CFB', 'OFB', 'CTR'], state="readonly")
    combo1.pack(side='left')
    combo1.current(0)
    combo2 = ttk.Combobox(frame3,values=['加密','解密'], state="readonly")
    combo2.pack(side='left',padx=10)
    combo2.current(0)

    frame4 = tk.Frame(window)
    frame4.grid(row=3, column=0, sticky='w')
    tk.Label(frame4, text='文檔預覽(預覽1000字)：   ').pack(side='left',padx=10)
    tk.Button(frame4,text='開啟檔案位置',command=open_input_file_window).pack(side='left',padx=10, pady=5)

    frame5 = tk.Frame(window)
    frame5.grid(row=4, column=0, sticky='w')
    file_text = tk.Text(frame5, height=15, width=52, highlightbackground='black', font=('Arial', 12), state='disabled')
    file_text.pack(padx=10)

    frame6 = tk.Frame(window)
    frame6.grid(row=5, column=0,)
    go_bin = tk.Button(frame6,text='執行 ↯', font=(20), command=DES_go)
    go_bin.pack(pady=5)

    frame7 = tk.Frame(window)
    frame7.grid(row=6, column=0, sticky='w')
    tk.Label(frame7, text='輸出預覽(預覽1000字)：   ').pack(side='left', padx=10)
    tk.Button(frame7,text='開啟檔案位置', command=open_output_file_window).pack(side='left',padx=10,pady=5)

    frame8 = tk.Frame(window)
    frame8.grid(row=7, column=0, sticky='w')
    output_text = tk.Text(frame8, height=15, width=52, highlightbackground='black', font=('Arial', 12))
    output_text.pack(padx=10)

    ui_is_done = True
    window.mainloop()