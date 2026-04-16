import cv2
import math
import heapq
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
# -----------------------------
# GLOBAL STATE
# -----------------------------
last_paths = {"GF": None, "F1": None, "F2": None,"F3":None}
last_source = None,
last_dest = None

img_GF = cv2.imread("oberoi/GF.png")
img_F1 = cv2.imread("oberoi/F1.png")
img_F2 = cv2.imread("oberoi/F2.png")
img_F3 = cv2.imread("oberoi/F3.png")

current_floor = "GF"
# -----------------------------
# STORES (same as yours)
# -----------------------------
stores_GF = {
    "Zara": (1493, 425),
    "Levis": (1043, 522),
    "Sephora": (916, 566),
    "Lifestyle": (814, 690),
    "Uniqlo": (580, 650),
    "Jack & Jones": (416, 616),
    "Vero Moda": (520, 576),
    "M&S": (303, 787),
    "Entrance": (724, 198),
    "poetry Love & Cheesecake": (257, 442),
    "SELECTED HOMME": (191, 272),
    "Only": (267, 238),
    "fossil": (347, 271),
    "Nykaa": (494, 230),
    "Ethos Watch": (615, 248),
    "Sunglasess Hut": (441, 293),
    "CK": (849, 199),
    "Swarovski": (941, 200),
    "Forever New": (1083, 171),
    "The Body Shop": (1134, 91),
    "Nail Spa": (1125, 413),

    "Esc1": (317, 440),
    "Esc2": (1141, 277),

    # PATH
    "P1": (198,342),
    "P2": (411,333),
    "P3": (762,297),
    "P4": (1016,229),
    "P5": (1192,168),
    "P6": (1226,330),
    "P7": (1023,393),
    "P8": (764,461),
    "P9": (487,497),
    "P10": (212,515),
}

stores_F1 = {
    "Metro Shoes": (144, 268),
    "Regal Shoes": (303, 250),
    "Asics": (508, 234),
    "The Souled Store": (572, 273),
    "Adidas": (865, 207),
    "Komponreo": (985, 167),
    "Van Hausen": (1160, 113),
    "The Bombay Shirt Company": (1518, 110),
    "ColorPlus": (1697, 258),
    "Jockey": (1691, 385),
    "GAP": (1545, 569),
    "BagLine": (1461, 481),
    "Fizzy goblet": (1458, 420),
    "Mokobara": (1437, 319),
    "puma": (1352, 412),
    "AllenSolly": (1139, 496),
    "US Polo Assn": (979, 522),
    "Louis Philippe": (809, 540),
    "LifeStyle ": (720, 747),
    "Nautica":(586 ,551),
    "Hide Design":(489 ,576),
    "Tanishq":(397 ,715),
    "Croma":(209 ,717),
    "theobroma":(187 ,442),

    "Esc1": (317, 440),
    "Esc2": (1141, 277),

    # PATH
    "P1": (198,342),
    "P2": (411,333),
    "P3": (762,297),
    "P4": (1016,229),
    "P5": (1192,168),
    "P6": ( 1338 ,213),
    "P7":( 1608 ,188),
    "P8":( 1643 ,437),
    "P9":(1518 ,445),
    "P10":( 1483 ,279),
    "P11":( 1360 ,292),
    "P12": (1226,330),
    "P13": (1023,393),
    "P14": (764,461),
    "P15": (487,497),
    "P16": (212,515),
}

stores_F2={
    "Fab":( 228 ,221),
    "samsonite":( 311 ,274),
    "BIBA":(489 ,257),
    "Cotton World":(600 ,201),
    "StarBucks":( 758 ,248),
    "Global Desi":(867 ,221),
    "House of Felt":( 968 ,125),
    "AND":( 1097 ,135),
    "Kitchen Garden":(1363 ,158),
    "Peora":( 1495 ,149),
    "Tasva":( 1563 ,128),
    "Jaypore":(1704 ,168),
    "Meena Bazaar":( 1703 ,282),
    "Raymond":(1715 ,360),
    "Good Flippin Burgers":(1600 ,543),
    "Copper Chimney":(1529 ,618),
    "Burma Burma":( 1447 ,508),
    "Coco caffe":(1345 ,433),
    "Envi Salon":(1231 ,553),
    "Enamor":( 1066 ,461),
    "Mother Care":(1011 ,536),
    "Chique":( 790 ,498),
    "Lifestyle":( 707 ,718),
    "Nalli":(400 ,756),
    "nature Basket":(264 ,723),
    "Chaayos":( 259 ,419),
# PATH (COPY FROM F1 OR ADJUST)
    "P1": (198,342),
    "P2": (411,333),
    "P3": (762,297),
    "P4": (1016,229),
    "P5": (1192,168),
    "P6": (1338,213),
    "P7": (1608,188),
    "P8": (1643,437),
    "P9": (1518,445),
    "P10": (1483,279),
    "P11": (1360,292),
    "P12": (1226,330),
    "P13": (1023,393),
    "P14": (764,461),
    "P15": (487,497),
    "P16": (212,515),

    "Esc1": (317, 440),
    "Esc2": (1141, 277),
}  #keep same

