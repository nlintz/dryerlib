from accel import Accelerometer
from dsp import *

class Dryer(object):
    def __init__(self):
        self.accelerometer = Accelerometer()
        self.accelerometer.initialize()

        self.previous_readings = []

    def collect_sample(self):
        x = self.accelerometer.read_accel('x')
        y = self.accelerometer.read_accel('y')
        z = self.accelerometer.read_accel('z')
	return {'x': x, 'y': y, 'z': z}
        self.previous_readings.append({'x': x, 'y': y, 'z': z})

    def get_lastn_readings(self, n):
        return self.previous_readings[-n:]

    def get_lastn_norm_integral(self, n):
        lastn_norms = preprocess_norm(df_to_mat(self.get_lastn_readings(n)))
        return np.mean(lastn_norms)
