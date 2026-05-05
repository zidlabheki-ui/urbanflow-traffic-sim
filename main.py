import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import osmnx as ox
import threading

# ─── APP SETTINGS ─────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("UrbanFlow — Traffic Flow Modelling System")
app.geometry("1280x780")
app.resizable(True, True)

# ─── HEADER ───────────────────────────────────────────────
header = ctk.CTkFrame(app, fg_color="#185FA5", height=60, corner_radius=0)
header.pack(fill="x", side="top")

ctk.CTkLabel(header,
             text="UrbanFlow — Urban Traffic Flow Modelling System",
             font=ctk.CTkFont(size=18, weight="bold"),
             text_color="white").pack(side="left", padx=20, pady=15)

# ─── MAIN BODY ────────────────────────────────────────────
body = ctk.CTkFrame(app, fg_color="#EFF6FF", corner_radius=0)
body.pack(fill="both", expand=True)

# ─── SIDEBAR ──────────────────────────────────────────────
sidebar_outer = ctk.CTkFrame(body, fg_color="white", width=270,
                              corner_radius=0, border_width=1,
                              border_color="#B5D4F4")
sidebar_outer.pack(fill="y", side="left")
sidebar_outer.pack_propagate(False)

sidebar = ctk.CTkScrollableFrame(sidebar_outer, fg_color="white", width=250)
sidebar.pack(fill="both", expand=True)

# ── Section: City ──
ctk.CTkLabel(sidebar, text="STEP 1 — SELECT CITY",
             font=ctk.CTkFont(size=11, weight="bold"),
             text_color="#185FA5").pack(anchor="w", padx=16, pady=(16, 6))

ctk.CTkLabel(sidebar, text="City / Metro Council",
             font=ctk.CTkFont(size=12),
             text_color="#378ADD").pack(anchor="w", padx=16)
city_entry = ctk.CTkEntry(sidebar,
                           placeholder_text="e.g. Bulawayo, Zimbabwe",
                           fg_color="#EFF6FF", border_color="#B5D4F4",
                           width=230)
city_entry.pack(padx=16, pady=(2, 8))

load_city_button = ctk.CTkButton(sidebar, text="Search City Roads",
                                  fg_color="#185FA5", hover_color="#0C447C",
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  height=36, width=230, corner_radius=8)
load_city_button.pack(padx=16, pady=(0, 6))

city_status_label = ctk.CTkLabel(sidebar, text="Enter a city to begin",
                                  font=ctk.CTkFont(size=10),
                                  text_color="#888")
city_status_label.pack(padx=16, pady=(0, 10))

# ── Section: Road Selection ──
ctk.CTkFrame(sidebar, fg_color="#B5D4F4", height=1).pack(
    fill="x", padx=16, pady=(0, 10))

ctk.CTkLabel(sidebar, text="STEP 2 — SELECT ROAD",
             font=ctk.CTkFont(size=11, weight="bold"),
             text_color="#185FA5").pack(anchor="w", padx=16, pady=(0, 6))

ctk.CTkLabel(sidebar, text="Search Road Name",
             font=ctk.CTkFont(size=12),
             text_color="#378ADD").pack(anchor="w", padx=16)
road_search_entry = ctk.CTkEntry(sidebar,
                                  placeholder_text="e.g. Joshua Nkomo",
                                  fg_color="#EFF6FF", border_color="#B5D4F4",
                                  width=230)
road_search_entry.pack(padx=16, pady=(2, 8))

ctk.CTkLabel(sidebar, text="Select Road",
             font=ctk.CTkFont(size=12),
             text_color="#378ADD").pack(anchor="w", padx=16)
road_var = ctk.StringVar(value="Load city first")
road_dropdown = ctk.CTkOptionMenu(sidebar, values=["Load city first"],
                                   variable=road_var,
                                   fg_color="#185FA5", width=230,
                                   dynamic_resizing=False)
road_dropdown.pack(padx=16, pady=(2, 8))
road_dropdown.configure(state="disabled")

load_road_button = ctk.CTkButton(sidebar, text="Load Selected Road",
                                  fg_color="#0C447C", hover_color="#042C53",
                                  font=ctk.CTkFont(size=12),
                                  height=36, width=230, corner_radius=8)
load_road_button.pack(padx=16, pady=(0, 6))
load_road_button.configure(state="disabled")

road_status_label = ctk.CTkLabel(sidebar, text="No road selected",
                                  font=ctk.CTkFont(size=10),
                                  text_color="#888")
road_status_label.pack(padx=16, pady=(0, 10))

# ── Section: Parameters ──
ctk.CTkFrame(sidebar, fg_color="#B5D4F4", height=1).pack(
    fill="x", padx=16, pady=(0, 10))

ctk.CTkLabel(sidebar, text="STEP 3 — SET PARAMETERS",
             font=ctk.CTkFont(size=11, weight="bold"),
             text_color="#185FA5").pack(anchor="w", padx=16, pady=(0, 6))

ctk.CTkLabel(sidebar, text="Number of Lanes",
             font=ctk.CTkFont(size=12),
             text_color="#378ADD").pack(anchor="w", padx=16)
