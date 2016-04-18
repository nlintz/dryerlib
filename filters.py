import numpy as np
from scipy import stats
import numpy as np
from scipy.signal import butter, lfilter


def bandpass_filter_signal(data, lpf_cutoff, hpf_cutoff, fs):
    filtered = butter_pass_filter(data, lpf_cutoff, fs, 6)
    filtered2 = butter_pass_filter(filtered, hpf_cutoff, fs, 6, btype='high')
    return filtered2


def butter_filter(cutoff, fs, btype, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    return b, a


def butter_pass_filter(data, cutoff, fs, order=5, btype='low'):
    b, a = butter_filter(cutoff, fs, btype, order=order)
    y = lfilter(b, a, data)
    return y