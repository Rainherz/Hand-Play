from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
import os 

# Clase para la ventana principal
class VentanaPrincipal(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaPrincipal, self).__init__(parent)
        # Configuración de la interfaz de usuario
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, 'GUI', 'Home.ui')
        loadUi(ui_file, self)

        # Conexión de los botones a los métodos correspondientes
        self.sectores.clicked.connect(self.OpenSectores)
        self.gestos.clicked.connect(self.OpenGestos)
        self.mouse.clicked.connect(self.OpenMouse)

    # Método para abrir la ventana de sectores
    def OpenSectores(self):
        from VentanaSectores import VentanaSectores
        self.hide()
        ventana1 = VentanaSectores(self)
        ventana1.show()

    # Método para abrir la ventana de gestos
    def OpenGestos(self):
        from VentanaGestos import VentanaGestos
        self.hide()
        ventana2 = VentanaGestos(self)
        ventana2.show()

    # Método para abrir la ventana de control de mouse
    def OpenMouse(self):
        from VentanaMouse import VentanaMouse
        self.hide()
        ventana3 = VentanaMouse(self)
        ventana3.show()
