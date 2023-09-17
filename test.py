
import sys
from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtWidgets import QApplication
from run import Worker


def my_slot(data):
    print(f"Sinyal Alındı: {data}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Worker nesnesi oluştur
    worker = Worker()
    
    # Sinyali işleve bağla
    worker.log.connect(my_slot)
    
    # Worker sınıfından bir iş parçacığı oluştur ve başlat
    thread = QThread()
    worker.moveToThread(thread)
    thread.started.connect(worker.test)
    thread.start()
    
    sys.exit(app.exec_())