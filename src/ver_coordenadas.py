import cv2
import fitz
import numpy as np
from pathlib import Path

# ==========================================================
# CARGAR PDF
# ==========================================================

pdf_path = Path(
    r"C:\Users\muril\Documents\GitHub\deteccion-fraude-d14\data\raw\E14Cali_Zona13_01\E14_001.pdf"
)

doc = fitz.open(str(pdf_path))
page = doc[0]

pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)

img = np.frombuffer(
    pix.samples,
    dtype=np.uint8
).reshape(pix.height, pix.width, 3)

doc.close()

img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# ==========================================================
# VARIABLES GLOBALES
# ==========================================================

drawing = False
ix, iy = -1, -1

img_original = img.copy()

# ==========================================================
# MOUSE
# ==========================================================

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        temp = img_original.copy()

        # Mostrar coordenadas del mouse
        texto = f"x={x}, y={y}"

        cv2.putText(
            temp,
            texto,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # Dibujar rectángulo dinámico
        if drawing:
            cv2.rectangle(temp, (ix, iy), (x, y), (0, 255, 0), 2)

        cv2.imshow("Selector E14", temp)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

        print("\n====================================")
        print(f"x1={ix}")
        print(f"y1={iy}")
        print(f"x2={x}")
        print(f"y2={y}")

        h, w = img.shape[:2]

        print("\nRELATIVAS:")
        print(
            f"({ix/w:.3f}, {iy/h:.3f}, {x/w:.3f}, {y/h:.3f})"
        )
        print("====================================")

        cv2.imshow("Selector E14", img)

# ==========================================================
# VENTANA
# ==========================================================

cv2.namedWindow("Selector E14", cv2.WINDOW_NORMAL)

# Tamaño más cómodo
cv2.resizeWindow("Selector E14", 1200, 900)

cv2.setMouseCallback("Selector E14", draw_rectangle)

print("\nINSTRUCCIONES:")
print("- Arrastra con click izquierdo.")
print("- El sistema imprimirá coordenadas.")
print("- ESC para salir.\n")

while True:
    cv2.imshow("Selector E14", img)

    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break

cv2.destroyAllWindows()