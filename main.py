import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPixmap


# ===== 解决 PyInstaller / exe 资源路径问题 =====
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller 解包目录
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

        # ===== 加载 stand 动画帧 =====
        self.stand_frames = [
            QPixmap(resource_path("assets/stand/1.png")),
            QPixmap(resource_path("assets/stand/2.png")),
            QPixmap(resource_path("assets/stand/3.png")),
            QPixmap(resource_path("assets/stand/4.png")),
        ]
        self.current_frame = 0

        # ===== 显示第一帧（防止透明消失） =====
        pix = self.stand_frames[0]
        if pix.isNull():
            print("ERROR: stand image load failed")
            self.resize(200, 200)  # 防止窗口 0x0
        else:
            self.setPixmap(pix)
            self.resize(pix.size())

        # ===== 强制窗口出现在屏幕中央 =====
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        # ===== 拖拽用 =====
        self.drag_pos = QPoint()

        # ===== stand 动画定时器 =====
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_stand_animation)
        self.timer.start(700)  # 700ms / 帧（慢节奏）

    # ===== 播放 stand 动画 =====
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
