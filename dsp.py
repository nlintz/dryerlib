import numpy as np

def df_to_mat(data):
    x = [d['x'] for d in data]
    y = [d['y'] for d in data]
    z = [d['z'] for d in data]
    x = np.array(x).astype("float32")
    y = np.array(y).astype("float32")
    z = np.array(z).astype("float32")
    return np.c_[x, y, z]


def compute_norm(data_mat):
    return ((data_mat**2).sum(axis=1))**0.5


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def preprocess_norm(data_mat):
    norm = compute_norm(data_mat)
    norm = norm - norm.mean()
    norm_lpf = moving_average(norm, n=3)
    return norm_lpf

