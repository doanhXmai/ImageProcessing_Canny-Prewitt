import cv2
import numpy as np


class ErrorScanner:
    def scan(self, mask, original_img):
        """
        Tìm kiếm lỗi dựa trên so sánh diện tích trung vị.
        """
        # 1. Tìm Contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 2. Lọc rác nhỏ
        valid_cnts = [c for c in contours if cv2.contourArea(c) > 100]

        if not valid_cnts:
            print("Cảnh báo: Không tìm thấy mối hàn nào.")
            return original_img

        # 3. Tính diện tích trung vị (Median)
        areas = [cv2.contourArea(c) for c in valid_cnts]
        median_area = np.median(areas)
        print(f"[INFO] Median Area: {median_area}")

        output = original_img.copy()

        # 4. Duyệt và bắt lỗi
        for cnt in valid_cnts:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)

            # --- LOGIC BẮT LỖI ---
            # Ngưỡng: Lớn hơn 1.6 lần trung bình -> Lỗi
            if area > (median_area * 1.6):
                # Vẽ ĐỎ
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 2)

                ratio = area / median_area
                label = f"ERR:{ratio:.1f}x"
                cv2.putText(output, label, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            else:
                # Vẽ XANH
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return output