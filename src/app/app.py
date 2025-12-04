import cv2
from matplotlib import pyplot as plt

from src.algorithms.prewitt import PrewittProcessor
from src.algorithms.scan_errors import ErrorScanner
from src.utils.pre_processor import ImagePreProcessor


def app(image_path):
    # 2. Khởi tạo các module
    pre_proc = ImagePreProcessor()
    prewitt = PrewittProcessor()
    scanner = ErrorScanner()

    # --- BƯỚC 1: TIỀN XỬ LÝ ---
    # Lấy ảnh gốc và Mask đã làm sạch
    original_img, mask_solid = pre_proc.load_and_create_mask(image_path)

    if original_img is None: return

    # --- BƯỚC 2: TÌM BIÊN (PREWITT) ---
    # Chạy trên Mask để biên sạch đẹp
    edge_img = prewitt.compute_edges(mask_solid)

    # --- BƯỚC 3: QUÉT LỖI ---
    # Phân tích Mask và vẽ kết quả lên ảnh gốc
    result_img = scanner.scan(mask_solid, original_img)

    # --- BƯỚC 4: HIỂN THỊ KẾT QUẢ ---
    titles = ['Original', 'Solid Mask (Clean)', 'Prewitt Edges', 'Final Result']
    images = [original_img, mask_solid, edge_img, result_img]

    plt.figure(figsize=(12, 8))
    for i in range(4):
        plt.subplot(2, 2, i + 1)
        plt.title(titles[i])

        # Xử lý màu sắc để hiển thị đúng trên Matplotlib
        if len(images[i].shape) == 2:  # Ảnh xám
            plt.imshow(images[i], cmap='gray')
        else:  # Ảnh màu BGR -> RGB
            plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))

        plt.axis('off')
    plt.tight_layout()
    plt.show()