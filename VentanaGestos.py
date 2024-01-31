# VentanaGestos.py
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from Rutas import games_dictionary
from Instrucciones import *
from subprocess import Popen
import sys
import os

# Directorio del script actual
script_directory = os.path.dirname(os.path.abspath(__file__))

# Definición de la clase VentanaSectores que hereda de QMainWindow
class VentanaGestos(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaGestos, self).__init__(parent)

        # Carga la interfaz de usuario desde el archivo Gestos.ui
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, 'GUI', 'Gestos.ui')
        loadUi(ui_file, self)
        # Connect signals to slots
        self.home.clicked.connect(self.OpenHome)

        # Lista de juegos seleccionados
        selected_games = ['pacman', 'snake']
        for game_name in selected_games:
            path = games_dictionary[game_name]
            self.connect_game_button(getattr(self, game_name.lower()), game_name, path)

    def connect_game_button(self, button, game_name, path):
        button.clicked.connect(lambda: self.open_game(game_name, path))

    # Función para abrir la ventana principal al hacer clic en "home"
    def OpenHome(self):
        from Home import VentanaPrincipal
        self.close()
        ventana1 = VentanaPrincipal(self)
        ventana1.show()

    # Función para abrir la ventana de instrucciones del juego seleccionado
    def open_game(self, game_name, path):
        self.close()

        print(f"Opening game: {game_name}")

        instrucciones_class = globals().get(f"Instrucciones{game_name.capitalize()}")
        if instrucciones_class:
            ventana = instrucciones_class(self)
            ventana.cerrar_signal.connect(lambda: self.launch_game(path))
            ventana.show()
        else:
            print(f"Unsupported game: {game_name}")
            return

    # Función para lanzar el juego seleccionado
    def launch_game(self, path):
        print("Launching the game...")
        self.process = Popen(path)
        self.process = Popen([sys.executable, os.path.join(script_directory, 'gestosOpt.py')])
        