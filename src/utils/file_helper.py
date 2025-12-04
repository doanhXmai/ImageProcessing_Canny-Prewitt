import math

import cv2
import os
import matplotlib.pyplot as plt

from src.utils.log import ConsoleLogger as cl


class FileHelper:
    def __init__(self):
        pass

    @staticmethod
    def read_file(file_path: str, gray_scale = False):
        if not os.path.exists(file_path):
            cl.error(f"File không tồn tại: {file_path}")
            return None

        flag = cv2.IMREAD_GRAYSCALE if gray_scale else cv2.IMREAD_COLOR

        img = cv2.imread(file_path, flag)

        if img is None:
            cl.error(f"Không thể đọc định dạng ảnh này: {file_path}")
            return None

        cl.info(f"Đã đọc ảnh: {file_path} | Kích thước: {img.shape}")
        return img

    @staticmethod
    def save_file(file_path : str, image, params = None):
        if image is None:
            cl.error("Ảnh đầu vào rỗng (None), không thể lưu.")
            return False

        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
                cl.info(f"Đã tạo thư mục mới: {directory}")
            except OSError as e:
                cl.error(f"Không thể tạo thư mục: {e}")
                return False
        success = cv2.imwrite(file_path, image, params)

        if success:
            cl.info(f"Đã lưu ảnh thành công: {file_path}")
        else:
            cl.error(f"Lưu ảnh thất bại: {file_path}")

        return success

    @staticmethod
    def show_image(image, title = "Show Image", wait_key = 0):
        if image is None:
            cl.error("Ảnh rỗng, không thể hiển thị.")
            return
        cv2.imshow(title, image)
        cl.info(f"Đang hiển thị cửa sổ '{title}'. Nhấn phím bất kì để tiếp tục.")

        # cv2.waitKey(wait_key)
        #
        # cv2.destroyWindow(title)

    @staticmethod
    def show_histogram(image, title = "Histogram"):
        if image is None:
            cl.error("Không có ảnh")
            return

        plt.figure(figsize=(10, 5))
        plt.title(title)
        plt.xlabel("Giá trị Pixel (0-255)")
        plt.ylabel("Số lượng Pixel")

        if len (image.shape) == 2:
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            plt.plot(hist, color="black", label="Grayscale")
            plt.fill_between(range(256), hist.ravel(), color="gray", alpha=0.3)
            plt.legend()

        else:
            colors = ('b', 'g', 'r')
            labels = ("Blue", "Green", "Red")

            for i, col in enumerate(colors):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                plt.plot(hist, color=col, label = labels[i])
                plt.xlim([0, 256])

            plt.legend()

        plt.grid(axis='y', alpha=0.5)
        cl.info(f"Đang hiện thị biểu đồ histogram của {title}")
        plt.show()

    @staticmethod
    def show_grid(images_dict, title="Process Pipline", cols = 3):
        if not images_dict:
            print("[WARN] Không có ảnh nào để hiển thị.")
            return

        n_images = len(images_dict)
        rows = math.ceil(n_images / cols)

        plt.figure(figsize=(5 * cols, 4 * rows))  # Tự động tính kích thước cửa sổ
        plt.suptitle(title, fontsize=16)

        for i, (label, img) in enumerate(images_dict.items()):
            if img is None:
                continue

            plt.subplot(rows, cols, i + 1)
            plt.title(label)
            plt.axis('off')  # Tắt trục tọa độ cho đẹp

            # Xử lý màu sắc để hiển thị đúng trên Matplotlib
            if len(img.shape) == 2:
                # Ảnh xám -> Dùng colormap 'gray'
                plt.imshow(img, cmap='gray')
            else:
                # Ảnh màu (OpenCV là BGR, Matplotlib là RGB) -> Phải đảo màu
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                plt.imshow(img_rgb)

        plt.tight_layout()
        plt.show()