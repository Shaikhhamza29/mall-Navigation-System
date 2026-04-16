import cv2

img = cv2.imread("oberoi/F3.png")

# -----------------------------
# STORE AREAS (Adjusted for YOUR image 1155x640)
# -----------------------------
stores = {
    "Zara": (712, 98, 1005, 374),
    "Levis": (576, 265, 651, 421),
    "Sephora": (513, 282, 581, 408),
    "Lifestyle": (415, 299, 528, 483),
    "Uniqlo": (317, 315, 427, 524),
    "Jack & Jones": (200, 320, 276, 478),
    "Vero Moda": (261, 317, 326, 411),
    "M&S": (106, 323, 208, 603),



    "Poetry Love & Cheesecake": (114, 224, 180, 296),
    "SELECTED HOMME": (96, 124, 128, 204),
    "Only": (124, 126, 183, 200),
    "fossil": (183, 126, 224, 196),

    "Nykaa": (271, 124, 309, 192),
    "Entrance": (381,116 , 475, 133),
    "Ethos Watch": (339, 122, 379, 191),
    "Sunglasess Hut": (244, 156, 274, 194),

    "CK": (477, 100, 510, 156),
    "Swarovski": (509, 88, 548, 144),
    "Forever New": (585, 101, 615, 129),
    "The Body Shop": (640, 46, 680, 104),

    "Nail Spa": (656, 241, 688, 327),
}

selected_store = None

# -----------------------------
# DISPLAY
# -----------------------------
def show():
    display = img.copy()

    if selected_store:
        x1, y1, x2, y2 = stores[selected_store]

        cv2.rectangle(display, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.putText(display, selected_store, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Ground Floor Navigation", display)

# -----------------------------
# CLICK EVENT
# -----------------------------
def click_event(event, x, y, flags, param):
    global selected_store

    if event == cv2.EVENT_LBUTTONDOWN:
        found = False

        for name, (x1, y1, x2, y2) in stores.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                selected_store = name
                print(f"Clicked: {name}")
                print("cordinates", x, y)
                found = True
                break

        if not found:
            selected_store = None
            print("cordinates", x, y)
            print("No store detected")

        show()

# -----------------------------
# WINDOW
# -----------------------------
cv2.namedWindow("Ground Floor Navigation", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Ground Floor Navigation", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.setMouseCallback("Ground Floor Navigation", click_event)

show()
cv2.waitKey(0)
cv2.destroyAllWindows()
