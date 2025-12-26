import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPixmap


class DesktopPet(QLabel):
    def __init__(self):
        super().__init__()

        # ===== 窗口属性 =====
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ===== stand 动画资源 =====
        self.stand_frames = [
            QPixmap("assets/stand/1.png"),
            QPixmap("assets/stand/2.png"),
            QPixmap("assets/stand/3.png"),
            QPixmap("assets/stand/4.png"),
        ]
        self.current_frame = 0

        # 显示第一帧
        self.setPixmap(self.stand_frames[0])
        self.resize(self.stand_frames[0].size())

        # ===== 拖拽用 =====
        self.drag_pos = QPoint()

        # ===== 动画定时器 =====
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_stand_animation)
        self.timer.start(700)  # 700ms / 帧（慢节奏）

    # ===== stand 动画播放 =====
    def play_stand_animation(self):
        self.current_frame = (self.current_frame + 1) % len(self.stand_frames)
        self.setPixmap(self.stand_frames[self.current_frame])

    # ===== 鼠标拖拽 =====
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        pass  # 以后加互动


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())