lanes_var = ctk.StringVar(value="2")
lanes_menu = ctk.CTkOptionMenu(sidebar,
                                values=["1","2","3","4","5","6"],
                                variable=lanes_var,
                                fg_color="#185FA5", width=230)
lanes_menu.pack(padx=16, pady=(2, 10))

ctk.CTkLabel(sidebar, text="Speed Limit (km/h)",
             font=ctk.CTkFont(size=12),
             text_color="#378ADD").pack(anchor="w", padx=16)
speed_val_label = ctk.CTkLabel(sidebar, text="60 km/h",
                                font=ctk.CTkFont(size=11),
                                text_color="#185FA5")
speed_val_label.pack(anchor="e", padx=16)

def update_speed(val):
    speed_val_label.configure(text=f"{int(float(val))} km/h")

speed_slider = ctk.CTkSlider(sidebar, from_=20, to=120,
                              number_of_steps=20, command=update_speed,
                              button_color="#185FA5",
                              progress_color="#378ADD", width=230)
speed_slider.set(60)
speed_slider.pack(padx=16, pady=(2, 10))

ctk.CTkLabel(sidebar, text="Traffic Density (%)",
             font=ctk.CTkFont(size=12),
             text_color="#378ADD").pack(anchor="w", padx=16)
density_val_label = ctk.CTkLabel(sidebar, text="65%",
                                  font=ctk.CTkFont(size=11),
                                  text_color="#185FA5")
density_val_label.pack(anchor="e", padx=16)

def update_density(val):
    density_val_label.configure(text=f"{int(float(val))}%")

density_slider = ctk.CTkSlider(sidebar, from_=0, to=100,
                                number_of_steps=20, command=update_density,
                                button_color="#185FA5",
                                progress_color="#378ADD", width=230)
density_slider.set(65)
density_slider.pack(padx=16, pady=(2, 10))

ctk.CTkLabel(sidebar, text="Simulation Time (mins)",
             font=ctk.CTkFont(size=12),
             text_color="#378ADD").pack(anchor="w", padx=16)
time_val_label = ctk.CTkLabel(sidebar, text="30 mins",
                               font=ctk.CTkFont(size=11),
                               text_color="#185FA5")
time_val_label.pack(anchor="e", padx=16)

def update_time(val):
    time_val_label.configure(text=f"{int(float(val))} mins")

time_slider = ctk.CTkSlider(sidebar, from_=5, to=120,
                             number_of_steps=23, command=update_time,
                             button_color="#185FA5",
                             progress_color="#378ADD", width=230)
time_slider.set(30)
time_slider.pack(padx=16, pady=(2, 16))

# ── Section: Actions ──
ctk.CTkFrame(sidebar, fg_color="#B5D4F4", height=1).pack(
    fill="x", padx=16, pady=(0, 10))

ctk.CTkLabel(sidebar, text="STEP 4 — RUN",
             font=ctk.CTkFont(size=11, weight="bold"),
             text_color="#185FA5").pack(anchor="w", padx=16, pady=(0, 6))

run_button = ctk.CTkButton(sidebar, text="▶  Run Simulation",
                            fg_color="#185FA5", hover_color="#0C447C",
                            font=ctk.CTkFont(size=14, weight="bold"),
                            height=40, width=230, corner_radius=8)
run_button.pack(padx=16, pady=(0, 8))

stop_button = ctk.CTkButton(sidebar, text="⏹  Stop Simulation",
                             fg_color="#A32D2D", hover_color="#791F1F",
                             font=ctk.CTkFont(size=13),
                             height=36, width=230, corner_radius=8)
stop_button.pack(padx=16, pady=(0, 10))

ctk.CTkFrame(sidebar, fg_color="#B5D4F4", height=1).pack(
    fill="x", padx=16, pady=(0, 10))

# ── Section: Data ──
ctk.CTkLabel(sidebar, text="DATA IMPORT",
             font=ctk.CTkFont(size=11, weight="bold"),
             text_color="#185FA5").pack(anchor="w", padx=16, pady=(0, 6))

upload_button = ctk.CTkButton(sidebar, text="+ Import CSV / Excel Data",
                               fg_color="white", text_color="#185FA5",
                               hover_color="#EFF6FF", border_width=1,
                               border_color="#378ADD",
                               font=ctk.CTkFont(size=13),
                               height=36, width=230, corner_radius=8)
upload_button.pack(padx=16, pady=(0, 4))

data_status_label = ctk.CTkLabel(sidebar, text="No data imported",
                                  font=ctk.CTkFont(size=10),
                                  text_color="#888")
data_status_label.pack(padx=16, pady=(0, 10))

ctk.CTkFrame(sidebar, fg_color="#B5D4F4", height=1).pack(
    fill="x", padx=16, pady=(0, 10))

# ── Section: Export ──
ctk.CTkLabel(sidebar, text="EXPORT RESULTS",
             font=ctk.CTkFont(size=11, weight="bold"),
             text_color="#185FA5").pack(anchor="w", padx=16, pady=(0, 6))

export_csv_button = ctk.CTkButton(sidebar, text="Export Data as CSV",
                                   fg_color="white", text_color="#185FA5",
                                   hover_color="#EFF6FF", border_width=1,
                                   border_color="#378ADD",
                                   font=ctk.CTkFont(size=13),
                                   height=36, width=230, corner_radius=8)
