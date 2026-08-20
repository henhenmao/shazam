# Shazam Music Recognition

Audio fingerprinting tool (Python scripts)  
Identifies a song from a short audio clip or recording, using the same general algorithm as Shazam.

Program computes a Short-Time Fourier Transform (STFT) of a song and picks the strongest spectral peaks per time window, producing a set of (time, frequency) points.  
Nearby peaks are paired together within a window. Pairs and their time differences are computed into hashes. These hashes are turned into a database.
Short clips of audio can be matched to hashes in the computed database. The same fingerprinting process is applied to the clip and each candidate in the database is given a score based on aligning hashes at a consistent time offset. The highest scoring song is the final match.

# How to use

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy scipy matplotlib tqdm
mkdir data

```
 place your sample `.wav` files in `data/`

```bash
python3 create_database.py
```
produces `database.pickle` and `song_index.pickle`

```bash
python3 findmatch.py <path to clip.wav>
```

this prints the ranked list of candidate matches with their scores.