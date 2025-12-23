# %%
import os
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from src.ColorWheel import ColorWheel
wheel = ColorWheel()
from src.ChatCSV import butter_lowpass_filter, process_csv_from_chat

def remove_offset_from_early_window(df, pct=0.08):
    grf_col = "vertical_grf_N_per_kg"
    t0 = df["time_s"].min()
    t1 = t0 + pct * (df["time_s"].max() - t0)
    baseline = df.loc[df["time_s"] <= t1, grf_col].median()
    df[grf_col] = (df[grf_col] - baseline).clip(lower=0)
    return df

graph_color = wheel.orange_creamsicle

jump_shot_phases = ['flight','loading','propulsion']
icon_dict = dict()
for phases in jump_shot_phases:
    icon_dict[phases] = wheel.recolor_icons(os.path.join(os.getcwd(),'icons', 'jump_shot_' + phases + '.png'), graph_color)

filename_basketball_jump = os.path.join(os.getcwd(), "mock_data", "basketball_jump_shot_biomechanics_temporal_dataset.csv")

df_jump_temp = pd.read_csv(filename_basketball_jump)
df_jump_temp = df_jump_temp.groupby(["athlete_id", "trial_id"], group_keys=False).apply(remove_offset_from_early_window)


df_jump_temp["power_W_per_kg"] = df_jump_temp["vertical_grf_N_per_kg"] * df_jump_temp["com_velocity_m_per_s"]
df_jump = process_csv_from_chat(df_jump_temp)
df_plot = df_jump


plt.style.use('dark_background')
mosaic_matrix = [['title','.'],
                 ['elbow_angle_deg','vertical_grf_N_per_kg'],
                 ['hip_angle_deg','com_velocity_m_per_s'],
                 ['knee_angle_deg','power_W_per_kg'],
                 ['jump_shot_phases_1', 'jump_shot_phases_2'],
                 ]
fig, ax = plt.subplot_mosaic(mosaic_matrix, figsize=(10, 10), layout='constrained', height_ratios=[0.15,1,1,1,0.25])

lw = 3
sd_alpha = 0.25
sd_times = 1
fs=12
shading_alpha = 0.25
annotation_color = wheel.light_grey
title_y_pos = 0.9
fs_title = fs+5
linespacing = 1
fs_mini = -1

ax['title'].set_axis_off()

fig.text(.25,1, "Temporal Coordination of Joint\nAngles during Jump Shot", ha='center', va='center', 
         fontsize=fs_title, weight='bold', linespacing=0.9, color=annotation_color)


fig.text(.75,1, "Vertical Force Production & Velocity\nduring Jump Shot Execution", ha='center', va='center', 
         fontsize=fs_title, weight='bold', linespacing=1, color=annotation_color)


for angle_param in ['elbow_angle_deg','hip_angle_deg','knee_angle_deg','vertical_grf_N_per_kg','com_velocity_m_per_s', 'power_W_per_kg']:
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

x0 = [-0.1, 0.125, .35] 
y0 = -0.2
width = .5
height = 2.5
x_tick_labels = np.linspace(df_plot.time_s.min(), df_plot.time_s.max(), 3)
for sprint_ax in ['jump_shot_phases_1', 'jump_shot_phases_2']:
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


ax['elbow_angle_deg'].set_title("Elbow Angle", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['elbow_angle_deg'].set_ylabel(r"Elbow Angle ($\mathbf{\theta}$)", weight='bold', fontsize=fs)

ax['hip_angle_deg'].set_title("Hip Angle", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['hip_angle_deg'].set_ylabel(r"Hip Angle ($\mathbf{\theta}$)", weight='bold', fontsize=fs)

ax['knee_angle_deg'].set_title("Knee Angle", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['knee_angle_deg'].set_ylabel(r"Knee Angle ($\mathbf{\theta}$)", weight='bold', fontsize=fs)

    
ax['vertical_grf_N_per_kg'].set_title("Vertical Ground\nReaction Force", weight='bold', fontsize=fs_title, c=graph_color)
ax['vertical_grf_N_per_kg'].set_ylabel("Vertical Ground\nReaction Force (N/kg)", weight='bold', fontsize=fs)

ax['com_velocity_m_per_s'].set_title("Center-of-Mass Velocity", weight='bold', fontsize=fs_title, c=graph_color, y=title_y_pos)
ax['com_velocity_m_per_s'].set_ylabel("Velocity (m/s)", weight='bold', fontsize=fs)

ax['power_W_per_kg'].set_title("Vertical Power", weight='bold', fontsize=fs_title, c=graph_color)
ax['power_W_per_kg'].set_ylabel("Power (W/kg)", weight='bold', fontsize=fs)


scale_annotation_loc = df_plot.time_s.max()/100
ax['power_W_per_kg'].axvspan(xmin=scale_annotation_loc*45, xmax=scale_annotation_loc*70, facecolor=wheel.light_grey, alpha=shading_alpha, zorder=0)
ax['power_W_per_kg'].text(scale_annotation_loc*(45+70)/2,0.5,'Propulsion\nPhase', rotation=90, color=annotation_color, 
                                fontsize=fs-fs_mini, weight='bold', linespacing=linespacing, ha='center', va='center')



figw, figh = fig.get_size_inches()
fig.canvas.draw()
fig.set_layout_engine('none')

dx, dy = 0, 0.165
dw, dh = 0, 0 

for shift_ax_up in ['jump_shot_phases_1','jump_shot_phases_2']:
    bbox = ax[shift_ax_up].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    w, h = bbox.width, bbox.height
    x, y = bbox.x0,bbox.y0
    ax[shift_ax_up].set_position(((x+dx)/figw, (y+dy)/figh, (w+dw)/figw, (h+dh)/figh))


fig.savefig(os.path.join('figures','Jump_Shot_Initiation_Biomechanics.png'))
plt.show()