export_csv_button.pack(padx=16, pady=(0, 8))

export_pdf_button = ctk.CTkButton(sidebar, text="Export Report as PDF",
                                   fg_color="white", text_color="#185FA5",
                                   hover_color="#EFF6FF", border_width=1,
                                   border_color="#378ADD",
                                   font=ctk.CTkFont(size=13),
                                   height=36, width=230, corner_radius=8)
export_pdf_button.pack(padx=16, pady=(0, 8))

reset_button = ctk.CTkButton(sidebar, text="↺  Reset All",
                              fg_color="white", text_color="#378ADD",
                              hover_color="#EFF6FF", border_width=1,
                              border_color="#378ADD",
                              font=ctk.CTkFont(size=13),
                              height=36, width=230, corner_radius=8)
reset_button.pack(padx=16, pady=(0, 16))

# ─── CONTENT AREA ─────────────────────────────────────────
content = ctk.CTkFrame(body, fg_color="#EFF6FF", corner_radius=0)
content.pack(fill="both", expand=True, padx=16, pady=16)

# ─── METRIC CARDS ─────────────────────────────────────────
metrics_frame = ctk.CTkFrame(content, fg_color="transparent")
metrics_frame.pack(fill="x", pady=(0, 12))

def make_metric_card(parent, label, value, sub):
    card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10,
                         border_width=1, border_color="#B5D4F4")
    card.pack(side="left", expand=True, fill="x", padx=6)
    ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=11),
                 text_color="#378ADD").pack(anchor="w", padx=12, pady=(10,0))
    val_lbl = ctk.CTkLabel(card, text=value,
                            font=ctk.CTkFont(size=22, weight="bold"),
                            text_color="#042C53")
    val_lbl.pack(anchor="w", padx=12)
    ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=11),
                 text_color="#888").pack(anchor="w", padx=12, pady=(0,10))
    return val_lbl

avg_speed_label  = make_metric_card(metrics_frame, "Avg Speed",
                                     "-- km/h", "not yet simulated")
flow_label       = make_metric_card(metrics_frame, "Vehicle Flow",
                                     "--", "vehicles / hour")
congestion_label = make_metric_card(metrics_frame, "Congestion",
                                     "--", "index (0-1)")
jam_label        = make_metric_card(metrics_frame, "Jam Length",
                                     "-- km", "estimated queue")

road_info_label  = ctk.CTkLabel(content,
                                 text="No road selected — search a city and pick a road",
                                 font=ctk.CTkFont(size=12),
                                 text_color="#378ADD")
road_info_label.pack(anchor="w", padx=6, pady=(0, 6))

# ─── TABS ─────────────────────────────────────────────────
tab_view = ctk.CTkTabview(content, fg_color="white",
                           segmented_button_fg_color="#EFF6FF",
                           segmented_button_selected_color="#185FA5",
                           segmented_button_selected_hover_color="#0C447C",
                           segmented_button_unselected_color="#EFF6FF",
                           segmented_button_unselected_hover_color="#B5D4F4",
                           text_color="white",
                           border_width=1, border_color="#B5D4F4")
tab_view.pack(fill="both", expand=True)

tab_sim    = tab_view.add("Road Simulation")
tab_map    = tab_view.add("Road Map")
tab_charts = tab_view.add("Charts")

# ── Tab 1: Simulation ──
road_canvas = tk.Canvas(tab_sim, bg="#1a2a3a", highlightthickness=0)
road_canvas.pack(fill="both", expand=True, padx=12, pady=(8,4))

legend_frame = ctk.CTkFrame(tab_sim, fg_color="transparent")
legend_frame.pack(anchor="w", padx=12, pady=(0,8))
for color, lbl in [("#185FA5","Moving"),
                   ("#E24B4A","Stopped"),
                   ("#BA7517","Slowing")]:
    leg = ctk.CTkFrame(legend_frame, fg_color="transparent")
    leg.pack(side="left", padx=8)
    tk.Label(leg, bg=color, width=2, height=1).pack(side="left", padx=(0,4))
    ctk.CTkLabel(leg, text=lbl, font=ctk.CTkFont(size=11),
                 text_color="#444").pack(side="left")

# ── Tab 2: Road Map ──
fig_map, ax_map = plt.subplots(figsize=(7, 4))
fig_map.patch.set_facecolor("#ffffff")
ax_map.set_facecolor("#EFF6FF")
ax_map.set_title("Select a road to see it highlighted on the map",
                  color="#378ADD", fontsize=10)
ax_map.axis("off")
fig_map.tight_layout()
map_canvas_widget = FigureCanvasTkAgg(fig_map, master=tab_map)
map_canvas_widget.get_tk_widget().pack(fill="both", expand=True,
                                        padx=8, pady=8)

# ── Tab 3: Charts ──
charts_frame = ctk.CTkFrame(tab_charts, fg_color="transparent")
charts_frame.pack(fill="both", expand=True)

flow_card = ctk.CTkFrame(charts_frame, fg_color="white", corner_radius=12,
                          border_width=1, border_color="#B5D4F4")
flow_card.pack(side="left", expand=True, fill="both",
               padx=(8,4), pady=8)
