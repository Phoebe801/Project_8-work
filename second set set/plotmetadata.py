import os,json
import matplotlib.pyplot as plt
import numpy as np

shortTracks = 1.e-6 # cut for short tracks
rootdir = 'results/'
avg_frequency = []
start_radius = []
electron_energy = []
track_length = []
first_track_length = []
start_time = []
ntracks = []


for root, dirs, files in os.walk(rootdir):
    for name in files:
        full_path = os.path.join(root, name)
        if (name.endswith(("LocustEventProperties.json")) and (os.path.getsize(full_path)) > 0):
            with open(full_path) as json_file:
                data = json.load(json_file)
                for ievent in range(data["nevents"]):
                    ntracks.append(data[str(ievent)]["ntracks"])
                    for itrack in range(data[str(ievent)]["ntracks"]):
                        if ((data[str(ievent)][str(itrack)]["end-time"] - data[str(ievent)][str(itrack)]["start-time"]) > shortTracks):  # Select stably-trapped electrons:                            
                            avg_frequency.append(data[str(ievent)][str(itrack)]["output-avg-frequency"])
                            start_radius.append(data[str(ievent)][str(itrack)]["start-radius"])
                            electron_energy.append(data[str(ievent)][str(itrack)]["energy-ev"])
                            track_length.append(data[str(ievent)][str(itrack)]["end-time"] - data[str(ievent)][str(itrack)]["start-time"])
                            if (itrack == 0):
                                first_track_length.append(data[str(ievent)][str(itrack)]["end-time"] - data[str(ievent)][str(itrack)]["start-time"])
                                start_time.append(data[str(ievent)][str(itrack)]["start-time"])

fig, axes = plt.subplots(2,2, figsize=(10,8))
axes[0,0].scatter(start_time, first_track_length)
axes[0,0].set_xlabel("first track start time (s)")
axes[0,0].set_ylabel("first track length (s)")
axes[1,0].scatter(electron_energy, avg_frequency)
axes[1,0].set_xlabel("e- energy (eV)")
axes[1,0].set_ylabel("avg output carrier frequency (Hz)")
axes[0,1].hist(ntracks, bins=np.arange(0, 20 + 1.0, 1.0))
axes[0,1].set_xlabel("n tracks per event")
axes[0,1].set_ylabel("counts")
axes[1,1].hist(track_length, bins=np.arange(0, 0.005, 0.0005))
axes[1,1].set_xlabel("track length")
axes[1,1].set_ylabel("counts")
plt.show()

