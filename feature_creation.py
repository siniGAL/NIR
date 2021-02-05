import numpy as np
import statistics


def feature_creation(times):
    if len(times) > 2:
        iat_min = np.amin(times)
        iat_max = np.amax(times)
        iat_mean = statistics.mean(times)
        iat_std = statistics.stdev(times)
        features = np.array([iat_mean, iat_std, iat_max, iat_min])
    else:
        features = np.zeros((4,), dtype=int)
    return features
