from scipy.signal import butter, lfilter


def butter_lowpass_filter(rate, data, freqHighCutoff, order=5):
    """Butterworth low pass filter"""
    nyq = 0.5 * rate
    normal_cutoff = freqHighCutoff / nyq
    b, a = butter(order, normal_cutoff, analog=False, btype='low')
    y = lfilter(b, a, data)
    return y


def butter_highpass_filter(rate, data, freqLowCutoff, order=5):
    """Butterworth high pass filter"""
    nyq = 0.5 * rate
    normal_cutoff = freqLowCutoff / nyq
    b, a = butter(order, normal_cutoff, analog=False, btype='high')
    y = lfilter(b, a, data)
    return y


def butter_bandpass_filter(rate, data, freqLowCutoff, freqHighCutoff, order=5):
    """Butterworth band pass filter"""
    nyq = 0.5 * rate
    low = freqLowCutoff / nyq
    high = freqHighCutoff / nyq
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y