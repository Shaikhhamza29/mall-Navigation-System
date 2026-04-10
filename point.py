import cv2
import math
img = cv2.imread("oberoi/GF.png")

# -----------------------------
# STORE AREAS (Adjusted for YOUR image 1155x640)
# -----------------------------
stores = {
    "Zara": (875, 263),
    "Levis": (611, 317),
    "Sephora": (537, 343),
    "Lifestyle": (476, 416),
    "Uniqlo": (340, 391),
    "Jack & Jones": (244, 373),
    "Vero Moda": (304, 349),
    "M&S": (177, 474),

    "Entrance":( 425 ,131),
    #
    #
    "Poetry Love & Cheesecake": (151, 273),
    "SELECTED HOMME": (112, 172),
    "Only": (156, 151),
    "fossil": (204, 171),
    #
    "Nykaa": (291, 148),
    "Ethos Watch": (359, 156),
    # "Ethos Watch": (339, 122, 379, 191),
    "Sunglasess Hut": (258, 183),
    #
    "CK": (499, 130),
    "Swarovski": (553, 130),
    "Forever New": (603, 111),
    "The Body Shop": (666, 67),
    #
    "Nail Spa": (657, 252),



    ###                PATH         ########
    "P1" : (110,216),
    "P2" : (237,211),
    "P3" : (444,186),
    "P4" : (575,155),
    "P5" : (696,116),
    "P6" : (716,206),
    "P7" : (604,241),
    "P8" : (459,279),
    "P9" : (302,302),
    "P10" : (190,308),


}

graph = {
    "Entrance": ["P3"],

    "P1": ["P2"],
    "P2": ["P1", "P3", "P9"],   # 🔥 ADD THIS
    "P3": ["P2", "P4", "Entrance"],
    "P4": ["P3", "P5"],
    "P5": ["P4", "P6"],
    "P6": ["P5", "P7"],
    "P7": ["P6", "P8"],
    "P8": ["P7", "P9"],
    "P9": ["P8", "P10", "P2"],  # 🔥 ADD THIS
    "P10": ["P9"],
}

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

import heapq

def shortest_path(graph, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == end:
            return path

        for neighbor in graph.get(node, []):
            p1 = stores[node]
            p2 = stores[neighbor]

            dist = distance(p1, p2)

            heapq.heappush(queue, (cost + dist, neighbor, path))

    return []

def nearest_node(store_point):
    min_dist = float("inf")
    nearest = None

    for node in ["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10"]:
        dist = distance(stores[node], store_point)

        if dist < min_dist:
            min_dist = dist
            nearest = node

    return nearest

def draw_path(display, path, store_point):
    for i in range(len(path)-1):
        cv2.line(display, stores[path[i]], stores[path[i+1]], (0, 0, 255), 4)

    # connect last node to store
    if path:
        cv2.line(display, stores[path[-1]], store_point, (0, 0, 255), 4)


def show():
    display = img.copy()

    if selected_store and selected_store not in ["P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","Entrance"]:

        store_point = stores[selected_store]

        start_node = "Entrance"
        end_node = nearest_node(store_point)

        path = shortest_path(graph, start_node, end_node)

        draw_path(display, path, store_point)

        # draw destination
        cv2.circle(display, store_point, 8, (255, 0, 0), -1)

        cv2.putText(display, selected_store, (store_point[0], store_point[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Ground Floor Navigation", display)











selected_store = None

# -----------------------------
# DISPLAY
# -----------------------------
# def show():
#     display = img.copy()
#
#     if selected_store:
#         x1, y1, = stores[selected_store]
#         cv2.circle(display, (x1, y1), 7, (255, 0, 0), -1)
#
#         # cv2.circle(display, (x1, y1), (0, 0, 255), 3)
#         cv2.putText(display, selected_store, (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#
#     cv2.imshow("Ground Floor Navigation", display)

# -----------------------------
# CLICK EVENT
# -----------------------------


def click_event(event, x, y, flags, param):
    global selected_store

    if event == cv2.EVENT_LBUTTONDOWN:
        found = False

        for name, (x1, y1) in stores.items():
            distance = math.sqrt((x - x1)**2 + (y - y1)**2)

            if distance < 20:  # 🔥 adjust this value
                selected_store = name
                print(f"Clicked: {name}")
                print("coordinates:", x, y)
                found = True
                break

        if not found:
            selected_store = None
            print("coordinates:", x, y)
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
