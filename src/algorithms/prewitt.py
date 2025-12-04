import cv2
import numpy as np


class PrewittProcessor:
    def __init__(self):
        # Định nghĩa Kernel Prewitt cố định
        self.kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
        self.ky = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)

    def compute_edges(self, img_input):
        """
        Tính toán biên Prewitt trên ảnh đầu vào.
        """
        # Tính Gradient X và Y
        gx = cv2.filter2D(img_input, cv2.CV_32F, self.kx)
        gy = cv2.filter2D(img_input, cv2.CV_32F, self.ky)

        # Tính độ lớn (Magnitude)
        mag = cv2.magnitude(gx, gy)

        # Chuẩn hóa về 0-255
        edge = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        return edge