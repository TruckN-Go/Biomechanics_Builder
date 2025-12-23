import os
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from src.ColorWheel import ColorWheel
wheel = ColorWheel()
from src.ChatCSV import butter_lowpass_filter, process_csv_from_chat


graph_color = wheel.powder_blue

filename_sprint = os.path.join(os.getcwd(), "mock_data", "nfl_sprint_acceleration_biomechanics_temporal_dataset.csv")
df_temp = pd.read_csv(filename_sprint)

phase_force_threshold = 0.05  
df_temp["phase"] = np.where(
    df_temp["horizontal_grf_N_per_kg"] > phase_force_threshold,
    "stance",
    "flight"
)

df_temp["power_W_per_kg"] = df_temp["horizontal_grf_N_per_kg"] * df_temp["com_velocity_m_per_s"]

df_sprint = process_csv_from_chat(df_temp, filter = False)
df_sprint_stance = process_csv_from_chat(df_temp[df_temp.phase == 'stance'].reset_index(drop=True), filter=False)
df_sprint_flight = process_csv_from_chat(df_temp[df_temp.phase == 'flight'].reset_index(drop=True), filter=False)

sprinting_phases = ["0_10", "10_25", "25_40", "40_55", "55_70", "70_100"]
icon_dict = dict()
for phases in sprinting_phases:
    icon_dict[phases] = wheel.recolor_icons(os.path.join(os.getcwd(),'icons', 'sprinting_phase_' + phases + '.png'), graph_color)


df_plot = df_sprint
plt.style.use('dark_background')
mosaic_matrix = [['title','.'],
                 ['hip_flexion_deg','horizontal_grf_N_per_kg'],
                 ['knee_flexion_deg','com_velocity_m_per_s'],
                 ['ankle_dorsiflexion_deg','power_W_per_kg'],
                 ['sprinting_phases_1', 'sprinting_phases_2'],
                 ]
fig, ax = plt.subplot_mosaic(mosaic_matrix, figsize=(10, 10), layout='constrained', height_ratios=[0.15,1,1,1,0.25])

lw = 3
sd_alpha = 0.25
sd_times = 1
fs=12
shading_alpha = 0.25
annotation_color = wheel.light_grey
title_y_pos = 0.85
fs_title = fs+5
linespacing = 0.9
fs_mini = -1

ax['title'].set_axis_off()

fig.text(.25,1, "Temporal Coordination of Lower-Body\nJoints during Sprint Acceleration", ha='center', va='center', 
         fontsize=fs_title, weight='bold', linespacing=0.9, color=annotation_color)


fig.text(.75,1, "Force Application &\nVelocity Development\nduring Early Sprint Acceleration", ha='center', va='center', 
         fontsize=fs_title, weight='bold', linespacing=1, color=annotation_color)


for angle_param in ['hip_flexion_deg','knee_flexion_deg','ankle_dorsiflexion_deg','horizontal_grf_N_per_kg','com_velocity_m_per_s','power_W_per_kg']:
    ax[angle_param].plot(df_plot.time_s, df_plot[angle_param+'_mean'], 
                         lw=lw, c=graph_color)
    ax[angle_param].fill_between(df_plot.time_s,
                                 df_plot[angle_param+'_mean']+sd_times*df_plot[angle_param+'_sd'],
                                 df_plot[angle_param+'_mean']-sd_times*df_plot[angle_param+'_sd'], 
                                 alpha=sd_alpha, color=graph_color, edgecolor=None)
    

    ax[angle_param].set_xlim(df_plot.time_s.min(), df_plot.time_s.max())
    ax[angle_param].tick_params(axis='both', labelsize=fs, width=2, length=3.5)
    ax[angle_param].set_yticks(ax[angle_param].get_yticks().astype(int),ax[angle_param].get_yticks().astype(int), weight='bold')
    ax[angle_param].set_xticks([],[], weight='bold')
    ax[angle_param].spines['right'].set_visible(False)
    ax[angle_param].spines['top'].set_visible(False)
    ax[angle_param].spines['bottom'].set_visible(False)
    for axis in ['left']:
        ax[angle_param].spines[axis].set_linewidth(1.75) 


