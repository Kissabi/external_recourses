import cv2
import threading

def capturar_video(camera, resultado, half_width, half_height):
    while True:
        ret, frame = camera.read()

        # Verifica se o frame foi capturado corretamente
        if not ret:
            break

        frame = frame[:half_height, :half_width]

        resultado[camera] = cv2.resize(frame, (640, 360))

    camera.release()

# Inicializa as câmeras
cap1 = cv2.VideoCapture('rtsp://192.168.100.198:1029/profile1')
cap2 = cv2.VideoCapture('rtsp://192.168.100.199:554/profile1')

# Configurações do vídeo de saída
out = cv2.VideoWriter("frame2record.mp4", cv2.VideoWriter_fourcc('a', 'v', 'c', '1'), 20.0, (1280, 360))

# Define as dimensões desejadas para recorte
half_width = 1470
half_height = 950

# Inicializa as matrizes para armazenar os resultados das câmeras
resultado_camaras = {cap1: None, cap2: None}

# Cria threads para cada câmera
thread_camera1 = threading.Thread(target=capturar_video, args=(cap1, resultado_camaras, half_width, half_height))
thread_camera2 = threading.Thread(target=capturar_video, args=(cap2, resultado_camaras, half_width, half_height))

# Inicia as threads
thread_camera1.start()
thread_camera2.start()

while True:
    # Aguarda até que ambas as threads terminem para garantir que todos os frames foram capturados
    thread_camera1.join(1)
    thread_camera2.join(1)

    # Verifica se ambas as threads terminaram
    if not (thread_camera1.is_alive() or thread_camera2.is_alive()):
        break

    # Obtém os resultados das câmeras
    frame1 = resultado_camaras[cap1]
    frame2 = resultado_camaras[cap2]

    # Concatena horizontalmente os resultados das câmeras
    if frame1 is not None and frame2 is not None:
        resultado_concatenado = cv2.hconcat([frame1, frame2])

        # Exibe a imagem concatenada
        cv2.imshow("Concatenado", resultado_concatenado)

        # Grava o frame resultante no vídeo de saída
        out.write(resultado_concatenado)

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# Libera os recursos
cap1.release()
cap2.release()
out.release()
cv2.destroyAllWindows()
