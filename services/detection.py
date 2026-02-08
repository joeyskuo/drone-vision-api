from ultralytics import YOLO
from PIL import Image
import io
import cv2

class DetectionService:
    def __init__(self):
        self.model = YOLO("models/yolov8s_best.pt")
    
    def detect_and_annotate(self, image_bytes: bytes, conf_threshold: float = 0.25):
        """
        Run detection and return annotated image with bounding boxes.
        """
        # Load image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run inference
        results = self.model(image, conf=conf_threshold)
        
        # Get annotated image (YOLO draws boxes automatically)
        annotated_image = results[0].plot()  # Returns numpy array with boxes drawn
        
        # Convert BGR to RGB (OpenCV uses BGR, PIL uses RGB)
        annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(annotated_image_rgb)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()