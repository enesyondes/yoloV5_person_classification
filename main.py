import torch
#from PIL import Image
import cv2
#import numpy as np
#from ultralytics import YOLO

# YOLOv5 modelini yükleme
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # Önceden eğitilmiş küçük model kullanılıyor

# Tespit yapmak istediğiniz görüntünün yolunu belirtin
cameraID = 0

video = cv2.VideoCapture(cameraID)
if cameraID != 0 or cameraID != 1:
    cameraID = "canli kayit"
    cameraName = video.get(cv2.CAP_PROP_BACKEND)
    cameraWidth = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    cameraHeight = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cameraFPS = video.get(cv2.CAP_PROP_FPS)
        
    if not video.isOpened():
        print("Kamera Açilamadi. Lütfen Kamera ID'sini Doğru Girdiğinizden Emin Olun!")
    else:
        print(f"Kamera Bilgileri:\nKamera ID: {cameraID}\nKamera İsmi: {cameraName}\nKamera Çözünürlüğü: ({cameraWidth}, {cameraHeight})\nFPS: {int(cameraFPS)}")
        

frame_count = 0
while True:
    retval, img = video.read()
    frame_count += 1
    if retval is False:
        break
    img = cv2.resize(src=img, dsize=(848, 480))
    
    # Nesne tespiti yapma
    results = model(img)

    # Sınıf etiketlerini ve skorlarını alın
    classifications = results.pred[0][:, 5].cpu().numpy()
    scores = results.pred[0][:, 4].cpu().numpy()

    # "insan" sınıfının tahmin edilip edilmediğini kontrol etme
    threshold = 0  # Bu eşik değerini ayarlayabilirsiniz
    is_person_detected = any((classifications == 0) & (scores > threshold))

    if is_person_detected:
        print("Görüntüde insan tespit edildi.")
        cv2.putText(img,"Goruntude insan tespit edildi",(30,30),cv2.FONT_HERSHEY_PLAIN,1.5,(0,255,255),2)
    else:
        print("Görüntüde insan tespit edilmedi.")

    cv2.imshow(winname="img", mat=img)
    cv2.waitKey(int(1000/cameraFPS))

video.release()
cv2.destroyAllWindows()