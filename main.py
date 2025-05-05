# -*- coding: utf-8 -*-
# @Time    : 2025/5/1 5:23
# @File    : main.py
# @Author  : Explore
# @Email   : 1989397949@qq.com

import tkinter as tk
import os
from tkinter import messagebox

class App:
    def __init__(self):
        with open("gold_achievement.txt", "r") as f: # 读取成就列表
            self.gold_list = f.readlines() # 读取金子列表
            self.gold_list = [int(i.strip()) for i in self.gold_list] # 读取金子列表并转换为 int 类型
        self.gold_list.sort() # 排序金子列表
        self.gold = 0 # 当前拥有的金子
        self.gold_window = tk.Tk() # 创建窗口
        self.gold_window.title('gold') # 设置窗口标题
        self.gold_window.geometry('300x200+%d+%d' % ((self.gold_window.winfo_screenwidth() - 300) / 2, (self.gold_window.winfo_screenheight() - 300) / 2)) # 设置窗口位置
        self.gold_window.iconbitmap('icon.ico') # 设置图标
        self.gold_window.resizable(False, False) # 禁止调整窗口大小
        self.gold_window.bind('<Configure>', lambda event: self.load("gold.txt")) # 调整窗口大小时保存存档
        self.gold_window.protocol("WM_DELETE_WINDOW", self.exit_app) # 关闭窗口时保存存档

        self.load("gold.txt") # 读取存档

        self.gold_window.grid_rowconfigure(0, weight = 1)
        self.gold_window.grid_rowconfigure(1, weight = 0)
        self.gold_window.grid_columnconfigure(0, weight = 1)

        self.gold_number = tk.Label(self.gold_window, text = '') # 显示当前拥有的金子
        self.font_size(self.gold_number)
        self.gold_number.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)

        self.gold_button = tk.Button(self.gold_window, text = "gold", command = self.gold_press) # 点击 gold 按钮
        self.font_size(self.gold_button)
        self.gold_button.grid(row = 1, column = 0, sticky = tk.N)

        # self.delete_button = tk.Button(self.gold_window, text = "Delete the archive", command = self.delete) # 删除存档
        # self.font_size(self.delete_button)
        # self.delete_button.grid(row = 2, column = 0, sticky = tk.N)

        self.gold_achievement = tk.Label(self.gold_window, text = '') # 成就
        self.font_size(self.gold_achievement)
        self.gold_achievement.grid(row = 3, column = 0, sticky = tk.SE)

        self.gold_window.mainloop()

    def exit_app(self): # 退出程序
        if messagebox.askyesno("退出", "确定要退出吗？"):
            self.save("gold.txt")
            with open(r"C:\ProgramData\Explore\gold.data", "r+") as f:
                f.write("false")
            self.gold_window.quit() # 退出 Tkinter 主循环
            os._exit(0) # 强制退出

    def font_size(self, component, base_font_size = 9, base_width = 300, base_height = 200): # 调整字体大小
        x = self.gold_window.winfo_width() / base_width
        y = self.gold_window.winfo_height() / base_height
        font_size = int(base_font_size * max(x, y))
        component.config(font = ('Segoe UI', font_size))

    def gold_achievement_if(self): # 显示成就
        if self.gold in self.gold_list:
            self.gold_achievement.config(text = f'Achievement! You have {self.gold} gold.')
            self.gold_window.after(1500, lambda: self.gold_achievement.config(text = ''))
            # 彩蛋
            if self.gold == 15231013:
               messagebox.showinfo('Birthday!', 'Oh, my god! Happy birthday! Furina!') # 作者同学要求加的
               
    def gold_press(self): # 点击 gold 按钮
        self.gold += 1
        self.gold_number.config(text = f'Have {self.gold} gold now.')
        self.save("gold.txt")
        self.gold_achievement_if()

    def load(self, file_path): # 读取存档
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    self.gold = int(f.readline())
            except Exception as e:
                messagebox.showerror('Error', f'Error loading data: {e}')
                messagebox.showerror('Error', 'Attempting to overwrite data.')
                self.delete("gold.txt")
                self.gold = 0

    def save(self, file_path): # 保存存档
        try:
            with open(file_path, 'w') as f:
                f.write(str(self.gold))
        except Exception as e:
            messagebox.showerror('Error', f'Error saving data: {e}')

    def delete(self, file_path): # 删除存档
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                self.gold = 0
                self.gold_number.config(text = f'Have {self.gold} gold now.')
            except Exception as e:
                messagebox.showerror('Error', f'Error deleting data: {e}')
        else:
            messagebox.showinfo('Error', 'File deleted.')

if __name__ == '__main__':
    app = App()