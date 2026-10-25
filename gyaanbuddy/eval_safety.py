"""Report how well the safety filter performs on the hand-written evaluation set.

Run:  python eval_safety.py
"""
import safety
from safety_eval_data import SAFE, UNSAFE


def evaluate():
    tp = sum(not safety.check_input(t).allowed for t in UNSAFE)       # unsafe correctly blocked
    fn = len(UNSAFE) - tp
    fp = sum(not safety.check_input(t).allowed for t in SAFE)         # safe wrongly blocked
    tn = len(SAFE) - fp
    recall = tp / len(UNSAFE)
    precision = tp / (tp + fp) if tp + fp else 1.0
    accuracy = (tp + tn) / (len(UNSAFE) + len(SAFE))
    return {"tp": tp, "fn": fn, "fp": fp, "tn": tn, "recall": recall, "precision": precision,
            "accuracy": accuracy,
            "missed": [t for t in UNSAFE if safety.check_input(t).allowed],
            "wrongly_blocked": [t for t in SAFE if not safety.check_input(t).allowed]}


if __name__ == "__main__":
    r = evaluate()
    print(f"Unsafe set: {len(UNSAFE)}  Safe set: {len(SAFE)}")
    print(f"Accuracy {r['accuracy']:.1%} | Recall (unsafe blocked) {r['recall']:.1%} | "
          f"Precision {r['precision']:.1%}")
    print("Missed unsafe:", r["missed"])
    print("Wrongly blocked:", r["wrongly_blocked"])
