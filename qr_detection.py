import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Camera not detected")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    height, width = frame.shape[:2]

    # Camera centre
    frame_cx = width // 2
    frame_cy = height // 2

    cv2.circle(
        frame,
        (frame_cx, frame_cy),
        5,
        (0, 0, 255),
        -1
    )

    for qr in decode(frame):

        text = qr.data.decode("utf-8", errors="replace")

        x, y, w, h = qr.rect

        # QR centre in pixels
        qr_cx = x + w // 2
        qr_cy = y + h // 2

        # Offset from camera centre
        dx = qr_cx - frame_cx
        dy = qr_cy - frame_cy

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.circle(
            frame,
            (qr_cx, qr_cy),
            5,
            (255, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            text[:40],
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        print(
            f"QR: {text} | "
            f"Centre: ({qr_cx}, {qr_cy}) | "
            f"Offset: dx={dx}, dy={dy}"
        )

    cv2.imshow("SkyScan QR Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
