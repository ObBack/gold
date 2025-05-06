import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QPushButton, QLabel)
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('./ui/main.ui')
        self.setWindowTitle('Gold')
        self.setCentralWidget(self.ui)
        self.setFixedSize(200, 200)
        self.setWindowIcon(QIcon("./icon.ico"))
        self.ver = "v_1.0.2"
        self.load_achievement_list()

        self.gold_button = self.findChild(QPushButton, 'gold_button')
        self.gold_label = self.findChild(QLabel, 'gold_label')
        self.ver_label = self.findChild(QLabel, 'ver')

        self.gold_button.clicked.connect(self.add_gold)
        self.ver_label.setText(self.ver)

        self.load_data("gold.txt")
        self.update_display()

    def load_achievement_list(self):  # 加载成就列表
        try:
            with open("gold_achievement.txt", "r") as f:
                self.gold_list = [int(line.strip()) for line in f if line.strip()]
                self.gold_list.sort()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"加载成就列表失败: {str(e)}")

    def update_display(self):  # 更新界面显示
        self.gold_label.setText(f"Gold: {self.gold}")

    def add_gold(self):  # 增加金币
        self.gold += 1
        self.update_display()
        self.save_data("gold.txt")
        self.check_achievement()

    def check_achievement(self):  # 检查成就
        if self.gold in self.gold_list:
            self.achievement_label.setText(f"Achievement! {self.gold} Gold!")
            QTimer.singleShot(1500, lambda: self.achievement_label.setText(""))
            
            if self.gold == 15231013:  # 彩蛋
                QMessageBox.information(self, "Birthday!", "Happy birthday! Furina!")

    def load_data(self, filename):  # 加载存档
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    self.gold = int(f.read())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"加载存档失败: {str(e)}")
            self.gold = 0

    def save_data(self, filename):  # 保存存档
        try:
            with open(filename, "w") as f:
                f.write(str(self.gold))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"保存失败: {str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()