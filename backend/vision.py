import cv2
import numpy as np


def decode_image(raw_bytes: bytes) -> np.ndarray:
    array = np.frombuffer(raw_bytes, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Não foi possível decodificar a imagem enviada.")
    return image


def crop_roi(image: np.ndarray, roi_x: float, roi_y: float, roi_w: float, roi_h: float) -> np.ndarray:
    height, width = image.shape[:2]
    x0 = int(max(0, min(roi_x, 1)) * width)
    y0 = int(max(0, min(roi_y, 1)) * height)
    x1 = int(max(0, min(roi_x + roi_w, 1)) * width)
    y1 = int(max(0, min(roi_y + roi_h, 1)) * height)
    x1 = max(x1, x0 + 1)
    y1 = max(y1, y0 + 1)
    return image[y0:y1, x0:x1]


def mean_rgb(crop: np.ndarray) -> tuple[float, float, float]:
    b, g, r = cv2.mean(crop)[:3]
    return r, g, b


def absorbance_from_channel(channel_8bit: float) -> float:
    normalized = max(channel_8bit, 1.0) / 255.0
    return -np.log10(normalized)


def analyze(raw_bytes: bytes, roi_x: float, roi_y: float, roi_w: float, roi_h: float) -> dict:
    image = decode_image(raw_bytes)
    crop = crop_roi(image, roi_x, roi_y, roi_w, roi_h)
    r, g, b = mean_rgb(crop)
    channel_value = absorbance_from_channel(g)
    return {"r": r, "g": g, "b": b, "channel_value": channel_value}
