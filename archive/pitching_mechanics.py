# %%
import os
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from src.ColorWheel import ColorWheel
wheel = ColorWheel()
from src.ChatCSV import butter_lowpass_filter, process_csv_from_chat



graph_color = wheel.bubblegum

filename_pitch = os.path.join(os.getcwd(), "mock_data", "mlb_pitching_biomechanics_temporal_dataset.csv")
df_temp = pd.read_csv(filename_pitch)
df_temp['trunk_hip_separation'] = df_temp['trunk_rotation_deg'] - df_temp['hip_rotation_deg']
df_pitch = process_csv_from_chat(df_temp, filter = False)


pitching_phases = ["0", "1", "2", "3", "4"]
icon_dict = dict()
for phases in pitching_phases:
    icon_dict[phases] = wheel.recolor_icons(os.path.join(os.getcwd(),'icons', 'pitching_phase_' + phases + '.png'), graph_color)

df_plot = df_pitch

plt.style.use('dark_background')
mosaic_matrix = [['title','.'],
                 ['shoulder_external_rotation_deg','elbow_varus_torque_Nm'],
                 ['elbow_flexion_deg','trunk_hip_separation'],
                 ['trunk_rotation_deg','lead_knee_flexion_deg'],
                 ['pitching_phases_1', 'pitching_phases_2'],
                 ]
fig, ax = plt.subplot_mosaic(mosaic_matrix, figsize=(10, 10), layout='constrained', height_ratios=[0.15,1,1,1,0.25])

lw = 3
sd_alpha = 0.25
sd_times = 1
fs=12
shading_alpha = 0.25
annotation_color = wheel.light_grey
title_y_pos = 0.95
fs_title = fs+5
linespacing = 1.5
fs_mini = -1

ax['title'].set_axis_off()

fig.text(.25,1, "Temporal Joint Kinematics\n during a Ball Pitch", ha='center', va='center', 
         fontsize=fs_title, weight='bold', linespacing=0.9, color=annotation_color)


fig.text(.75,1, "Mechanical Loading Metrics\nRelevant to Injury Risk\nduring Pitching", ha='center', va='center', 
         fontsize=fs_title, weight='bold', linespacing=1, color=annotation_color)


for angle_param in ['shoulder_external_rotation_deg','elbow_flexion_deg','trunk_rotation_deg','elbow_varus_torque_Nm','trunk_hip_separation', 'lead_knee_flexion_deg']:
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

x0 = [-0.15, 0.0, .2, 0.45, 0.7] 
y0 = -0.3
width = .4
height = 2
x_tick_labels = np.linspace(df_plot.time_s.min(), df_plot.time_s.max(), 5)
for pitch_ax in ['pitching_phases_1', 'pitching_phases_2']:
    ax[pitch_ax].spines['left'].set_visible(False)
    ax[pitch_ax].tick_params(axis='both', labelsize=fs, width=2, length=3.5)
    ax[pitch_ax].set_yticks([], [])
    ax[pitch_ax].set_xticks(x_tick_labels, x_tick_labels, weight='bold')
    ax[pitch_ax].spines['right'].set_visible(False)
    ax[pitch_ax].spines['top'].set_visible(False) 
    ax[pitch_ax].spines['bottom'].set_linewidth(1.75) 
    ax[pitch_ax].set_xlabel('Time (seconds)', weight='bold', fontsize=fs, labelpad=1)
        

    for phases_i, phases in enumerate(icon_dict.keys()):
        ax_pitching_icons = ax[pitch_ax].inset_axes([x0[phases_i], y0, width, height])
        ax_pitching_icons.imshow(icon_dict[phases])
        ax_pitching_icons.set_axis_off()
        

ax['shoulder_external_rotation_deg'].set_title("Shoulder External\nRotation Angle", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['shoulder_external_rotation_deg'].set_ylabel("Shoulder External\nRotation Angle " + r"($\mathbf{\theta}$)", weight='bold', fontsize=fs)

ax['elbow_flexion_deg'].set_title("Elbow Flexion Angle", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['elbow_flexion_deg'].set_ylabel(r"Elbow Flexion Angle ($\mathbf{\theta}$)", weight='bold', fontsize=fs)

ax['trunk_rotation_deg'].set_title("Trunk Rotation Angle", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['trunk_rotation_deg'].set_ylabel(r"Trunk Rotation Angle ($\mathbf{\theta}$)", weight='bold', fontsize=fs)

ax['elbow_varus_torque_Nm'].set_title("Elbow Varus Torque", weight='bold', fontsize=fs_title, c=graph_color)
ax['elbow_varus_torque_Nm'].set_ylabel("Elbow Varus Torque (Nm)", weight='bold', fontsize=fs)

ax['trunk_hip_separation'].set_title("Trunk-Hip Rotation\nAngle Separation", weight='bold', fontsize=fs_title, c=graph_color)
ax['trunk_hip_separation'].set_ylabel("Trunk-Hip Rotation\nAngle Separation" + r"($\mathbf{\theta}$)", weight='bold', fontsize=fs)

ax['lead_knee_flexion_deg'].set_title("Lead Knee Flexsion", weight='bold', fontsize=fs_title, c=graph_color)
ax['lead_knee_flexion_deg'].set_ylabel(r"Lead Knee Flexion ($\mathbf{\theta}$)", weight='bold', fontsize=fs)


scale_annotation_loc = df_plot.time_s.max()/100
ax['elbow_varus_torque_Nm'].axvspan(xmin=scale_annotation_loc*55, xmax=scale_annotation_loc*75, facecolor=wheel.light_grey, alpha=shading_alpha, zorder=0)
ax['elbow_varus_torque_Nm'].text(scale_annotation_loc*(55+75)/2,35,'Peak Elbow\nLoading', rotation=90, color=annotation_color, 
                                fontsize=fs-fs_mini, weight='bold', linespacing=linespacing, ha='center', va='center')

ax['trunk_hip_separation'].axvspan(xmin=scale_annotation_loc*40, xmax=scale_annotation_loc*60, facecolor=wheel.light_grey, alpha=shading_alpha, zorder=0)
ax['trunk_hip_separation'].text(scale_annotation_loc*(40+60)/2,-20,'Kinetic Chain\nMax Separation', rotation=0, color=annotation_color, 
                                fontsize=fs-fs_mini, weight='bold', linespacing=linespacing, ha='center', va='center')
# too little separation == arm overload
# too much separation == lumbar stress

ax['lead_knee_flexion_deg'].axvspan(xmin=scale_annotation_loc*60, xmax=scale_annotation_loc*80, facecolor=wheel.light_grey, alpha=shading_alpha, zorder=0)
ax['lead_knee_flexion_deg'].text(scale_annotation_loc*(60+80)/2,160,'Lead Leg\nEnergy\nTransfer', rotation=90, color=annotation_color, 
                                fontsize=fs-fs_mini, weight='bold', linespacing=linespacing, ha='center', va='center')


figw, figh = fig.get_size_inches()
fig.canvas.draw()
fig.set_layout_engine('none')

dx, dy = 0, 0.15
dw, dh = 0, 0 

for shift_ax_up in ['pitching_phases_1','pitching_phases_2']:
    bbox = ax[shift_ax_up].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    w, h = bbox.width, bbox.height
    x, y = bbox.x0,bbox.y0
    ax[shift_ax_up].set_position(((x+dx)/figw, (y+dy)/figh, (w+dw)/figw, (h+dh)/figh))


fig.savefig(os.path.join('figures','Pitching_Biomechanics.png'))
plt.show()