ctk.CTkLabel(flow_card, text="Vehicle Flow Over Time",
             font=ctk.CTkFont(size=12, weight="bold"),
             text_color="#185FA5").pack(anchor="w", padx=12, pady=(10,0))
fig1, ax1 = plt.subplots(figsize=(4, 2.8))
fig1.patch.set_facecolor("#ffffff")
ax1.set_facecolor("#EFF6FF")
ax1.set_xlabel("Time (s)", fontsize=8, color="#378ADD")
ax1.set_ylabel("Vehicles/hour", fontsize=8, color="#378ADD")
ax1.tick_params(colors="#378ADD", labelsize=7)
for spine in ax1.spines.values():
    spine.set_edgecolor("#B5D4F4")
fig1.tight_layout()
flow_canvas_chart = FigureCanvasTkAgg(fig1, master=flow_card)
flow_canvas_chart.get_tk_widget().pack(fill="both", expand=True,
                                        padx=8, pady=(0,8))

sd_card = ctk.CTkFrame(charts_frame, fg_color="white", corner_radius=12,
                        border_width=1, border_color="#B5D4F4")
sd_card.pack(side="left", expand=True, fill="both", padx=(4,8), pady=8)
ctk.CTkLabel(sd_card, text="Speed vs Density",
             font=ctk.CTkFont(size=12, weight="bold"),
             text_color="#185FA5").pack(anchor="w", padx=12, pady=(10,0))
fig2, ax2 = plt.subplots(figsize=(4, 2.8))
fig2.patch.set_facecolor("#ffffff")
ax2.set_facecolor("#EFF6FF")
ax2.set_xlabel("Density (veh/km)", fontsize=8, color="#378ADD")
ax2.set_ylabel("Speed (km/h)", fontsize=8, color="#378ADD")
ax2.tick_params(colors="#378ADD", labelsize=7)
for spine in ax2.spines.values():
    spine.set_edgecolor("#B5D4F4")
fig2.tight_layout()
sd_canvas_chart = FigureCanvasTkAgg(fig2, master=sd_card)
sd_canvas_chart.get_tk_widget().pack(fill="both", expand=True,
                                      padx=8, pady=(0,8))

# ─── DATA STORAGE ─────────────────────────────────────────
flow_history    = []
time_history    = []
density_history = []
speed_history   = []
sim_time        = 0
imported_data   = None
cars            = []
simulation_running  = False
city_graph          = None
all_road_names      = []
selected_road_edges = None
selected_road_name  = ""
selected_road_length_km = 0.0

# ─── STATUS BAR ───────────────────────────────────────────
status_bar = ctk.CTkFrame(app, fg_color="#0C447C",
                           height=28, corner_radius=0)
status_bar.pack(fill="x", side="bottom")

status_label = ctk.CTkLabel(status_bar,
    text="Ready — search a city to begin",
    font=ctk.CTkFont(size=11), text_color="#B5D4F4")
status_label.pack(side="left", padx=16, pady=4)

ctk.CTkLabel(status_bar, text="UrbanFlow v1.0",
             font=ctk.CTkFont(size=11),
             text_color="#B5D4F4").pack(side="right", padx=16, pady=4)

def set_status(msg):
    status_label.configure(text=msg)

# ─── CHART UPDATES ────────────────────────────────────────
def update_flow_chart():
    ax1.clear()
    ax1.set_facecolor("#EFF6FF")
    ax1.set_xlabel("Time (s)", fontsize=8, color="#378ADD")
    ax1.set_ylabel("Vehicles/hour", fontsize=8, color="#378ADD")
    ax1.tick_params(colors="#378ADD", labelsize=7)
    for spine in ax1.spines.values():
        spine.set_edgecolor("#B5D4F4")
    if flow_history:
        ax1.plot(time_history, flow_history,
                 color="#185FA5", linewidth=1.5)
        ax1.fill_between(time_history, flow_history,
                          alpha=0.2, color="#378ADD")
    fig1.tight_layout()
    flow_canvas_chart.draw()

def update_sd_chart():
    ax2.clear()
    ax2.set_facecolor("#EFF6FF")
    ax2.set_xlabel("Density (veh/km)", fontsize=8, color="#378ADD")
    ax2.set_ylabel("Speed (km/h)", fontsize=8, color="#378ADD")
    ax2.tick_params(colors="#378ADD", labelsize=7)
    for spine in ax2.spines.values():
        spine.set_edgecolor("#B5D4F4")
    d_range = np.linspace(0, 100, 100)
    v_free  = speed_slider.get()
    s_curve = v_free * (1 - d_range / 100)
    ax2.plot(d_range, s_curve, color="#B5D4F4",
             linewidth=1, linestyle="--", label="Theoretical")
    if density_history:
        ax2.scatter(density_history, speed_history,
                    color="#185FA5", s=10, alpha=0.6, label="Simulated")
        ax2.legend(fontsize=7)
    fig2.tight_layout()
    sd_canvas_chart.draw()

