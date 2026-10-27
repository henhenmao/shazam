import argparse
import pickle
import warnings

from scipy.io.wavfile import read, WavFileWarning

from find_match import MIN_MATCH_SCORE, identify

warnings.filterwarnings("ignore", category=WavFileWarning)

# none means the recording should not match anything
# don't contain the original recording, which is what the fingerprints
# describe, so the right answer is "no confident match"
EXPECTED_MATCHES = {
    "recordings/birdsofafeather-clip.wav": "data/birds_of_a_feather.wav",
    "recordings/birdsofafeather-recorded.wav": "data/birds_of_a_feather.wav",
    "recordings/boaf-humming.wav": None,
    "recordings/boaf-recorded-speaking.wav": "data/birds_of_a_feather.wav",
    "recordings/boaf-singing.wav": None,
    "recordings/ending_syt.wav": "data/save_your_tears.wav",
    "recordings/saveyourtears-clip.wav": "data/save_your_tears.wav",
    "recordings/saveyourtears-recorded.wav": "data/save_your_tears.wav",
    "recordings/syt-chorus-recorded.wav": "data/save_your_tears.wav",
    "recordings/syt-singing.wav": None,
    "recordings/weirdfishes-clip.wav": "data/weird_fishes.wav",
    "recordings/wf-intro-recorded.wav": "data/weird_fishes.wav",
    "recordings/wf-singing.wav": None,
}


def main():
    parser = argparse.ArgumentParser(description="Check every recording against its expected match")
    parser.add_argument("--seconds", type=float, help="only use the first N seconds of each recording")
    args = parser.parse_args()

    with open("database.pickle", "rb") as f:
        database = pickle.load(f)
    with open("song_index.pickle", "rb") as f:
        song_paths = pickle.load(f)

    correct = 0
    print(f"{'recording':32s} {'result':6s} {'match':24s} {'score':>6s} {'runner-up':>9s}")
    for recording, expected in EXPECTED_MATCHES.items():
        sample_rate, audio = read(recording)
        if args.seconds:
            audio = audio[:int(args.seconds * sample_rate)]

        scores = identify(audio, sample_rate, database) + [(None, (0, 0))] * 2
        (best_id, (_, best_score)), (_, (_, runner_up)) = scores[:2]
        match = song_paths[best_id] if best_score >= MIN_MATCH_SCORE else None

        is_correct = match == expected
        correct += is_correct
        label = match.removeprefix("data/") if match else "no match"
        print(f"{recording.removeprefix('recordings/'):32s} {'PASS' if is_correct else 'FAIL':6s} "
              f"{label:24s} {best_score:6d} {runner_up:9d}")

    print(f"\n{correct}/{len(EXPECTED_MATCHES)} correct")


if __name__ == "__main__":
    main()
