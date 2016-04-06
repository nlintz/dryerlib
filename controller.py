import dryer
import time
import dsp
# import numpy as np


class Controller(object):
    def __init__(self, off_sleep_duration=2, on_sleep_duration=1,
                 initial_state="off", on_threshold=0.1, num_samples=100,
                 mavg_samples=10):
        self.dryer = dryer.Dryer()
        self.state_machine = {"on":self._on_state,
                              "off":self._off_state,
                              "alert":self._alert_state}
        self.off_sleep_duration = off_sleep_duration
        self.on_sleep_duration = on_sleep_duration
        self.state = initial_state
        self.on_threshold = on_threshold
        self.num_samples = num_samples
        self.mavg_samples = mavg_samples

    def compute_norm_sum(self):
	try:
            samples = self.dryer.get_readings(self.mavg_samples+self.num_samples)
	except:
	    pass
        norm = dsp.compute_norm(samples)
        norm_lpf = dsp.moving_average(norm, n=self.mavg_samples)
        norm_lpf_slice = norm_lpf[self.mavg_samples:self.mavg_samples+self.num_samples]
        norm_sum = norm_lpf_slice.sum()
        # norm_sum = np.random.randn()
        return norm_sum


    def _on_state(self):
        norm_sum = self.compute_norm_sum()
        #print norm_sum
        if norm_sum < self.on_threshold:
            self.state = "alert"
        time.sleep(self.on_sleep_duration)

    def _alert_state(self):
        print "tweet!"
        self.state = "off"

    def _off_state(self):
        norm_sum = self.compute_norm_sum()
        #print norm_sum
        if norm_sum > self.on_threshold:
            self.state = "on"

        time.sleep(self.on_sleep_duration)

    def run(self):
        while True:
            print "dryer state: %s" % self.state
            self.state_machine[self.state]()


if __name__ == "__main__":
    c = Controller(on_threshold=92.5)
    c.run()