# ─── STEP 1: LOAD CITY ────────────────────────────────────
def load_city():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("No City",
                               "Please enter a city name first.")
        return
    city_status_label.configure(
        text="Searching... please wait", text_color="#BA7517")
    load_city_button.configure(state="disabled")
    set_status(f"Loading road data for {city}...")

    def fetch():
        global city_graph, all_road_names
        try:
            G = ox.graph_from_place(city, network_type="drive")
            city_graph = G
            edges = ox.graph_to_gdfs(G, nodes=False)
            names = set()
            if "name" in edges.columns:
                for n in edges["name"].dropna():
                    if isinstance(n, list):
                        for item in n:
                            if isinstance(item, str) and len(item) > 2:
                                names.add(item.strip())
                    elif isinstance(n, str) and len(n) > 2:
                        names.add(n.strip())
            all_road_names = sorted(list(names))
            app.after(0, lambda: finish_city_load(city))
        except Exception as e:
            app.after(0, lambda: city_load_error(str(e)))

    threading.Thread(target=fetch, daemon=True).start()

def finish_city_load(city):
    city_status_label.configure(
        text=f"Found {len(all_road_names)} roads in {city}",
        text_color="#0F6E56")
    load_city_button.configure(state="normal")
    road_dropdown.configure(
        state="normal",
        values=all_road_names if all_road_names else ["No named roads found"])
    road_var.set("Select a road...")
    load_road_button.configure(state="normal")
    set_status(f"City loaded — {len(all_road_names)} roads found. "
               f"Now select a road.")
    messagebox.showinfo("City Loaded",
                        f"Found {len(all_road_names)} named roads.\n\n"
                        f"Use the search box to filter roads,\n"
                        f"then select one from the dropdown.")

def city_load_error(err):
    city_status_label.configure(
        text="Failed — check city name", text_color="#A32D2D")
    load_city_button.configure(state="normal")
    set_status("City load failed.")
    messagebox.showerror("Load Failed",
                         f"Could not find city.\n\n"
                         f"Tips:\n"
                         f"- Be specific: 'Bulawayo, Zimbabwe'\n"
                         f"- Try: 'Harare, Zimbabwe'\n"
                         f"- Try: 'Nairobi, Kenya'\n\n"
                         f"Error: {err}")

load_city_button.configure(command=load_city)

# ─── ROAD SEARCH FILTER ───────────────────────────────────
def filter_roads(event=None):
    query = road_search_entry.get().strip().lower()
    if not all_road_names:
        return
    filtered = [r for r in all_road_names if query in r.lower()] \
               if query else all_road_names
    road_dropdown.configure(
        values=filtered if filtered else ["No match found"])
    if filtered:
        road_var.set(filtered[0])

road_search_entry.bind("<KeyRelease>", filter_roads)

# ─── STEP 2: LOAD SELECTED ROAD ───────────────────────────
def load_selected_road():
    global selected_road_edges, selected_road_name
    global selected_road_length_km, city_graph

    if city_graph is None:
        messagebox.showwarning("No City", "Please load a city first.")
        return
    road_name = road_var.get().strip()
    if not road_name or road_name in ["Load city first",
                                       "Select a road...",
                                       "No match found",
                                       "No named roads found"]:
        messagebox.showwarning("No Road", "Please select a valid road.")
        return

    road_status_label.configure(
        text="Loading road...", text_color="#BA7517")
    load_road_button.configure(state="disabled")
    set_status(f"Loading {road_name}...")

    def fetch():
        global selected_road_edges, selected_road_name
        global selected_road_length_km
        try:
            edges = ox.graph_to_gdfs(city_graph, nodes=False)
            # Filter edges matching this road name
            def matches(n):
                if isinstance(n, list):
                    return road_name in n
                return n == road_name
            mask = edges["name"].apply(
                lambda n: matches(n) if pd.notna(n) else False)
            road_edges = edges[mask]

            if road_edges.empty:
                app.after(0, lambda: road_load_error(
                    "No edges found for this road."))
                return

            # Calculate road length
            length_m = road_edges["length"].sum() \
                       if "length" in road_edges.columns else 0
            length_km = round(length_m / 1000, 2)

            # Get speed limit
            speed_limit = 50
            if "maxspeed" in road_edges.columns:
                speeds = []
                for s in road_edges["maxspeed"].dropna():
                    try:
                        if isinstance(s, list): s = s[0]
                        speeds.append(int(str(s).split()[0]))
                    except:
                        pass
                if speeds:
                    speed_limit = int(sum(speeds) / len(speeds))

            # Get lanes
            lanes = 2
            if "lanes" in road_edges.columns:
                lane_vals = []
                for l in road_edges["lanes"].dropna():
                    try:
                        if isinstance(l, list): l = l[0]
                        lane_vals.append(int(l))
                    except:
                        pass
                if lane_vals:
                    lanes = int(sum(lane_vals) / len(lane_vals))
                    lanes = max(1, min(6, lanes))

            app.after(0, lambda: finish_road_load(
                road_edges, road_name, length_km, speed_limit, lanes))
        except Exception as e:
            app.after(0, lambda: road_load_error(str(e)))

    threading.Thread(target=fetch, daemon=True).start()

