from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve


class AnimatedComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._popup_animation = None

    def showPopup(self):
        super().showPopup()
        popup = self.view().window()
        if popup is None:
            return
        popup.setWindowOpacity(0.0)
        animation = QPropertyAnimation(popup, b"windowOpacity", self)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setDuration(140)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        self._popup_animation = animation
        animation.start()
