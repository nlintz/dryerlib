import dryer
import time

d = dryer.Dryer()
reading_buffer_size = 5
off_sleep_duration = 2
on_sleep_duration = 1
on_threshold = 0.1
state = False

for i in range(1000):
    d.collect_sample()
    if len(d.previous_readings) > reading_buffer_size:
	print d.get_lastn_norm_integral(reading_buffer_size)
        if d.get_lastn_norm_integral(reading_buffer_size) < on_threshold:
            if state is True:
                print ("laundry is done")
        if state == False:
            time.sleep(off_sleep_duration)
        else:
            time.sleep(on_sleep_duration)