def finish_road_load(road_edges, name, length_km, speed_limit, lanes):
    global selected_road_edges, selected_road_name
    global selected_road_length_km
    selected_road_edges     = road_edges
    selected_road_name      = name
    selected_road_length_km = length_km

    road_status_label.configure(
        text=f"Loaded: {name} ({length_km} km)",
        text_color="#0F6E56")
    load_road_button.configure(state="normal")

    # Auto-fill parameters from real data
    speed_slider.set(min(120, max(20, speed_limit)))
    update_speed(speed_limit)
    lanes_var.set(str(lanes))
    road_info_label.configure(
        text=f"Selected road: {name}  |  "
             f"Length: {length_km} km  |  "
             f"Lanes: {lanes}  |  "
             f"Speed limit: {speed_limit} km/h")

    # Draw road on map — highlighted
    ax_map.clear()
    ax_map.set_facecolor("#1a2a3a")
    fig_map.patch.set_facecolor("#1a2a3a")

    # Draw full city network faintly
    all_edges = ox.graph_to_gdfs(city_graph, nodes=False)
    all_edges.plot(ax=ax_map, color="#2a3f55",
                   linewidth=0.4, alpha=0.5)

    # Highlight selected road in bright blue
    road_edges.plot(ax=ax_map, color="#378ADD",
                    linewidth=3, alpha=1.0)

    ax_map.set_title(f"{name}  —  {city_entry.get().strip()}",
                      color="white", fontsize=11)
    ax_map.axis("off")
    fig_map.tight_layout()
    map_canvas_widget.draw()

    tab_view.set("Road Map")
    set_status(f"Road loaded: {name} | "
               f"{length_km} km | {lanes} lanes | "
               f"{speed_limit} km/h speed limit")
    messagebox.showinfo("Road Loaded",
                        f"Road: {name}\n"
                        f"Length: {length_km} km\n"
                        f"Lanes: {lanes}\n"
                        f"Speed limit: {speed_limit} km/h\n\n"
                        f"Parameters auto-filled from real data.\n"
                        f"Click Run Simulation to begin!")

def road_load_error(err):
    road_status_label.configure(
        text="Failed to load road", text_color="#A32D2D")
    load_road_button.configure(state="normal")
    messagebox.showerror("Road Load Failed", f"Error:\n{err}")

load_road_button.configure(command=load_selected_road)

# ─── CSV IMPORT ───────────────────────────────────────────
def import_data():
    global imported_data
    file_path = filedialog.askopenfilename(
        title="Select Traffic Data File",
        filetypes=[("CSV files", "*.csv"),
                   ("Excel files", "*.xlsx *.xls"),
                   ("All files", "*.*")])
    if not file_path:
        return
    try:
        df = pd.read_csv(file_path) \
             if file_path.endswith(".csv") else pd.read_excel(file_path)
        df.columns = [c.strip().lower() for c in df.columns]
        speed_col   = next(
            (c for c in df.columns if "speed" in c), None)
        density_col = next(
            (c for c in df.columns
             if "density" in c or "volume" in c or "flow" in c), None)
        if speed_col and density_col:
            imported_data = df
            speeds    = df[speed_col].dropna().tolist()
            densities = df[density_col].dropna().tolist()
            avg_spd   = sum(speeds) / len(speeds)
            speed_slider.set(min(120, max(20, avg_spd)))
            update_speed(avg_spd)
            density_history.clear()
            speed_history.clear()
            for s, d in zip(speeds[:50], densities[:50]):
                speed_history.append(round(float(s), 2))
                density_history.append(round(float(d), 2))
            update_sd_chart()
            data_status_label.configure(
                text=f"Loaded: {len(df)} rows", text_color="#0F6E56")
            set_status(f"Data imported — {len(df)} rows loaded.")
            messagebox.showinfo("Data Imported",
                                f"Loaded {len(df)} rows.\n"
                                f"Speed: '{speed_col}'\n"
                                f"Density: '{density_col}'")
        else:
            imported_data = df
            data_status_label.configure(
                text=f"Loaded: {len(df)} rows (check columns)",
                text_color="#BA7517")
            messagebox.showwarning("Columns Not Detected",
                                   f"Loaded {len(df)} rows.\n"
                                   f"Columns: {list(df.columns)}\n\n"
                                   f"Name columns 'speed' and 'density'.")
    except Exception as e:
        messagebox.showerror("Import Error",
                             f"Could not read file:\n{str(e)}")

upload_button.configure(command=import_data)

