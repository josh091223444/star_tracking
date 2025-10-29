import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Planets to track
planets_to_plot = ["Sun", "Moon", "Mercury", "Venus", "Mars"]

# Set up two side-by-side subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharex=True)

def update(frame):
    """Re-runs every few seconds to refresh the plot."""
    try:
        # Read the latest data
        df = pd.read_csv("Star_tracking.csv")
        df["Time"] = pd.to_datetime(df["Time"])

        # Filter only selected planets
        subset = df[df["Body"].isin(planets_to_plot)]

        # Clear old plots
        ax1.clear()
        ax2.clear()

        # Plot altitude and azimuth
        for planet in planets_to_plot:
            planet_df = subset[subset["Body"] == planet]
            ax1.plot(planet_df["Time"], planet_df["Altitude_deg"], label=planet)
            ax2.plot(planet_df["Time"], planet_df["Azimuth_deg"], label=planet)

        # Format plots
        ax1.set_title("Planet Altitude Over Time")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Altitude (deg)")
        ax1.legend(loc="upper right")

        ax2.set_title("Azimuth Over Time")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Azimuth (deg)")
        ax2.legend(loc="upper right")

        plt.tight_layout()

    except Exception as e:
        print(f"⚠️ Error during update: {e}")

# Create the live animation
ani = animation.FuncAnimation(
    fig,
    update,
    interval=5000,              # refresh every 5 seconds
    cache_frame_data=False,     # prevent caching buildup
    repeat=False,               # don’t restart when done
    blit=False                  # make it compatible with window resize
)

plt.show()
