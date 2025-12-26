import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu,
)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QAction
#启动命令
# python main.py


def resource_path(relative_path: str) -> str:
    """兼容 PyInstaller / 本地运行"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class DesktopPet(QLabel):
    def __init__(self):
        super().__init__()

        # ===== 窗口设置 =====
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ===== 图片资源（不改动作）=====
        self.frames = [
            QPixmap(resource_path("assets/stand/6.png")),
            QPixmap(resource_path("assets/stand/7.png")),
            QPixmap(resource_path("assets/stand/8.png")),
            QPixmap(resource_path("assets/stand/9.png")),
        ]

        # ===== 动画轨道 =====
        self.sequence = [0, 1, 2, 3, 3, 2, 1, 0]
        self.intervals = [900, 120, 150, 180, 180, 150, 120, 1200]

        self.seq_index = 0

        self.setPixmap(self.frames[0])
        self.resize(self.frames[0].size())

        # ===== 初始位置 =====
        screen = QApplication.primaryScreen().geometry()
        self.base_x = (screen.width() - self.width()) // 2
        self.base_y = (screen.height() - self.height()) // 2
        self.move(self.base_x, self.base_y)

        # ===== 拖拽 =====
        self.drag_pos = QPoint()

        # ===== 动画定时器 =====
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_animation)
        self.timer.start(self.intervals[0])

        # ===== 右键菜单 =====
        self.init_context_menu()

    # ================== 动画 ==================
    def play_animation(self):
        frame_index = self.sequence[self.seq_index]
        self.setPixmap(self.frames[frame_index])

        # 固定位置，不做上下浮动
        self.move(self.base_x, self.base_y)

        self.seq_index = (self.seq_index + 1) % len(self.sequence)
        self.timer.start(self.intervals[self.seq_index])

    # ================== 右键菜单 ==================
    def init_context_menu(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.menu = QMenu(self)

        self.action_settings = QAction("设置", self)
        self.action_exit = QAction("退出", self)

        self.menu.addAction(self.action_settings)
        self.menu.addSeparator()
        self.menu.addAction(self.action_exit)

        self.action_settings.triggered.connect(self.on_settings)
        self.action_exit.triggered.connect(self.on_exit)

    def show_context_menu(self, pos):
        self.menu.exec(self.mapToGlobal(pos))

    def on_settings(self):
        # 先占位，后续你要我可以直接给你写设置窗口
        print("点击了：设置")

    def on_exit(self):
        QApplication.quit()

    # ================== 拖拽 ==================
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_pos
            self.base_x = new_pos.x()
            self.base_y = new_pos.y()
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
