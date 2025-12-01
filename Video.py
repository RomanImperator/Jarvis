import cv2 as cv
from PIL import Image

class Camera:
    """
    Handles webcam operations using OpenCV.
    """
    def __init__(self):
        # Initialize the default camera (index 0)
        self.cam = cv.VideoCapture(0)
        if not self.cam.isOpened():
            print("[ERROR] Could not open camera.")
    
    def capture_frame(self) -> Image.Image | None:
        """
        Captures a single frame from the camera.
        
        Returns:
            Image.Image | None: The captured frame as a PIL Image, or None if failed.
        """
        if not self.cam.isOpened():
            return None

        ret, frame = self.cam.read() # Read the frame
        if not ret:
            return None
        
        # Convert from BGR (OpenCV default) to RGB (PIL compatible)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return Image.fromarray(frame_rgb)

    def release(self):
        """
        Releases the camera resource and closes windows.
        """
        self.cam.release()
        cv.destroyAllWindows()

# DEBUG:
# if __name__ == "__main__":
#    cam = Camera()
#    img = cam.capture_frame()
#    if img:
#        img.show()
#    cam.release()