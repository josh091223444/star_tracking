import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import CheckButtons, Button
from astropy.coordinates import Angle
import re

planets_to_plot = ["Sun", "Moon", "Mercury", "Venus", "Mars"]
active_planets = set(planets_to_plot)

# --- Setup plots ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 6))
plt.subplots_adjust(left=0.2)

# --- Widgets ---
checkbox_ax = plt.axes([0.05, 0.4, 0.1, 0.3])
button_ax = plt.axes([0.05, 0.2, 0.1, 0.1])
checkbox = CheckButtons(checkbox_ax, planets_to_plot, [True]*len(planets_to_plot))
button = Button(button_ax, "Pause/Resume")

paused = False

def toggle_planet(label):
    """Add or remove planets dynamically."""
    global active_planets
    if label in active_planets:
        active_planets.remove(label)
    else:
        active_planets.add(label)
    print(f"Active planets: {active_planets}")

def toggle_pause(event):
    """Pause or resume live updates."""
    global paused
    paused = not paused
    print(f"Paused: {paused}")

checkbox.on_clicked(toggle_planet)
button.on_clicked(toggle_pause)

# --- Helper to convert RA/Dec strings ---

def parse_angle(val, kind='ra'):
    if not isinstance(val, str):
        return None
    try:
        val = val.strip().replace('""', '"')  # remove extra double-quote

        if kind == 'ra':
            # "15h 19m 00.64s" → "15h19m00.64s"
            val = val.replace(" ", "")
            #return Angle(val, unit='hourangle').hours
            return Angle(val).hour

        else:  # DEC
            # "-20deg 54' 30.7""" → "-20d54m30.7s"
            val = (
                val.replace("deg", "d")
                   .replace("'", "m")
                   .replace('"', "s")
                   .replace(" ", "")
            )
            #return Angle(val, unit='degree').degrees
            return Angle(val).degree 

    except Exception as e:
        print(f"⚠️ Could not parse: {val} → {e}")
        return None


# --- Animation update function ---
def update(frame):
    global paused
    if paused:
        return

    if not os.path.exists("Star_tracking.csv"):
        print("⏳ Waiting for Star_tracking.csv... (Run file.py first)")
        return

    df = pd.read_csv("Star_tracking.csv")
    df["Time"] = pd.to_datetime(df["Time"])

    # ✅ Parse RA/Dec properly using Skyfield’s Angle
    df["RA"] = df["RA"].apply(lambda x: parse_angle(x, 'ra'))
    df["Dec"] = df["Dec"].apply(lambda x: parse_angle(x, 'dec'))

    # Filter only selected planets
    subset = df[df["Body"].isin(active_planets)]

    # Clear plots
    ax1.clear()
    ax2.clear()
    ax3.clear()

    for planet in active_planets:
        planet_df = subset[subset["Body"] == planet].dropna(subset =["RA", "Dec"])
        ax1.plot(planet_df["Time"], planet_df["Altitude_deg"], label=planet)
        ax2.plot(planet_df["Time"], planet_df["Azimuth_deg"], label=planet)
        ax3.plot(planet_df["RA"], planet_df["Dec"], label=planet, marker='o')
       # ax3.scatter(planet_df["RA"], planet_df["Dec"], label=planet, s=40)

# 🪄 Set tighter axis limits for the sky map
    if not subset["RA"].isnull().all() and not subset["Dec"].isnull().all():
        ax3.set_xlim(subset["RA"].min() - 1, subset["RA"].max() + 1)
        ax3.set_ylim(subset["Dec"].min() - 5, subset["Dec"].max() + 5)

        # Titles and labels
        ax1.set_title("Altitude Over Time")
        ax2.set_title("Azimuth Over Time")
        ax3.set_title("RA vs Dec (Sky Map)")
        ax3.set_xlabel("Right Ascension (hours)")
        ax3.set_ylabel("Declination (degrees)")
        ax3.set_aspect("equal", adjustable="box")
        ax3.invert_xaxis()

    # 🌌 Sky map styling
    ax3.set_facecolor("black")
    ax3.grid(True, color="white", alpha=0.2)
    ax3.tick_params(colors="white")
    for spine in ax3.spines.values():
        spine.set_color("white")

    # ✅ Common grid and legend
    for ax in [ax1, ax2, ax3]:
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)
# --- Run live animation ---
ani = animation.FuncAnimation(fig, update, interval=5000, cache_frame_data=False)
plt.show()