x0 = [-.05, 0.07, 0.2, 0.35, 0.55, 0.8]
y0 = 0
width = .2
height = 1
x_tick_labels = np.linspace(df_plot.time_s.min(), df_plot.time_s.max(), 5)
for sprint_ax in ['sprinting_phases_1', 'sprinting_phases_2']:
    ax[sprint_ax].spines['left'].set_visible(False)
    ax[sprint_ax].tick_params(axis='both', labelsize=fs, width=2, length=3.5)
    ax[sprint_ax].set_yticks([], [])
    ax[sprint_ax].set_xticks(x_tick_labels, x_tick_labels, weight='bold')
    ax[sprint_ax].spines['right'].set_visible(False)
    ax[sprint_ax].spines['top'].set_visible(False) 
    ax[sprint_ax].spines['bottom'].set_linewidth(1.75) 
    ax[sprint_ax].set_xlabel('Time (seconds)', weight='bold', fontsize=fs, labelpad=1)
        

    for phases_i, phases in enumerate(icon_dict.keys()):
        ax_sprinting_icons = ax[sprint_ax].inset_axes([x0[phases_i], y0, width, height])
        ax_sprinting_icons.imshow(icon_dict[phases])
        ax_sprinting_icons.set_axis_off()


ax['hip_flexion_deg'].set_title("Hip Flexion Angle", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['hip_flexion_deg'].set_ylabel(r"Hip Flexion Angle ($\mathbf{\theta}$)", weight='bold', fontsize=fs)

ax['knee_flexion_deg'].set_title("Knee Flexion Angle", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['knee_flexion_deg'].set_ylabel(r"Knee Flexion Angle ($\mathbf{\theta}$)", weight='bold', fontsize=fs)

ax['ankle_dorsiflexion_deg'].set_title("Ankle Dorsiflexion Angle", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['ankle_dorsiflexion_deg'].set_ylabel(r"Ankle Dorsiflexion Angle ($\mathbf{\theta}$)", weight='bold', fontsize=fs)

    
ax['horizontal_grf_N_per_kg'].set_title("Horizontal Ground\nReaction Force", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['horizontal_grf_N_per_kg'].set_ylabel("Horizontal Ground\nReaction Force (N/kg)", weight='bold', fontsize=fs)

ax['com_velocity_m_per_s'].set_title("Center-of-Mass Velocity", weight='bold', fontsize=fs_title, c=graph_color)
ax['com_velocity_m_per_s'].set_ylabel("Velocity (m/s)", weight='bold', fontsize=fs)


ax['power_W_per_kg'].set_title("Horizontal Power", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['power_W_per_kg'].set_ylabel("Power (W/kg)", weight='bold', fontsize=fs)


scale_annotation_loc = df_plot.time_s.max()/100
ax['com_velocity_m_per_s'].text(scale_annotation_loc*(10+25)/2,7,'Early\nDrive', rotation=90, color=annotation_color, 
                                fontsize=fs-fs_mini, weight='bold', linespacing=linespacing, ha='center', va='center')

ax['com_velocity_m_per_s'].axvspan(xmin=scale_annotation_loc*25, xmax=scale_annotation_loc*40, facecolor=wheel.light_grey, alpha=shading_alpha, zorder=0)
ax['com_velocity_m_per_s'].text(scale_annotation_loc*(25+40)/2,1.5,'Peak\nAcceleration', rotation=90, color=annotation_color, 
                                fontsize=fs-fs_mini, weight='bold', linespacing=linespacing, ha='center', va='center')

ax['com_velocity_m_per_s'].axvspan(xmin=scale_annotation_loc*55, xmax=scale_annotation_loc*70, facecolor=wheel.light_grey, alpha=shading_alpha, zorder=0)
ax['com_velocity_m_per_s'].text(scale_annotation_loc*(55+70)/2,2,'Transition into\nUpright Sprint', rotation=90, color=annotation_color, 
                                fontsize=fs-fs_mini, weight='bold', linespacing=linespacing, ha='center', va='center')


figw, figh = fig.get_size_inches()
fig.canvas.draw()
fig.set_layout_engine('none')

dx, dy = 0, 0.2
dw, dh = 0, 0 

for shift_ax_up in ['sprinting_phases_1','sprinting_phases_2']:
    bbox = ax[shift_ax_up].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    w, h = bbox.width, bbox.height
    x, y = bbox.x0,bbox.y0
    ax[shift_ax_up].set_position(((x+dx)/figw, (y+dy)/figh, (w+dw)/figw, (h+dh)/figh))

fig.savefig(os.path.join('figures','Sprint_Acceleration_Biomechanics.png'))
plt.show()