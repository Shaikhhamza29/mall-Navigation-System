from data.Imp import *
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



def filter_combobox(event, var, combo):
    typed = var.get().lower()

    if typed == "":
        data = full_store_list
    else:
        data = [item for item in full_store_list if typed in item.lower()]

    combo['values'] = data

    # show dropdown automatically
    if data:
        combo.event_generate('<Down>')

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
    header_height = header.winfo_height() or 60
    scale_y = (screen_h - header_height) / h

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
            draw_arrow(display, store[last_paths[current_floor][i]],
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

def animate_card_in():
    card_width = 350
    card_height = 450

    screen_w = root.winfo_width()
    screen_h = root.winfo_height()

    start_x = screen_w      # off-screen right
    end_x = screen_w - card_width - 20
    y = screen_h - card_height - 20

    def slide(x):
        if x <= end_x:
            card.place(x=end_x, y=y, width=card_width, height=card_height)
            return

        card.place(x=x, y=y, width=card_width, height=card_height)
        root.after(5, lambda: slide(x - 20))  # speed (lower = smoother)

    slide(start_x)

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

    # -----------------------------
    # UPDATE FLOATING CARD
    # -----------------------------
    card.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20, width=350, height=450)

    # Clear old steps
    for widget in steps_frame.winfo_children():
        widget.destroy()

    # Update title
    title_label.config(text=d)
    floor_info_label.config(text=f"{df} floor")

    # Add steps
    add_step("🟢", "Start", s)
    add_step("🚶", "Walking", f"{len(floor_sequence)} floor transition")

    # If multi-floor
    if len(floor_sequence) > 1:
        add_step("⬆", "Change Floor", " → ".join(floor_sequence))

    add_step("📍", "Arrive", d)



    update_image()
# UI LAYOUT

# HEADER FIRST
header = tk.Frame(root, bg="#f5f5f5", height=60)
header.pack(side="top", fill="x")
header.pack_propagate(False)

# THEN MAIN
main = tk.Frame(root)
main.pack(fill="both", expand=True)

# LEFT SIDE (Back + Title)
left_frame = tk.Frame(header, bg="#f5f5f5")
left_frame.pack(side="left", padx=20)

tk.Button(
    left_frame,
    text="←",
    font=("Arial", 14, "bold"),
    bg="#4a7dfc",
    fg="white",
    relief="flat",
    width=3,
    command=lambda: print("Back pressed")
).pack(side="left", padx=5)

tk.Label(
    left_frame,
    text="Map",
    font=("Arial", 16, "bold"),
    bg="#f5f5f5"
).pack(side="left", padx=10)

# RIGHT SIDE
right_frame = tk.Frame(header, bg="#f5f5f5")
right_frame.pack(side="right", padx=20)

time_label = tk.Label(right_frame, font=("Arial", 14, "bold"), bg="#f5f5f5")
time_label.pack(side="left", padx=10)

date_label = tk.Label(right_frame, font=("Arial", 10), bg="#f5f5f5")
date_label.pack(side="left", padx=10)

weather_label = tk.Label(right_frame, text="☀ 25°C", font=("Arial", 12), bg="#f5f5f5")
weather_label.pack(side="left", padx=10)

tk.Button(
    right_frame,
    text="EN",
    font=("Arial", 10, "bold"),
    bg="#e0e0e0",
    relief="flat",
    width=4
).pack(side="left", padx=10)


def update_time():
    now = datetime.datetime.now()
    time_label.config(text=now.strftime("%H:%M"))
    date_label.config(text=now.strftime("%A, %d %B"))
    root.after(1000, update_time)

update_time()



image_label = tk.Label(main)
image_label.pack(fill="both", expand=True)














floor_label = tk.Label(header, font=("Arial", 18, "bold"), bg="#f5f5f5")
floor_label.pack(side="left", padx=20)

source_var = tk.StringVar()
dest_var = tk.StringVar()

# -----------------------------
# CONTROL BOX (LEFT BELOW FLOORS)
# -----------------------------

control_box = tk.Frame(main, bg="#e6e6e6", bd=1, relief="solid")
control_box.place(x=25, y=260)   # 👈 adjusted to sit below floor panel

inner = tk.Frame(control_box, bg="#f2f2f2", padx=20, pady=15)
inner.pack(padx=2, pady=2)

