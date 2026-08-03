import importlib, numpy as np, pandas as pd
import predict as P
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, roc_auc_score

files = ['S1_A1_s01.csv','S1_A1_s02.csv','S1_A1_s03.csv','S1_A1_s04.csv','S1_A1_s05.csv']
windows = [(0.0,0.2),(0.1,0.3),(0.2,0.4),(0.3,0.5),(0.5,0.7),(0.8,1.0)]

print('lead window (s)   prev%    AP     lift   ROC-AUC   AP(level-only)')
for lo, hi in windows:
    P.LEAD_LO, P.LEAD_HI = lo, hi
    D = [P.build(f) for f in files]
    aps, aucs, prevs, base = [], [], [], []
    for i in range(5):
        Xte, yte = D[i][0], D[i][1]
        if yte.sum() < 5: continue
        Xtr = pd.concat([D[j][0] for j in range(5) if j != i])
        ytr = np.concatenate([D[j][1] for j in range(5) if j != i])
        m = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.06,
            max_leaf_nodes=15, min_samples_leaf=40, l2_regularization=1.0,
            random_state=0).fit(Xtr, ytr)
        p = m.predict_proba(Xte)[:, 1]
        aps.append(average_precision_score(yte, p))
        aucs.append(roc_auc_score(yte, p))
        prevs.append(yte.mean())
        base.append(average_precision_score(yte, Xte['g'].values))
    ap, pv = np.mean(aps), np.mean(prevs)
    print(f'  {lo:.1f}-{hi:.1f}        {100*pv:5.2f}  {ap:.3f}  x{ap/pv:5.1f}   {np.mean(aucs):.3f}     {np.mean(base):.3f}')
