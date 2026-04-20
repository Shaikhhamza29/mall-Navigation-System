import tkinter as tk
from data.stores import *
from PIL import Image, ImageTk


def open_store_details(root, full_store_list):

    def on_search(event=None):
        query = search_var.get().lower()

        filtered = [
            s for s in store_data
            if query in s["name"].lower()
        ]

        # update cards
        create_cards(filtered)

        # update suggestions
        suggestion_box.delete(0, tk.END)

        if query == "":
            suggestion_box.place_forget()
            return

        for item in filtered[:10]:
            suggestion_box.insert(tk.END, item["name"])

        if filtered:
            suggestion_box.place(x=0, y=45, width=search_outer.winfo_width())
        else:
            suggestion_box.place_forget()


    # -----------------------------
    # WINDOW
    # -----------------------------
    win = tk.Toplevel(root)
    win.attributes("-fullscreen", True)
    win.configure(bg="#f4f6f8")

    win.bind("<Escape>", lambda e: win.destroy())

    # -----------------------------
    # HEADER
    # -----------------------------
    header = tk.Frame(win, bg="#4a7dfc", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Store Details",
        font=("Segoe UI", 20, "bold"),
        bg="#4a7dfc",
        fg="white"
    ).pack(side="left", padx=30)

    tk.Button(
        header,
        text="← Back",
        font=("Segoe UI", 12, "bold"),
        bg="white",
        fg="#333",
        relief="flat",
        padx=15,
        pady=5,
        command=win.destroy
    ).pack(side="right", padx=30)

    # -----------------------------
    # MAIN CONTAINER (CENTERED)
    # -----------------------------
    container = tk.Frame(win, bg="#f4f6f8")
    container.pack(expand=True)

    card = tk.Frame(container, bg="white", padx=40, pady=30)
    card.pack()

    # -----------------------------
    # TITLE
    # -----------------------------
    tk.Label(
        card,
        text="All Stores",
        font=("Segoe UI", 24, "bold"),
        bg="white",
        fg="#222"
    ).pack(pady=(10, 20))

    # -----------------------------
    # SEARCH BAR + ICON
    # -----------------------------
    search_var = tk.StringVar()

    search_container = tk.Frame(card, bg="white")
    search_container.pack(pady=10)

    # outer border (rounded feel)
    search_outer = tk.Frame(search_container, bg="#e0e0e0")
    search_outer.pack()

    # input + button row
    search_inner = tk.Frame(search_outer, bg="white")
    search_inner.pack(padx=2, pady=2)

    # ENTRY
    search_entry = tk.Entry(
        search_inner,
        textvariable=search_var,
        font=("Segoe UI", 14),
        width=35,
        bd=0,
        relief="flat"
    )
    search_entry.pack(side="left", ipady=10, padx=(10, 0))

    # -----------------------------

    # SUGGESTION LISTBOX
    # -----------------------------
    suggestion_box = tk.Listbox(
        search_outer,
        font=("Segoe UI", 12),
        height=6,
        bd=1,
        relief="solid"
    )

    # SEARCH BUTTON (ICON)
    search_btn = tk.Button(
        search_inner,
        text="🔍",
        font=("Segoe UI", 14),
        bg="white",
        relief="flat",
        cursor="hand2",
        command=lambda: on_search()
    )
    search_btn.pack(side="right", padx=10)
    # -----------------------------
    # SEARCH LOGIC (TEMP)
    # -----------------------------

    search_entry.bind("<KeyRelease>", on_search)
    # -----------------------------
    # CARD GRID CONTAINER
    # SCROLLABLE AREA
    # -----------------------------
    canvas = tk.Canvas(win, bg="#f4f6f8", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside canvas
    scroll_frame = tk.Frame(canvas, bg="#f4f6f8")

    window_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind("<Configure>", on_configure)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    def resize_frame(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_frame)
    # Example structure
    # -----------------------------
    # BUILD STORE DATA FROM REAL LIST
    # -----------------------------
    import os

    def clean_name(name):
        return name.lower().replace(" ", "_").replace("&", "").replace(".", "")

    store_data = []

    for f, data in {
        "GF": stores_GF,
        "F1": stores_F1,
        "F2": stores_F2,
        "F3": stores_F3
    }.items():
        for name in data:
            if not name.startswith("P") and not name.startswith("Esc"):
                filename = clean_name(name) + ".png"
                path = os.path.join("logos", filename)

                store_data.append({
                    "name": name,
                    "floor": f,
                    "logo": path if os.path.exists(path) else None
                })

    def select_suggestion(event):
        selected = suggestion_box.get(suggestion_box.curselection())

        search_var.set(selected)
        suggestion_box.place_forget()

        # show only selected store
        filtered = [s for s in store_data if s["name"] == selected]
        create_cards(filtered)

    suggestion_box.bind("<<ListboxSelect>>", select_suggestion)



    def create_cards(data):

        # clear old cards
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        columns = max(4, win.winfo_screenwidth() // 300)
        for index, store in enumerate(data):
            row = index // columns
            col = index % columns

            card_box = tk.Frame(
                scroll_frame,
                bg="#f7f7f7",
                width=400,
                height=200,
                bd=1,
                relief="solid"
            )
            card_box.grid(row=row, column=col, padx=15, pady=15)
            scroll_frame.grid_columnconfigure(col, weight=1)
            card_box.pack_propagate(False)

            # LOGO
            # LOGO
            if store["logo"]:
                try:
                    img = Image.open(store["logo"])
                    img = img.resize((60, 60))
                    logo = ImageTk.PhotoImage(img)

                    label_img = tk.Label(card_box, image=logo, bg="#f7f7f7")
                    label_img.image = logo
                    label_img.pack(pady=(10, 5))

                except:
                    tk.Label(card_box, text="🏬", font=("Arial", 20), bg="#f7f7f7").pack(pady=(10, 5))
            else:
                tk.Label(card_box, text="🏬", font=("Arial", 20), bg="#f7f7f7").pack(pady=(10, 5))
            # STORE NAME
            tk.Label(
                card_box,
                text=store["name"],
                font=("Segoe UI", 11, "bold"),
                bg="#f7f7f7"
            ).pack()

            # FLOOR
            tk.Label(
                card_box,
                text=f"Floor : {store['floor']}",
                font=("Segoe UI", 9),
                fg="gray",
                bg="#f7f7f7"
            ).pack()


    create_cards(store_data)
