"""Priorización de tarjetas: árbol de decisión que predice la probabilidad de error.
Con pocos datos usa una regla simple (arranque en frío)."""
import time
from sklearn.tree import DecisionTreeClassifier

MIN_ROWS = 30  # registros mínimos para entrenar el árbol


def features(n, hits, last_ts, total_ms, now):
    acc = hits / n if n else 0.5
    days = (now - last_ts) / 86400 if last_ts else 30
    avg_s = (total_ms / n) / 1000 if n else 0
    return [n, acc, days, avg_s]  # intentos, aciertos %, días sin repasar, tiempo medio


def build_dataset(answers):
    state, X, y = {}, [], []
    for a in answers:  # ordenadas por tiempo
        s = state.setdefault(a["card_id"], dict(n=0, h=0, last=None, ms=0))
        X.append(features(s["n"], s["h"], s["last"], s["ms"], a["ts"]))
        y.append(0 if a["correct"] else 1)  # 1 = error
        s["n"] += 1; s["h"] += a["correct"]; s["last"] = a["ts"]; s["ms"] += a["time_ms"]
    return X, y, state


def rank_cards(cards, answers):
    now = time.time()
    X, y, state = build_dataset(answers)
    model = None
    if len(X) >= MIN_ROWS and len(set(y)) == 2:
        model = DecisionTreeClassifier(max_depth=4, min_samples_leaf=3).fit(X, y)
    ranked = []
    for c in cards:
        s = state.get(c["id"], dict(n=0, h=0, last=None, ms=0))
        f = features(s["n"], s["h"], s["last"], s["ms"], now)
        risk = model.predict_proba([f])[0][1] if model else 1 - f[1]
        ranked.append({**c, "risk": round(float(risk), 3), "source": "árbol" if model else "reglas"})
    return sorted(ranked, key=lambda c: c["risk"], reverse=True)
