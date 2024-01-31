import psutil

def cerrar_programas(nombres_procesos):
    for proceso in psutil.process_iter(['pid', 'name']):
        for nombre_proceso in nombres_procesos:
            if nombre_proceso.lower() in proceso.info['name'].lower():
                pid = proceso.info['pid']
                psutil.Process(pid).terminate()
                print(f'{nombre_proceso} cerrado exitosamente.')
                return

    print('Ningún proceso de la lista encontrado en ejecución.')