stores_F3={
    "play N learn ":(242 ,394),
    "Olive Bistor":( 971 ,140),
    "Third Wave Coffee ":( 1342 ,299),
    "pvr Inox":( 1537 ,471),
    "Soical":( 1220 ,513),
    "farzi Coffee":( 1100 ,614),
    "pizza Express":( 977, 675),
    "Asia Kitchen":( 860 ,603),
    "Maharaja bhoj":( 773 ,728),
    "Burger King":( 651 ,650),
    "HAS juice":(656 ,729),
    "Dominos":( 649 ,789),
    "MOD":( 596 ,897),
    "kailash parbat":( 482 ,940),
    "KFC":( 373 ,965),
    "MCD":( 257 ,964),
    "Subway":( 261 ,890),
    "Sbarro":( 253 ,831),
    "Sandwizza":(238 ,752),
    "Nom Nom Express":( 232 ,683),
    "WOW momos":( 228 ,606),

    "P1":( 355 ,359),
    "P2":( 541 ,335),
    "P3":( 769 ,295),
    "P4":( 993 ,245),
    "P5":( 1230 ,169 ),
    "P6":( 1276 ,335),
    "P7":(  1207 ,442),
    "P8":( 1048 ,472),
    "P9":( 842 ,514),
    "P10":(  676 ,544),
    "P11":(  517 ,566),
    "P12":(  572 ,729),
    "P13":(  535 ,852),
    "P14":(  427 ,883),
    "P15":(  328 ,820),
    "P16":( 310 ,641),

    "Esc1": (337, 440),
    "Esc2": (1141, 277),

}

# -----------------------------
# GRAPHS (same GF + F1)
# -----------------------------
graph_GF = {
    "Entrance": ["P3"],
    "P1": ["P2", "Esc1"],
    "P2": ["P1", "P3", "P9","Esc1"],
    "P3": ["P2", "P4", "Entrance"],
    "P4": ["P3", "P5","Esc2"],
    "P5": ["P4", "P6", "Esc2"],
    "P6": ["P5", "P7","Esc2"],
    "P7": ["P6", "P8"],
    "P8": ["P7", "P9"],
    "P9": ["P8", "P10", "P2","Esc1"],
    "P10": ["P9","Esc1"],
    "Esc1": ["P1","P2","P9"],
    "Esc2": ["P5","P4","P6"],
}

graph_F1 = {
    "P1": ["P2", "P16", "P15"],
    "P2": ["P1", "P3", "P15","Esc1"],
    "P3": ["P2", "P4","Esc1"],
    "P4": ["P3", "P5"],
    "P5": ["P4", "P6","Esc2"],
    "P6": ["P5", "P7","Esc2"],
    "P7": ["P6", "P8"],
    "P8": ["P7", "P9"],
    "P9": ["P8", "P10"],
    "P10": ["P9", "P11"],
    "P11": ["P10", "P12"],
    "P12": ["P11", "P13"],
    "P13": ["P12", "P14","Esc1"],
    "P14": ["P13", "P15","Esc1"],
    "P15": ["P14", "P16", "P2", "P1","Esc1"],
    "P16": ["P15", "P1"],
    "Esc1": ["P1","P2","P3","P13","P14","P15"],
    "Esc2": ["P5","P6"],
}

graph_F2 = {
    "P1": ["P2", "P16", "P15"],
    "P2": ["P1", "P3", "P15", "Esc1"],
    "P3": ["P2", "P4", "Esc1"],
    "P4": ["P3", "P5"],
    "P5": ["P4", "P6", "Esc2"],
    "P6": ["P5", "P7", "Esc2"],
    "P7": ["P6", "P8"],
    "P8": ["P7", "P9"],
    "P9": ["P8", "P10"],
    "P10": ["P9", "P11"],
    "P11": ["P10", "P12"],
    "P12": ["P11", "P13"],
    "P13": ["P12", "P14", "Esc1"],
    "P14": ["P13", "P15", "Esc1"],
    "P15": ["P14", "P16", "P2", "P1", "Esc1"],
    "P16": ["P15", "P1"],
    "Esc1": ["P1", "P2", "P3", "P13", "P14", "P15"],
    "Esc2": ["P5", "P6"],
}

