import pyaudio
import wave
import threading
import multiprocessing
import requests


audio_playing = multiprocessing.Value('b', False)
audio_playing.value = False

def send_flag():
    url = "https://myserver1-in01.onrender.com/flag"
    data = '1'
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Flag enviado exitosamente")
    else:
        print(f"Error al enviar flag: {response.status_code}")

def play_audio(file_path, device_index):

    CHUNK = 1024

    wf = wave.open(file_path, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=device_index)

    data = wf.readframes(CHUNK)
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

    audio_playing.value = False  # Establecemos la variable de control en False una vez que la reproducción ha terminado

def play_audio_thread(file_path, device_index):

    if not audio_playing.value:  # Verificamos si el audio se está reproduciendo actualmente
        audio_playing.value = True  # Establecemos la variable de control en True antes de iniciar la reproducción
        print("Reproduciendo audio...")
        send_flag()
        thread = threading.Thread(target=play_audio, args=(file_path, device_index))
        thread.start()
        
def audSource(dataJSON):

    # Definimos las listas donde guardaremos los nombres de los audios y las rutas
    nombres_audios = []
    rutas_audios = []

    # Abrimos el archivo txt
    with open('audios.txt', 'r') as f:
        # Leemos cada línea del archivo
        for linea in f:
            # Dividimos la línea por el carácter de tabulación
            nombre_audio, ruta_audio = linea.strip().split('\t')
            # Añadimos el nombre del audio y la ruta a las listas correspondientes
            nombres_audios.append(nombre_audio)
            rutas_audios.append(ruta_audio)

    # Buscamos el audio en la lista de nombres de audios
    for i in range(len(nombres_audios)):
        if dataJSON + '.wav' == nombres_audios[i]:
            return rutas_audios[i]
    

    


