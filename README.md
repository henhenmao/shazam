# Shazam Music Recognition

Audio fingerprinting tool (Python scripts)  
Identifies a song from a short audio clip or recording, using the same general algorithm as Shazam.

Each song is converted to mono, resampled to 11,025 Hz and turned into a spectrogram (Short-Time Fourier Transform). Peaks are points that are louder than everything around them in both time and frequency, capped to the loudest 30 per second, producing a constellation map of (time, frequency) points.
Each peak is paired with up to 10 nearby peaks that come shortly after it. The two frequencies and the time gap between them form a hash, and these hashes are stored in a database.
Short clips of audio go through the same fingerprinting process. Each song in the database is scored by how many of the clip's hashes line up at one consistent time offset. The highest scoring song is the match, as long as its score is clearly above chance (`MIN_MATCH_SCORE` in `find_match.py`).

Like Shazam, this recognizes a recording of the original song (including one played from a speaker and recorded on a phone).

# How to use

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy scipy tqdm matplotlib
mkdir data
```
 place your sample `.wav` files in `data/`
```bash
python3 create_database.py
```
produces `database.pickle` and `song_index.pickle`

```bash
python3 find_match.py <path to clip.wav>
```

this prints the ranked list of candidate matches with their scores.

# Testing

```bash
python3 evaluate.py
python3 evaluate.py --seconds 5
```
compare every file in `recordings/` with the song it should match (or with no match). `--seconds` only uses the start of each recording, to test shorter clips.
