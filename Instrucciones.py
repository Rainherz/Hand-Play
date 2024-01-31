import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal

# Clase base para las instrucciones con señal de cierre
class InstruccionesBase(QMainWindow):
    cerrar_signal = pyqtSignal()

    def __init__(self, ui_file, parent=None):
        super(InstruccionesBase, self).__init__(parent)
        # Cargar la interfaz de usuario desde el archivo .ui
        ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'GUI', ui_file))
        loadUi(ui_path, self)

        self.okey.clicked.connect(self.Cerrar)

    # Método para cerrar la ventana y emitir la señal de cierre
    def Cerrar(self):
        self.hide()
        self.cerrar_signal.emit()

# Clases específicas para las instrucciones de cada juego
class InstruccionesPacman(InstruccionesBase):
    def __init__(self, parent=None):
        super(InstruccionesPacman, self).__init__('IPacman.ui', parent)

class InstruccionesBomberman(InstruccionesBase):
    def __init__(self, parent=None):
        super(InstruccionesBomberman, self).__init__('IBomberman.ui', parent)

class InstruccionesSnake(InstruccionesBase):
    def __init__(self, parent=None):
        super(InstruccionesSnake, self).__init__('ISnake.ui', parent)

class InstruccionesBike(InstruccionesBase):
    def __init__(self, parent=None):
        super(InstruccionesBike, self).__init__('IBike.ui', parent)

class InstruccionesChess(InstruccionesBase):
    def __init__(self, parent=None):
        super(InstruccionesChess, self).__init__('IChess.ui', parent)

class InstruccionesZuma(InstruccionesBase):
    def __init__(self, parent=None):
        super(InstruccionesZuma, self).__init__('IZuma.ui', parent)
