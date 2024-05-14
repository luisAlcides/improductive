from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon, QPainter, QPixmap, QPainterPath
from PySide6.QtCore import QSize, Qt, QPropertyAnimation, QPoint, QEasingCurve


class RoundIconButton(QPushButton):
    def __init__(self, icon_path, size, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size, size)
        self.setStyleSheet("border: none;")

        self.anim_in = QPropertyAnimation(self, b"pos")
        self.anim_in.setDuration(200)
        self.anim_in.setEasingCurve(QEasingCurve.InOutQuad)

        self.anim_out = QPropertyAnimation(self, b"pos")
        self.anim_out.setDuration(200)
        self.anim_out.setEasingCurve(QEasingCurve.InOutQuad)

        self.default_pos = self.pos()

    def mousePressEvent(self, event):
        self.anim_in.stop()
        self.anim_in.setStartValue(self.pos())
        self.anim_in.setEndValue(self.default_pos + QPoint(1, 1))
        self.anim_in.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.anim_out.stop()
        self.anim_out.setStartValue(self.pos())
        self.anim_out.setEndValue(self.default_pos)
        self.anim_out.start()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dibujar fondo
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        painter.setClipPath(path)

        painter.setBrush(self.palette().color(self.backgroundRole()))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

        # Dibujar icono
        icon = self.icon().pixmap(self.iconSize())
        icon = icon.scaled(self.size(), Qt.KeepAspectRatio,
                           Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, icon)

        painter.end()  # Asegúrate de que QPainter termine correctamente
