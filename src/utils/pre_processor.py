import cv2
import numpy as np


class ImagePreProcessor:
    def __init__(self):
        pass

    def load_and_create_mask(self, image_path):
        """
        Đọc ảnh và tạo mặt nạ nhị phân (Solid Mask).
        """
        # 1. Đọc ảnh
        img = cv2.imread(image_path)
        if img is None:
            print(f"Lỗi: Không thể đọc ảnh tại {image_path}")
            return None, None

        # 2. Chuyển sang ảnh xám
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Làm mờ nhẹ (Kernel 3x3 như bạn đã chọn)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # 4. Otsu Threshold
        _, mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 5. Morphology (Khắc phục phân mảnh)
        # Kernel 3x3 hình Ellipse
        kernel_fill = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        # Close mạnh (iter=3) để hàn gắn mảnh vỡ
        mask_solid = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_fill, iterations=3)

        # Dilate nhẹ (iter=1) để gia cố cầu nối
        mask_solid = cv2.dilate(mask_solid, kernel_fill, iterations=1)

        return img, mask_solid