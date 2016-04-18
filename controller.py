import dryer
import time
import dsp
import filters
from twitter_handler import TwitterHandler


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
	self.twitter_handler = TwitterHandler()

    def compute_norm_sum(self):
    	try:
            samples, times = self.dryer.get_readings(self.mavg_samples+self.num_samples)
    	except Exception as e:
            print e
        norm = dsp.compute_norm(samples)
        fs = dsp.get_fs(times)
        norm_filtered = filters.bandpass_filter_signal(norm, 0.0009, 0.0001, fs)
        # norm_filtered = dsp.moving_average(norm, n=self.mavg_samples)
        # norm_filtered = bandpass_filter_signal(norm, lpf_cutoff, hpf_cutoff, fs)
        norm_slice = norm_filtered[self.mavg_samples:self.mavg_samples+self.num_samples]
        norm_sum = norm_slice.sum()
        return norm_sum


    def _on_state(self):
        norm_sum = self.compute_norm_sum()
        if norm_sum < self.on_threshold:
            self.state = "alert"
        time.sleep(self.on_sleep_duration)

    def _alert_state(self):
        # self.twitter_handler.send_tweet("@hemal laundrys done")
        self.state = "off"

    def _off_state(self):
        norm_sum = self.compute_norm_sum()
        if norm_sum > self.on_threshold:
            self.state = "on"

        time.sleep(self.on_sleep_duration)

    def run(self):
        while True:
            # print "dryer state: %s" % self.state
            print self.compute_norm_sum()
            time.sleep(1)
            # self.state_machine[self.state]()


if __name__ == "__main__":
    c = Controller(on_threshold=93.)
    c.run()
