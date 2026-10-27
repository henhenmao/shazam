FREQUENCY_BITS = 9
FAN_OUT = 10

# each anchor peak is paired with up to FAN_OUT peaks in a "target zone"
# just after it in time and close to it in frequency
MIN_TIME_DELTA = 1
MAX_TIME_DELTA = 64
MAX_FREQUENCY_DELTA = 128


def create_hashes(constellation_map, song_id=None):
    for i, (anchor_time, anchor_frequency) in enumerate(constellation_map):
        pairs = 0

        for target_time, target_frequency in constellation_map[i+1:]:
            time_delta = target_time - anchor_time
            if time_delta > MAX_TIME_DELTA:
                break
            if time_delta < MIN_TIME_DELTA or abs(target_frequency - anchor_frequency) > MAX_FREQUENCY_DELTA:
                continue

            hash_value = (
                anchor_frequency
                | (target_frequency << FREQUENCY_BITS)
                | (time_delta << (2 * FREQUENCY_BITS))
            )
            yield hash_value, (anchor_time, song_id)

            pairs += 1
            if pairs == FAN_OUT:
                break
