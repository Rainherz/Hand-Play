# main.py
import sys
from PyQt5.QtWidgets import QApplication
from Home import VentanaPrincipal

# Función para iniciar la ventana principal de la aplicación
def iniciarVentana():
    app = QApplication(sys.argv)
    ventana1 = VentanaPrincipal()
    ventana1.show()
    sys.exit(app.exec_())

# Verificación de ejecución directa del script y llamada a la función principal
if __name__ == "__main__":
    iniciarVentana()