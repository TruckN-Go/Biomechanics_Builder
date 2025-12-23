
import pandas as pd
from scipy.signal import butter, filtfilt

def butter_lowpass_filter(data, fs, cutoff, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)


def process_csv_from_chat(df_time_series, filter=True):
    # mock data
    df = df_time_series

    fs = 1/df.time_s.diff()[1]
    cutoff_joint_angles = 8 #Hz

    no_math_cols = ['trial_id', 'time_s'] + df_time_series.select_dtypes(include=['object', 'string']).columns.tolist()
    do_math_cols = df.columns.drop(no_math_cols).tolist()

    if filter == True:
        df[do_math_cols] = df_time_series[do_math_cols].apply(butter_lowpass_filter, args=[fs, cutoff_joint_angles])

    # calculate means for trials within an athlete
    df_temporal_mean = df.groupby(['athlete_id','time_s'])[do_math_cols].mean().reset_index()

    # between athlete variabilty 
    df_mean_between_athletes = df_temporal_mean.groupby(['time_s'])[do_math_cols].mean().reset_index()
    df_sd_between_athletes = df_temporal_mean.groupby(['time_s'])[do_math_cols].std().reset_index()

    df_between_athletes = pd.merge(df_mean_between_athletes, df_sd_between_athletes, on=['time_s'], how='inner',suffixes=["_mean", "_sd"])

    return df_between_athletes