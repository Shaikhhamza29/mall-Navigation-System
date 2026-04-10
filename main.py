import cv2

# -----------------------------
# LOAD IMAGES
# -----------------------------
images = [
    cv2.imread("oberoi/GF.png"),
    cv2.imread("oberoi/F1.png"),
    cv2.imread("oberoi/F2.png"),
    cv2.imread("oberoi/F3.png")
]

names = ["GF", "F1", "F2", "F3"]
full_names = ["Ground Floor", "First Floor", "Second Floor", "Third Floor"]

index = 0

# -----------------------------
# BUTTON SETTINGS
# -----------------------------
btn_width = 100
btn_height = 50
gap = 20

# -----------------------------
# DRAW UI
# -----------------------------
def show():
    img = images[index].copy()
    h, w = img.shape[:2]

    # 🔥 Dynamic positioning
    y_pos = h - 80
    start_x = (w - (len(names) * (btn_width + gap))) // 2

    # Title
    cv2.putText(img, full_names[index], (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Draw buttons
    for i, name in enumerate(names):
        x1 = start_x + i * (btn_width + gap)
        y1 = y_pos
        x2 = x1 + btn_width
        y2 = y1 + btn_height

        color = (0, 200, 0) if i == index else (200, 200, 200)

        # Button fill
        cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        # Border
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

        # Text
        cv2.putText(img, name, (x1 + 30, y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.imshow("Mall Floors", img)

# -----------------------------
# MOUSE CLICK
# -----------------------------
def click_event(event, x, y, flags, param):
    global index

    if event == cv2.EVENT_LBUTTONDOWN:
        img = images[index]
        h, w = img.shape[:2]

        # Same dynamic calculation
        y_pos = h - 80
        start_x = (w - (len(names) * (btn_width + gap))) // 2

        for i, name in enumerate(names):
            x1 = start_x + i * (btn_width + gap)
            y1 = y_pos
            x2 = x1 + btn_width
            y2 = y1 + btn_height

            if x1 <= x <= x2 and y1 <= y <= y2:
                index = i
                show()

# -----------------------------
# WINDOW SETUP
# -----------------------------
cv2.namedWindow("Mall Floors", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Mall Floors", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.setMouseCallback("Mall Floors", click_event)

# -----------------------------
# START
# -----------------------------
show()

while True:
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cv2.destroyAllWindows()
