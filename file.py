import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skyfield.api import load, Topos


planets = load('de421.bsp')
earth = planets['earth']


bodies = {
    "Sun": planets["sun"],
    "Moon": planets["moon"],
    "Mercury": planets["mercury"],
    "Venus": planets["venus"],
    "Mars": planets["mars"],
    "Jupiter": planets["jupiter barycenter"],
    "Saturn": planets["saturn barycenter"],
    "Uranus": planets["uranus barycenter"],
    "Neptune": planets["neptune barycenter"],
    "Pluto": planets["pluto barycenter"],
}


ts = load.timescale()
observer = earth + Topos('51.5074 N', '0.1278 W')


minutes = int(input("How many minutes do you want to log data? "))
interval = int(input("How often (in seconds) do you want to take a measurement? "))


with open("Star_tracking.csv", "a", newline="") as file:
    writer = csv.writer(file)

    
    if file.tell() == 0:
        writer.writerow(["Time", "Body", "RA", "Dec", "Distance_AU", "Altitude_deg", "Azimuth_deg"])

 
    end_time = time.time() + minutes * 60

    while time.time() < end_time:
        t = ts.now()  

        for name, body in bodies.items():
            
            ra, dec, distance = earth.at(t).observe(body).apparent().radec()
           
            alt, az, dist_altaz = observer.at(t).observe(body).apparent().altaz()

            
            print(f"{name}: RA={ra}, Dec={dec}, Dist={distance.au:.2f} AU, "
                  f"Alt={alt.degrees:.2f}°, Az={az.degrees:.2f}°")

            
            writer.writerow([
                t.utc_strftime('%Y-%m-%d %H:%M:%S'),
                name,
                ra, dec,
                distance.au,
                alt.degrees,
                az.degrees
            ])

        file.flush()   
        time.sleep(interval)

print("Logging complete!")

#  Visualise Planetary motion over time 
df = pd.read_csv("Star_tracking.csv")
df["Time"] = pd.to_datetime(df["Time"])
planets_to_plot = ["Sun" , "Moon" , "Mercury" , "Venus", "Mars"]
subset = df[df["Body"].isin(planets_to_plot)]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6), sharex = True)
for planet in planets_to_plot: 
 planet_df = subset[subset["Body"] == planet]
 ax1.plot(planet_df["Time"], planet_df["Altitude_deg"], label=planet)
ax1.set_xlabel("Time")

ax1.set_ylabel("Altitude (deg)")
ax1.set_title("Planet Altitude Over Time")
ax1.legend()

for planet in planets_to_plot:
    planet_df = subset[subset["Body"] == planet]
    ax2.plot(planet_df["Time"], planet_df["Azimuth_deg"], label=planet)
ax2.set_title("Azimuth Over Time")
ax2.set_xlabel("Time")
ax2.set_ylabel("Azimuth (deg)")
ax2.legend()
plt.tight_layout()
plt.show()



