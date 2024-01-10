import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
cap1 = cv2.VideoCapture('rtsp://playtime.cctvddns.net:1029/profile1')
cap2 = cv2.VideoCapture('rtsp://playtime.cctvddns.net:554/profile1')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('{}.avi'.format(video_path.split('/')[-1].split('.')[0]),fourcc, 20.0, (1280,360))
out = cv2.VideoWriter("frame2record.mp4", cv2.VideoWriter_fourcc('a', 'v', 'c', '1'), 20.0, (1280,360))
#cap = cv2.VideoCapture("vlc-record-2023-11-30-17h17m43s-rtsp___playtime.cctvddns.net_554_profile1-.avi")

model = YOLO('yolov8n.pt')
minimap_size = (180, 200, 3)
while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()


    print(frame1.shape)
    print(frame2.shape)


    width = frame1.shape[1]
    height = frame1.shape[0]

    # Recorta o quadro horizontalmente
    half_width = 1470
    half_height = 950

    half_width2 = 1770
    half_height2 = 1150


    frame1 = frame1[:half_height, :half_width]
    frame2 = frame2[:half_height2, :half_width2]
    frame1 = cv2.resize(frame1, (640, 360))
    frame2 = cv2.resize(frame2, (640, 360))
    concatenated_frame = cv2.hconcat([frame1, frame2])

    frame = cv2.resize(concatenated_frame, (1280, 360))

    #frame1 = cv2.resize(frame1, (640, 360))
    # Exibe o quadro recortado


    # Clear the minimap by creating a new black image
    minimap = np.zeros(minimap_size, dtype=np.uint8)

    # Redimensiona o frame2 para as dimensões do frame1


    # Concatena os quadros horizontalmente






    cv2.imshow('raw', frame)


    out.write(frame)

    k = cv2.waitKey(10)& 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
