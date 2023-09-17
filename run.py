import sys
from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtWidgets import QApplication

class Worker(QObject):
    log = Signal(int)

    def test(self):
        for i in range(10000):
            self.log.emit(i)

