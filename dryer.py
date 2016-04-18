from accel import Accelerometer
import dsp
import time


class Dryer(object):
    def __init__(self):
        self.accelerometer = Accelerometer()
        self.accelerometer.initialize()

    def collect_sample(self):
        x = self.accelerometer.read_accel('x')
        y = self.accelerometer.read_accel('y')
        z = self.accelerometer.read_accel('z')
        t = time.time()

        return {"x": x, "y": y, "z": z, "time": t}

    def get_readings(self, num_samples):
        readings = []
        for i in range(num_samples):
            readings.append(self.collect_sample())
        return dsp.df_to_mat(readings), dsp.df_times(readings)
