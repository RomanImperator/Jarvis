import cv2 as cv
from PIL import Image

class Camera:
    def __init__(self):
        self.cam = cv.VideoCapture(0)
        if not self.cam.isOpened():
            print("Errore: Impossibile aprire la fotocamera.")
    
    def capture_frame(self) -> Image.Image | None:
        if not self.cam.isOpened():
            return None

        ret, frame = self.cam.read() #legge il frame
        if not ret:
            return None
        
        # Converti da BGR (OpenCV) a RGB (PIL)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return Image.fromarray(frame_rgb)

    def release(self):
        self.cam.release()
        cv.destroyAllWindows()

#DEBUG:
#if __name__ == "__main__":
#    cam = Camera()
#    img = cam.capture_frame()
#    if img:
#        img.show()
#    cam.release()