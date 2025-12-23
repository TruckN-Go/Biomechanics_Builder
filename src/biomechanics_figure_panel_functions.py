import os
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from src.ColorWheel import ColorWheel
wheel = ColorWheel()
from src.ChatCSV import butter_lowpass_filter, process_csv_from_chat

def sprint_acceleration(graph_color = wheel.powder_blue):

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

def pitching_mechanics(graph_color = wheel.bubblegum):
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


def remove_offset_from_early_window(df, pct=0.08):
    grf_col = "vertical_grf_N_per_kg"
    t0 = df["time_s"].min()
    t1 = t0 + pct * (df["time_s"].max() - t0)
    baseline = df.loc[df["time_s"] <= t1, grf_col].median()
    df[grf_col] = (df[grf_col] - baseline).clip(lower=0)
    return df

def jump_shot_initiation(graph_color = wheel.orange_creamsicle):

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