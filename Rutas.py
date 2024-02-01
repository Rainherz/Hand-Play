# Rutas.py
import os
import sys

script_directory = os.path.dirname(os.path.abspath(__file__))

games_dictionary = {
    'pacman': os.path.join(script_directory, 'Juegos', 'Pac-Man.exe'),
    'zuma': os.path.join(script_directory, 'Juegos', 'Zuma Deluxe', 'Zuma.exe'),
    'bomberman': [os.path.join(script_directory, 'Juegos', 'snes9x', 'snes9x-x64.exe') ,
                  os.path.join(script_directory, 'Juegos', 'snes9x', 'Roms','Bomberman4.smc')],
    'bike': os.path.join(script_directory, 'Juegos', 'Extreme Bike Trials', 'game.exe'),
    'chess': os.path.join(script_directory, 'Juegos', 'Chess Pro 3D', 'game.exe'),
    'snake': os.path.join(script_directory, 'Juegos', 'Snake-main','dist', 'snake.exe'),
}

