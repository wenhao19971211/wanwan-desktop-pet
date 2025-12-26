import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPixmap


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class DesktopPet(QLabel):
    def __init__(self):
        super().__init__()

        # ===== 窗口设置 =====
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ===== 加载图片（不改动作）=====
        self.frames = [
            QPixmap(resource_path("assets/stand/1.png")),
            QPixmap(resource_path("assets/stand/2.png")),
            QPixmap(resource_path("assets/stand/3.png")),
            QPixmap(resource_path("assets/stand/4.png")),
        ]

        # ===== 动画轨道（顺序 + 停留）=====
        self.sequence = [0, 0, 1, 2, 3, 3, 2, 1, 0]

        # ===== 每一帧的节奏（ms）=====
        self.intervals = [260, 200, 120, 120, 220, 260, 140, 140, 300]

        self.seq_index = 0

        # ===== 显示第一帧 =====
        self.setPixmap(self.frames[0])
        self.resize(self.frames[0].size())

        # ===== 初始位置（防止跑飞）=====
        screen = QApplication.primaryScreen().geometry()
        self.base_x = (screen.width() - self.width()) // 2
        self.base_y = (screen.height() - self.height()) // 2
        self.move(self.base_x, self.base_y)

        # ===== 拖拽 =====
        self.drag_pos = QPoint()

        # ===== 定时器 =====
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_animation)
        self.timer.start(self.intervals[0])

    def play_animation(self):
        frame_index = self.sequence[self.seq_index]
        self.setPixmap(self.frames[frame_index])

        # ===== 伪缓动（极轻微上下浮动）=====
        offset_map = {
            0: 0,
            1: 1,
            2: 2,
            3: 1,
        }
        offset = offset_map.get(frame_index, 0)
        self.move(self.base_x, self.base_y + offset)

        # ===== 下一帧 =====
        self.seq_index = (self.seq_index + 1) % len(self.sequence)
        self.timer.start(self.intervals[self.seq_index])

    # ===== 拖拽 =====
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            new_pos = event.globalPos() - self.drag_pos
            self.base_x = new_pos.x()
            self.base_y = new_pos.y()
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())