# ─── EXPORT CSV ───────────────────────────────────────────
def export_csv():
    if not flow_history:
        messagebox.showwarning("No Data", "Run simulation first.")
        return
    fp = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")])
    if not fp:
        return
    try:
        pd.DataFrame({
            "time_s":       time_history,
            "vehicle_flow": flow_history,
            "density":      density_history
                            if len(density_history) == len(time_history)
                            else [None]*len(time_history),
            "avg_speed":    speed_history
                            if len(speed_history) == len(time_history)
                            else [None]*len(time_history),
        }).to_csv(fp, index=False)
        set_status(f"CSV saved to {fp}")
        messagebox.showinfo("Exported", f"Saved to:\n{fp}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

export_csv_button.configure(command=export_csv)

# ─── EXPORT PDF ───────────────────────────────────────────
def export_pdf():
    if not flow_history:
        messagebox.showwarning("No Data", "Run simulation first.")
        return
    fp = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")])
    if not fp:
        return
    try:
        from matplotlib.backends.backend_pdf import PdfPages
        speeds   = [c["speed"] for c in cars] if cars else [0]
        avg_spd  = round(sum(speeds)/len(speeds), 1)
        flow_val = int(len(cars)*avg_spd*0.8) if cars else 0
        cong     = round(max(0, 1-(avg_spd/speed_slider.get())), 2)

        with PdfPages(fp) as pdf:
            # Page 1 — Summary
            fs, axs = plt.subplots(figsize=(8.27, 11.69))
            axs.axis("off")
            fs.patch.set_facecolor("white")
            axs.add_patch(plt.Rectangle(
                (0, 0.92), 1, 0.08,
                transform=axs.transAxes, color="#185FA5"))
            axs.text(0.05, 0.96,
                     "UrbanFlow — Traffic Simulation Report",
                     transform=axs.transAxes,
                     fontsize=15, fontweight="bold",
                     color="white", va="center")
            info = [
                ("Road",         selected_road_name or "N/A"),
                ("City",         city_entry.get() or "N/A"),
                ("Length",       f"{selected_road_length_km} km"),
                ("Lanes",        lanes_var.get()),
                ("Speed Limit",  f"{int(speed_slider.get())} km/h"),
                ("Avg Speed",    f"{avg_spd} km/h"),
                ("Vehicle Flow", f"{flow_val} veh/hr"),
                ("Congestion",   str(cong)),
            ]
            y = 0.85
            for k, v in info:
                axs.text(0.05, y, k,  transform=axs.transAxes,
                         fontsize=11, color="#378ADD")
                axs.text(0.45, y, v,  transform=axs.transAxes,
                         fontsize=11, color="#042C53", fontweight="bold")
                y -= 0.06
            if selected_road_edges is not None:
                ax_mini = fs.add_axes([0.05, 0.1, 0.9, 0.38])
                ax_mini.set_facecolor("#1a2a3a")
                all_e = ox.graph_to_gdfs(city_graph, nodes=False)
                all_e.plot(ax=ax_mini, color="#2a3f55",
                           linewidth=0.3, alpha=0.5)
                selected_road_edges.plot(ax=ax_mini, color="#378ADD",
                                          linewidth=2.5)
                ax_mini.set_title(
                    f"{selected_road_name} — "
                    f"{city_entry.get()}",
                    color="#185FA5", fontsize=9)
                ax_mini.axis("off")
            pdf.savefig(fs)
            plt.close(fs)

            # Page 2 — Charts
            fc, (c1, c2) = plt.subplots(1, 2, figsize=(11.69, 4))
            fc.patch.set_facecolor("white")
            c1.plot(time_history, flow_history,
                    color="#185FA5", linewidth=1.5)
            c1.fill_between(time_history, flow_history,
                             alpha=0.2, color="#378ADD")
            c1.set_title("Vehicle Flow Over Time", color="#185FA5")
            c1.set_xlabel("Time (s)",      color="#378ADD")
            c1.set_ylabel("Vehicles/hour", color="#378ADD")
            c1.set_facecolor("#EFF6FF")
            dr = np.linspace(0, 100, 100)
            c2.plot(dr, speed_slider.get()*(1-dr/100),
                    color="#B5D4F4", linestyle="--", label="Theoretical")
            if density_history:
                c2.scatter(density_history, speed_history,
                           color="#185FA5", s=10, alpha=0.6,
                           label="Simulated")
                c2.legend(fontsize=8)
            c2.set_title("Speed vs Density",  color="#185FA5")
            c2.set_xlabel("Density (veh/km)", color="#378ADD")
            c2.set_ylabel("Speed (km/h)",     color="#378ADD")
            c2.set_facecolor("#EFF6FF")
            fc.tight_layout()
            pdf.savefig(fc)
            plt.close(fc)

        set_status(f"PDF saved to {fp}")
        messagebox.showinfo("Exported", f"PDF saved to:\n{fp}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

export_pdf_button.configure(command=export_pdf)

# ─── ROAD DRAWING ─────────────────────────────────────────
def draw_road():
    road_canvas.delete("all")
    w           = road_canvas.winfo_width()  or 900
    h           = road_canvas.winfo_height() or 200
    num_lanes   = int(lanes_var.get())
    lane_height = h // num_lanes
    for i in range(1, num_lanes):
        y = i * lane_height
        for x in range(0, w, 30):
            road_canvas.create_line(
                x, y, x+15, y,
                fill="#ffffb3", width=1, dash=(8,6))
    # Road name overlay
    if selected_road_name:
        road_canvas.create_text(
            w//2, 14,
            text=f"Simulating: {selected_road_name}  "
                 f"({selected_road_length_km} km)",
            fill="white", font=("Arial", 10))
    for car in cars:
        x, lane, speed = car["x"], car["lane"], car["speed"]
        y     = int((lane + 0.5) * lane_height)
        color = "#E24B4A" if speed < 10 else \
                "#BA7517" if speed < 30 else "#185FA5"
        road_canvas.create_rectangle(
            x, y-8, x+26, y+8,
            fill=color, outline="white", width=1)

# ─── SIMULATION LOOP ──────────────────────────────────────
def move_cars():
    global sim_time
    if not simulation_running:
        return
    w           = road_canvas.winfo_width() or 900
    speed_limit = speed_slider.get()
    for car in cars:
        ahead = [c for c in cars
                 if c["lane"] == car["lane"] and c["x"] > car["x"]]
        if ahead:
            nearest = min(ahead, key=lambda c: c["x"])
            gap     = nearest["x"] - car["x"]
            if gap < 40:
                car["speed"] = max(0, car["speed"] - 5)
            elif gap < 80:
                car["speed"] = min(speed_limit*0.6, car["speed"]+2)
            else:
                car["speed"] = min(speed_limit, car["speed"]+3)
        else:
            car["speed"] = min(speed_limit, car["speed"]+3)
        car["x"] += car["speed"] * 0.05
        if car["x"] > w + 30:
            car["x"]     = random.randint(-100, -30)
            car["speed"] = random.uniform(speed_limit*0.3, speed_limit)
    draw_road()
    update_metrics()
    sim_time += 1
    if sim_time % 20 == 0:
        speeds  = [c["speed"] for c in cars]
        avg_spd = sum(speeds)/len(speeds) if speeds else 0
        flow    = int(len(cars)*avg_spd*0.8)
        density = len(cars)/(road_canvas.winfo_width()/10)
        flow_history.append(flow)
        time_history.append(sim_time)
        if imported_data is None:
            density_history.append(round(density, 2))
            speed_history.append(round(avg_spd, 2))
        if len(flow_history) > 30:
            flow_history.pop(0)
            time_history.pop(0)
            if imported_data is None:
                density_history.pop(0)
                speed_history.pop(0)
        update_flow_chart()
        update_sd_chart()
    app.after(50, move_cars)

def update_metrics():
    if not cars:
        return
    speeds     = [c["speed"] for c in cars]
    avg_speed  = sum(speeds)/len(speeds)
    flow       = int(len(cars)*avg_speed*0.8)
    congestion = round(max(0, 1-(avg_speed/speed_slider.get())), 2)
    stopped    = [c for c in cars if c["speed"] < 5]
    jam_km     = round(len(stopped)*0.05, 1)
    avg_speed_label.configure(text=f"{int(avg_speed)} km/h")
    flow_label.configure(text=str(flow))
    congestion_label.configure(text=str(congestion))
    jam_label.configure(text=f"{jam_km} km")

# ─── RUN / STOP / RESET ───────────────────────────────────
def run_simulation():
    global cars, simulation_running, sim_time
    simulation_running = True
    sim_time = 0
    cars.clear()
    flow_history.clear()
    time_history.clear()
    if imported_data is None:
        density_history.clear()
        speed_history.clear()
    num_lanes   = int(lanes_var.get())
    density     = density_slider.get()/100
    speed_limit = speed_slider.get()
    num_cars    = int(30*density*num_lanes)
    w           = road_canvas.winfo_width() or 900
    for i in range(num_cars):
        cars.append({
            "x":     random.randint(0, w),
            "lane":  random.randint(0, num_lanes-1),
            "speed": random.uniform(speed_limit*0.3, speed_limit)
        })
    tab_view.set("Road Simulation")
    draw_road()
    move_cars()
    set_status(f"Simulating: {selected_road_name or 'Custom road'}...")

def stop_simulation():
    global simulation_running
    simulation_running = False
    set_status("Simulation stopped.")

def reset_all():
    global cars, simulation_running, sim_time
    global imported_data, city_graph, all_road_names
    global selected_road_edges, selected_road_name
    global selected_road_length_km
    simulation_running      = False
    sim_time                = 0
    cars.clear()
    flow_history.clear()
    time_history.clear()
    density_history.clear()
    speed_history.clear()
    imported_data           = None
    city_graph              = None
    all_road_names          = []
    selected_road_edges     = None
    selected_road_name      = ""
    selected_road_length_km = 0.0
    road_canvas.delete("all")
    avg_speed_label.configure(text="-- km/h")
    flow_label.configure(text="--")
    congestion_label.configure(text="--")
    jam_label.configure(text="-- km")
    data_status_label.configure(text="No data imported",
                                 text_color="#888")
    city_status_label.configure(text="Enter a city to begin",
                                 text_color="#888")
    road_status_label.configure(text="No road selected",
                                 text_color="#888")
    road_info_label.configure(
        text="No road selected — search a city and pick a road")
    road_dropdown.configure(values=["Load city first"],
                             state="disabled")
    road_var.set("Load city first")
    load_road_button.configure(state="disabled")
    speed_slider.set(60)
    density_slider.set(65)
    time_slider.set(30)
    update_speed(60)
    update_density(65)
    update_time(30)
    ax_map.clear()
    ax_map.set_title(
        "Select a road to see it highlighted on the map",
        color="#378ADD", fontsize=10)
    ax_map.axis("off")
    map_canvas_widget.draw()
    update_flow_chart()
    update_sd_chart()
    set_status("Reset complete — ready for new simulation.")

run_button.configure(command=run_simulation)
stop_button.configure(command=stop_simulation)
reset_button.configure(command=reset_all)

# ─── LAUNCH ───────────────────────────────────────────────
app.mainloop()