graph_F3 = {
    "P1": ["P2", "P16", "P15", "Esc1"],
    "P2": ["P1", "P3", "P15", "Esc1"],
    "P3": ["P2", "P4", "P6"],
    "P4": ["P3", "P5"],
    "P5": ["P4", "P6", "Esc2"],
    "P6": ["P5", "P7", "P3", "Esc2"],
    "P7": ["P6", "P8","Esc2"],
    "P8": ["P7", "P9","Esc1"],
    "P9": ["P8", "P10","Esc1"],
    "P10": ["P9", "P11"],
    "P11": ["P10", "P12"],
    "P12": ["P11", "P13"],
    "P13": ["P12", "P14"],
    "P14": ["P13", "P15"],
    "P15": ["P14", "P16", "P1", "P2"],
    "P16": ["P15", "P1","Esc1"],

    "Esc1": ["P1", "P2","P8","P9","P16"],
    "Esc2": ["P5", "P6","P7"],
}

# FLOOR SYSTEM

floors = {
    "GF": {"img": img_GF, "stores": stores_GF, "graph": graph_GF},
    "F1": {"img": img_F1, "stores": stores_F1, "graph": graph_F1},
    "F2": {"img": img_F2, "stores": stores_F2, "graph": graph_F2},
    "F3": {"img": img_F3, "stores": stores_F3, "graph": graph_F3},
}

floor_keys = list(floors.keys())

# ESCALATOR LINKS (MULTI FLOOR)

vertical_links = {
    ("GF", "Esc1"): ("F1", "Esc1"),
    ("F1", "Esc1"): ("F2", "Esc1"),
    ("F2", "Esc1"): ("F3", "Esc1"),


    ("GF", "Esc2"): ("F1", "Esc2"),
    ("F1", "Esc2"): ("F2", "Esc2"),
    ("F2", "Esc2"): ("F3", "Esc2"),

}

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def astar(graph, start, end, store):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {node: float("inf") for node in store}
    g_score[start] = 0

    f_score = {node: float("inf") for node in store}
    f_score[start] = distance(store[start], store[end])

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in graph.get(current, []):
            tentative_g = g_score[current] + distance(store[current], store[neighbor])

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + distance(store[neighbor], store[end])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def nearest_node(point, store):
    return min([n for n in store if n.startswith("P")],
               key=lambda n: distance(store[n], point))

def get_floor(name):
    for f, data in floors.items():
        if name in data["stores"]:
            return f

def filter_store(s):
    return [k for k in s if not k.startswith("P") and not k.startswith("Esc")]

# STORE LIST (FIXED ORDER)
store_list = filter_store(stores_GF) + filter_store(stores_F1) + filter_store(stores_F2) + filter_store(stores_F3)
full_store_list = store_list.copy()

# TKINTER

root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

def convert(img):
    global scale_x, scale_y

    h, w = img.shape[:2]
    scale_x = screen_w / w
    scale_y = (screen_h - 120) / h

    resized = cv2.resize(img, (screen_w, screen_h - 120))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    return ImageTk.PhotoImage(Image.fromarray(rgb))

def filter_combobox(event, var, combo):
    typed = var.get().lower()

    if typed == "":
        combo['values'] = full_store_list
    else:
        combo['values'] = [i for i in full_store_list if typed in i.lower()]

    combo.event_generate('<Down>')

def on_click(event):
    Radius = 50
    x = int(event.x / scale_x)
    y = int(event.y / scale_y)

    store_data = floors[current_floor]["stores"]

    closest = None
    min_d = float("inf")

    for name, (sx, sy) in store_data.items():
        if name.startswith("P") or name.startswith("Esc"):
            continue

        d = distance((x, y), (sx, sy))

        if d < min_d and d < Radius:   #Radius
            min_d = d
            closest = name

    if closest:
        if active_input == "source":
            source_var.set(closest)
        else:
            dest_var.set(closest)


# UI LAYOUT

main = tk.Frame(root)
main.pack(fill="both", expand=True)

map_frame = tk.Frame(main)
map_frame.pack(fill="both", expand=True)

control = tk.Frame(main, height=120)
control.pack(fill="x")

image_label = tk.Label(map_frame)
image_label.pack(fill="both", expand=True)

floor_label = tk.Label(map_frame, font=("Arial", 22, "bold"), bg="white")
floor_label.place(x=20, y=20)

source_var = tk.StringVar()
dest_var = tk.StringVar()

