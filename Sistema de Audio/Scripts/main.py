import audfunc as af
import Interfaz as app
import multiprocessing
import getData as gd

def main():
    af.audio_playing.value = False
    # Define el dispositivo de audio al que se enviará la salida
    audio_device_index = 3  # Reemplaza con el índice correcto de tu dispositivo de audio
    while True:
        try:
            dataSensor = gd.getDataTXT(gd.urltxt)
            dataJson = gd.getDataJSON(gd.urljson)
            if dataSensor == "SENSOR 1":
                af.play_audio_thread(af.audSource(dataJson), audio_device_index)
                dataSensor = "-"
        except Exception as e:
            print(f"Error: {e}. Reintentando...")

if __name__ == '__main__':
    # Inicia el servidor en un hilo separado
    app_process = multiprocessing.Process(target=app.run_App)
    app_process.start()
    # Ejecuta la función principal
    main()
