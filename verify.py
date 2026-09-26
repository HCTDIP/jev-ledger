#!/usr/bin/env python3
"""白箱验证：用公开的哈希口径复算，任何人可跑。"""
import hashlib, json, sys

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def input_hash(model, state, questions):
    return hashlib.sha256(canonical({"model": model, "state": state, "questions": questions}).encode()).hexdigest()[:32]

def ledger_digest(path="ledger_public.jsonl"):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "digest":
        d = json.load(open(sys.argv[1], encoding="utf-8"))
        h = input_hash(d.get("model"), d.get("state"), d.get("questions"))
        pub = {json.loads(l)["input_hash"] for l in open("ledger_public.jsonl", encoding="utf-8") if l.strip()}
        print("input_hash =", h)
        print("✅ 命中公开账本" if h in pub else "❌ 不在公开账本里（或输入不完整）")
    else:
        print("ledger_digest =", ledger_digest())
