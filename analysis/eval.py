import numpy as np, pandas as pd, predict as P
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import average_precision_score

files = ['S1_A1_s01.csv','S1_A1_s02.csv','S1_A1_s03.csv','S1_A1_s04.csv','S1_A1_s05.csv']
D = [P.build(f) for f in files]
FS = P.FS

def group(flag, gap):
    idx = np.where(flag)[0]
    if len(idx) == 0: return []
    return np.split(idx, np.where(np.diff(idx) > gap)[0] + 1)

def evaluate(y, p, thr):
    fl = p >= thr
    alarms = group(fl, int(0.3*FS))
    wins = group(y, 1)
    hit = sum(1 for w in wins if fl[w].any())
    fa = sum(1 for a in alarms if not y[a].any())
    return hit, len(wins), fa

rows = []
imps = []
for i in range(5):
    Xte, yte, tte, _ = D[i]
    Xtr = pd.concat([D[j][0] for j in range(5) if j != i])
    ytr = np.concatenate([D[j][1] for j in range(5) if j != i])
    m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.06,
        max_leaf_nodes=15, min_samples_leaf=40, l2_regularization=1.0,
        random_state=0).fit(Xtr, ytr)
    p = m.predict_proba(Xte)[:, 1]
    mins = len(yte)/FS/60
    chosen = None
    for q in np.linspace(0.999, 0.90, 80):
        thr = np.quantile(p, q)
        hit, nw, fa = evaluate(yte, p, thr)
        if fa/mins > 2.0:
            break
        chosen = (thr, hit, nw, fa/mins)
    if chosen:
        thr, hit, nw, fam = chosen
        rows.append((100*hit/nw, fam, nw))
        print(f'fold {i+1}: {nw:3d} events  recall={100*hit/nw:5.1f}%  '
              f'false alarms={fam:.2f}/min  ({mins:.1f} min)')
    if i == 0:
        r = permutation_importance(m, Xte, yte, n_repeats=5, random_state=0,
                                   scoring='average_precision')
        imps = sorted(zip(Xte.columns, r.importances_mean), key=lambda x: -x[1])[:8]

a = np.array(rows)
print()
print(f'MEAN at <=2 false alarms/min: recall={a[:,0].mean():.1f}%  FA={a[:,1].mean():.2f}/min')
print()
print('Top features (permutation importance, fold 1):')
for n, v in imps:
    print(f'   {n:12s} {v:+.4f}')
