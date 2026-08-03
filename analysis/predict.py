import csv, numpy as np, pandas as pd
from pathlib import Path

THRESH = 1301
FS = 50.0                 # resample grid (Hz)
DT = 1.0/FS
LEAD_LO, LEAD_HI = 0.20, 0.40   # predict onset occurring 200-400 ms ahead
MIN_EVENT = 0.10          # event must stay above threshold >=100 ms
REFRACT = 0.5             # ignore candidates within 0.5 s after an event ends

UP = Path('/mnt/user-data/uploads')

def load(fn):
    recs = []
    with open(UP/fn) as fh:
        for r in csv.reader(fh):
            if len(r) != 12: continue
            try:
                recs.append((int(r[1]), int(r[2]), int(r[4]),
                             float(r[5]), float(r[6]), float(r[7]),
                             float(r[8]), float(r[9]), float(r[10])))
            except ValueError:
                continue
    a = np.array(recs, float)
    t = (a[:,0] - a[0,0]) / 1000.0
    ok = np.diff(t, prepend=t[0]-DT) > 0        # strictly increasing
    a, t = a[ok], t[ok]
    grid = np.arange(0, t[-1], DT)
    out = {'t': grid}
    out['grip'] = np.interp(grid, t, a[:,1])
    out['emg']  = np.interp(grid, t, a[:,2])
    acc = np.sqrt(a[:,3]**2 + a[:,4]**2 + a[:,5]**2)
    gyr = np.sqrt(a[:,6]**2 + a[:,7]**2 + a[:,8]**2)
    out['acc'] = np.interp(grid, t, acc)
    out['gyr'] = np.interp(grid, t, gyr)
    return pd.DataFrame(out)

def playing_mask(df):
    """bowing period: sustained gyro activity, longest contiguous block"""
    act = df['gyr'].rolling(int(2*FS), center=True, min_periods=1).mean()
    on = (act > 25).values
    idx = np.where(on)[0]
    if len(idx) < 100: return np.zeros(len(df), bool)
    splits = np.where(np.diff(idx) > int(3*FS))[0]
    blk = max(np.split(idx, splits+1), key=len)
    m = np.zeros(len(df), bool); m[blk] = True
    return m

def onsets(grip):
    """indices where grip crosses threshold upward and stays up >= MIN_EVENT"""
    above = grip > THRESH
    cross = np.where((~above[:-1]) & (above[1:]))[0] + 1
    keep = []
    n = int(MIN_EVENT*FS)
    for c in cross:
        if c+n < len(above) and above[c:c+n].all():
            keep.append(c)
    return np.array(keep, int), above

def features(df):
    g, e, ac, gy = df['grip'], df['emg'], df['acc'], df['gyr']
    def roll(s, sec, fn):
        return getattr(s.rolling(max(int(sec*FS),2), min_periods=2), fn)()
    F = pd.DataFrame(index=df.index)
    F['g']        = g
    F['g_m200']   = roll(g,0.2,'mean');  F['g_m500'] = roll(g,0.5,'mean')
    F['g_m1000']  = roll(g,1.0,'mean')
    F['g_s200']   = roll(g,0.2,'std');   F['g_s500'] = roll(g,0.5,'std')
    F['g_max1']   = roll(g,1.0,'max')
    F['g_d100']   = g - g.shift(int(0.1*FS))
    F['g_d300']   = g - g.shift(int(0.3*FS))
    F['g_slope2'] = (g - roll(g,0.2,'mean')) / 0.2
    F['g_slope5'] = (g - roll(g,0.5,'mean')) / 0.5
    F['g_head']   = THRESH - g                      # distance to threshold
    F['gy']       = gy
    F['gy_m200']  = roll(gy,0.2,'mean'); F['gy_m500'] = roll(gy,0.5,'mean')
    F['gy_s500']  = roll(gy,0.5,'std')
    F['gy_d300']  = gy - gy.shift(int(0.3*FS))
    F['ac_m500']  = roll(ac,0.5,'mean'); F['ac_s500'] = roll(ac,0.5,'std')
    emd = (e - e.rolling(int(2*FS), min_periods=2).median()).abs()
    F['emg_m200'] = roll(emd,0.2,'mean'); F['emg_m500'] = roll(emd,0.5,'mean')
    return F

def build(fn):
    df = load(fn)
    play = playing_mask(df)
    ons, above = onsets(df['grip'].values)
    n = len(df)
    # label: onset occurs in [t+LEAD_LO, t+LEAD_HI]
    y = np.zeros(n, bool)
    lo, hi = int(LEAD_LO*FS), int(LEAD_HI*FS)
    for c in ons:
        a0, a1 = c-hi, c-lo
        if a1 > 0: y[max(a0,0):a1] = True
    # candidates: playing, currently below threshold, not just after an event
    cand = play & (~above)
    # refractory: drop samples within REFRACT after any above-threshold sample
    ref = pd.Series(above).rolling(int(REFRACT*FS), min_periods=1).max().values.astype(bool)
    cand &= ~ref
    F = features(df)
    good = cand & F.notna().all(axis=1).values
    return F[good], y[good], df['t'].values[good], len(ons)