tk.Label(inner, text="Source", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(anchor="w")
source_combo = ttk.Combobox(inner, textvariable=source_var, values=full_store_list, width=25)
source_combo.pack(pady=5)

tk.Label(inner, text="Destination", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(anchor="w")
dest_combo = ttk.Combobox(inner, textvariable=dest_var, values=full_store_list, width=25)
dest_combo.pack(pady=5)

tk.Button(
    inner,
    text="📍 Show Route",
    bg="#1f8f3a",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=10,
    pady=5,
    command=find_and_draw
).pack(pady=10)

source_combo.bind("<KeyRelease>", lambda e: filter_combobox(e, source_var, source_combo))
dest_combo.bind("<KeyRelease>", lambda e: filter_combobox(e, dest_var, dest_combo))

map_frame = tk.Frame(main)
map_frame.pack(fill="both", expand=True)

control = tk.Frame(main, height=120)
control.pack_forget()

image_label = tk.Label(map_frame)
image_label.pack(fill="both", expand=True)

floor_label = tk.Label(header, font=("Arial", 18, "bold"), bg="#f5f5f5")
floor_label.pack(side="left", padx=20)

source_var = tk.StringVar()
dest_var = tk.StringVar()

# -----------------------------
# MODERN CONTROL PANEL (CENTER BOX)
# -----------------------------
control.place_forget()  # remove old layout

control_box = tk.Frame(map_frame, bg="#e6e6e6", bd=1, relief="solid")

# 👇 POSITION BELOW FLOOR SELECTOR
control_box.place(x=25, y=450)   # adjust Y if needed

inner = tk.Frame(control_box, bg="#f2f2f2", padx=20, pady=15)
inner.pack(padx=2, pady=2)

# SOURCE
tk.Label(inner, text="Source", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(anchor="w")
source_combo = ttk.Combobox(inner, textvariable=source_var, values=full_store_list, width=25)
source_combo.pack(pady=5)

# DESTINATION
tk.Label(inner, text="Destination", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(anchor="w")
dest_combo = ttk.Combobox(inner, textvariable=dest_var, values=full_store_list, width=25)
dest_combo.pack(pady=5)

# BUTTON
tk.Button(
    inner,
    text="📍 Show Route",
    bg="#1f8f3a",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=10,
    pady=5,
    command=find_and_draw
).pack(pady=10)

# KEEP bindings
source_combo.bind("<KeyRelease>", lambda e: filter_combobox(e, source_var, source_combo))
dest_combo.bind("<KeyRelease>", lambda e: filter_combobox(e, dest_var, dest_combo))

# -----------------------------
# FLOATING ROUTE CARD (HIDDEN INITIALLY)
# -----------------------------
card = tk.Frame(map_frame, bg="#f7f7f7", bd=1, relief="solid")

inner = tk.Frame(card, bg="#f7f7f7", padx=15, pady=15)
inner.pack(fill="both", expand=True)

# TITLE
title_label = tk.Label(inner, text="", font=("Arial", 14, "bold"), bg="#f7f7f7")
title_label.pack(anchor="w")

floor_info_label = tk.Label(inner, text="", font=("Arial", 10), fg="gray", bg="#f7f7f7")
floor_info_label.pack(anchor="w")

tk.Label(inner, text="Directions", font=("Arial", 12, "bold"), bg="#f7f7f7").pack(anchor="w", pady=(10,5))

steps_frame = tk.Frame(inner, bg="#f7f7f7")
steps_frame.pack(fill="x")

def add_step(icon, title, subtitle):
    f = tk.Frame(steps_frame, bg="#f7f7f7")
    f.pack(fill="x", pady=5)

    tk.Label(f, text=icon, font=("Arial", 16), bg="#f7f7f7").pack(side="left", padx=5)

    txt = tk.Frame(f, bg="#f7f7f7")
    txt.pack(side="left")

    tk.Label(txt, text=title, font=("Arial", 11, "bold"), bg="#f7f7f7").pack(anchor="w")
    tk.Label(txt, text=subtitle, font=("Arial", 9), fg="gray", bg="#f7f7f7").pack(anchor="w")

# CANCEL BUTTON
tk.Button(
    inner,
    text="Cancel",
    bg="#5f6770",
    fg="white",
    relief="flat",
    command=lambda: card.place_forget()
).pack(side="bottom", fill="x", pady=10)


# FLOOR SWITCH

def switch_floor(direction):
    global current_floor
    idx = floor_keys.index(current_floor)
    idx = (idx + 1) % len(floor_keys) if direction == "next" else (idx - 1) % len(floor_keys)
    current_floor = floor_keys[idx]
    update_image()

# -----------------------------
# MODERN VERTICAL FLOOR PANEL
# -----------------------------
floor_panel = tk.Frame(map_frame, bg="#e5e5e5")
floor_panel.place(x=20, y=100)

container = tk.Frame(floor_panel, bg="#f2f2f2", bd=1, relief="solid")
container.pack(padx=5, pady=5)

floor_order = ["F3", "F2", "F1", "GF"]

def set_floor(f):
    global current_floor
    current_floor = f
    update_image()
    highlight_active_floor()

def highlight_active_floor():
    for f, btn in floor_buttons.items():
        if f == current_floor:
            btn.config(bg="#4a7dfc", fg="white")
        else:
            btn.config(bg="#f2f2f2", fg="black")

floor_buttons = {}

# + BUTTON
btn_plus = tk.Button(
    container,
    text="+",
    font=("Arial", 16, "bold"),
    bg="#f2f2f2",
    relief="flat",
    width=6,
    command=lambda: switch_floor("next")
)
btn_plus.pack(fill="x")

# FLOOR BUTTONS
for f in floor_order:
    btn = tk.Button(
        container,
        text=f,
        font=("Arial", 14, "bold"),
        bg="#f2f2f2",
        relief="flat",
        height=2,
        command=lambda x=f: set_floor(x)
    )
    btn.pack(fill="x", pady=1)
    floor_buttons[f] = btn

# - BUTTON
btn_minus = tk.Button(
    container,
    text="-",
    font=("Arial", 16, "bold"),
    bg="#f2f2f2",
    relief="flat",
    width=6,
    command=lambda: switch_floor("prev")
)
btn_minus.pack(fill="x")

highlight_active_floor()


# START

update_image()
root.mainloop()
root.update_idletasks()
