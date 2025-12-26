import sys
import os
import random

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu,
)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QAction


def resource_path(relative_path: str) -> str:
    """
    PyInstaller 兼容资源路径
    """
    try:
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class DesktopPet(QLabel):
    def __init__(self):
        super().__init__()

        # ===== 窗口属性 =====
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ===== 加载图片帧 =====
        self.frames = [
            QPixmap(resource_path("assets/stand/1.png")),  # 0 睁眼
            QPixmap(resource_path("assets/stand/2.png")),  # 1 半眯1
            QPixmap(resource_path("assets/stand/3.png")),  # 2 半眯2
            QPixmap(resource_path("assets/stand/4.png")),  # 3 闭眼
        ]

        # ===== 默认状态 =====
        self.idle_frame = 0
        self.setPixmap(self.frames[self.idle_frame])
        self.resize(self.frames[self.idle_frame].size())

        # ===== 初始位置 =====
        screen = QApplication.primaryScreen().geometry()
        self.base_x = (screen.width() - self.width()) // 2
        self.base_y = (screen.height() - self.height()) // 2
        self.move(self.base_x, self.base_y)

        # ===== 拖拽 =====
        self.drag_pos = QPoint()

        # ===== 眨眼动画 =====
        self.blink_sequence = [0, 1, 2, 3, 2, 1, 0]
        self.blink_intervals = [0, 30, 20, 60, 20, 40, 0]
        self.blink_index = 0
        self.is_blinking = False
        self.blink_repeat_total = 1   # 本轮要眨几次
        self.blink_repeat_count = 0   # 已眨次数


        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.start_blink)
        self.schedule_next_blink()

        # ===== 右键菜单 =====
        self.init_context_menu()

    # ===============================
    # 眨眼逻辑
    # ===============================
    def schedule_next_blink(self):
        delay = random.randint(2000, 5000)
        self.blink_timer.start(delay)

    def start_blink(self):
        if self.is_blinking:
            return

        self.is_blinking = True
        self.blink_repeat_total = random.choice([1, 2])  # 快速眨 1 或 2 次
        self.blink_repeat_count = 0

        self.blink_index = 0
        self.play_blink_frame()


    def play_blink_frame(self):
        frame = self.blink_sequence[self.blink_index]
        self.setPixmap(self.frames[frame])

        interval = self.blink_intervals[self.blink_index]
        self.blink_index += 1

        if self.blink_index >= len(self.blink_sequence):
            self.blink_repeat_count += 1

            if self.blink_repeat_count < self.blink_repeat_total:
                # 很短的停顿后再眨一次
                self.blink_index = 0
                QTimer.singleShot(
                    random.randint(80, 120),
                    self.play_blink_frame
                )
                return
            else:
                # 所有眨眼完成
                self.is_blinking = False
                self.setPixmap(self.frames[self.idle_frame])
                self.schedule_next_blink()
                return
        QTimer.singleShot(interval, self.play_blink_frame)

    # ===============================
    # 拖拽
    # ===============================
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_pos
            self.base_x = new_pos.x()
            self.base_y = new_pos.y()
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        pass

    # ===============================
    # 右键菜单
    # ===============================
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
        print("点击了：设置（占位）")

    def on_exit(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