source_combo = ttk.Combobox(control, textvariable=source_var, values=full_store_list, width=25)
source_combo.grid(row=0, column=1)

dest_combo = ttk.Combobox(control, textvariable=dest_var, values=full_store_list, width=25)
dest_combo.grid(row=0, column=3)

source_combo.bind("<Button-1>", lambda e: set_active_input("source"))
dest_combo.bind("<Button-1>", lambda e: set_active_input("dest"))

tk.Label(control, text="Source").grid(row=0, column=0)
tk.Label(control, text="Destination").grid(row=0, column=2)



# FLOOR SWITCH

def switch_floor(direction):
    global current_floor
    idx = floor_keys.index(current_floor)
    idx = (idx + 1) % len(floor_keys) if direction == "next" else (idx - 1) % len(floor_keys)
    current_floor = floor_keys[idx]
    update_image()

tk.Button(control, text="⬅ Prev", command=lambda: switch_floor("prev")).grid(row=1, column=0)
tk.Button(control, text="Next ➡", command=lambda: switch_floor("next")).grid(row=1, column=1)


# UPDATE IMAGE
def update_image():
    display = floors[current_floor]["img"].copy()

    floor_label.config(text={
        "GF": "Ground Floor",
        "F1": "First Floor",
        "F2": "Second Floor",
        "F3": "Third Floor",
    }[current_floor])

    if last_paths[current_floor]:
        store = floors[current_floor]["stores"]
        for i in range(len(last_paths[current_floor])-1):
            cv2.line(display, store[last_paths[current_floor][i]],
                     store[last_paths[current_floor][i+1]], (0,0,255), 4)

    if last_source in floors[current_floor]["stores"]:
        cv2.circle(display, floors[current_floor]["stores"][last_source], 10, (0,255,0), -1)

    if last_dest in floors[current_floor]["stores"]:
        cv2.circle(display, floors[current_floor]["stores"][last_dest], 10, (0,0,255), -1)

    img_tk = convert(display)
    image_label.config(image=img_tk)
    image_label.image = img_tk
    image_label.bind("<Button-1>", on_click)


def set_active_input(field):
    global active_input
    active_input = field


def find_and_draw():
    global last_paths, last_source, last_dest

    s = source_var.get()
    d = dest_var.get()

    last_source = s
    last_dest = d

    sf = get_floor(s)
    df = get_floor(d)

    active_input = "source"

    floor_sequence = []
    floor_path_label = tk.Label(control, text="", font=("Arial", 14, "bold"), fg="green")
    floor_path_label.grid(row=3, column=0, columnspan=5)

    # 🔥 CLEAR PREVIOUS STATE
    last_paths = {"GF": None, "F1": None, "F2": None, "F3": None}
    floor_path_label.config(text="")  # clear old route

    # SAME FLOOR

    if sf == df:
        data = floors[sf]

        start = nearest_node(data["stores"][s], data["stores"])
        end = nearest_node(data["stores"][d], data["stores"])

        last_paths[sf] = astar(data["graph"], start, end, data["stores"])

        floor_sequence = [sf]


    # MULTI FLOOR

    else:
        floor_sequence.append(sf)

        # STEP 1 → go to nearest escalator
        start = nearest_node(floors[sf]["stores"][s], floors[sf]["stores"])

        esc = min(
            ["Esc1", "Esc2"],
            key=lambda e: distance(
                floors[sf]["stores"][start],
                floors[sf]["stores"][e]
            )
        )

        last_paths[sf] = astar(floors[sf]["graph"],start,esc,floors[sf]["stores"])

        current = sf
        current_esc = esc

        # STEP 2 → climb floors
        while current != df:
            next_floor, next_esc = vertical_links[(current, current_esc)]

            floor_sequence.append(next_floor)

            data = floors[next_floor]

            # FINAL FLOOR
            if next_floor == df:
                end = nearest_node(data["stores"][d], data["stores"])

                last_paths[next_floor] = astar(data["graph"], next_esc, end,data["stores"])

            else:
                # intermediate floor → move to escalator
                next_esc_target = min(
                    ["Esc1", "Esc2"],
                    key=lambda e: distance(
                        data["stores"][next_esc],
                        data["stores"][e]
                    )
                )

                last_paths[next_floor] = astar( data["graph"],next_esc,next_esc_target, data["stores"] )

                current_esc = next_esc_target

            current = next_floor


    floor_path_text = " → ".join(floor_sequence)
    floor_path_label.config(text=f"Route: {floor_path_text}")

    update_image()

tk.Button(control, text="Show Path", command=find_and_draw).grid(row=0, column=4)

# START

update_image()
root.mainloop()
