# jev 账本哈希口径（SPEC）

> 白箱的含义：**算法写在明处，任何人可用同一套算法复算，结果必须一致。**
> 只公开哈希，不公开原文 —— 哈希不泄露内容，但能证明记录未被改动。

## 规范化（canonical）

所有哈希都先做 canonical 序列化：

```
canonical(obj) = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
```

要点：键**字典序**排序、无多余空格、中文不转义。字典顺序不影响结果（同内容同哈希）。

## 四个指纹

| 字段 | 公式 | 用来查 |
|---|---|---|
| `input_hash` | `sha256(canonical({model, state, questions}))[:32]` | **输入是不是给偏了**（首查） |
| `output_hash` | `sha256(canonical(response))[:32]`，计算前剔除 `_cache` 字段 | 同输入重跑，**模型是不是漂了** |
| `subject_hash` | `sha256(subject_text)[:32]` | 主体可对号，但名字本身不外露 |
| `code_hash` | git short sha；非 git 目录则 `src-` + `sha256(判定脚本字节)[:12]` | 是不是**我们改过判定逻辑** |
| `record_digest` | `sha256(canonical(record))[:32]`（计算时排除 `record_digest` 自身） | 单条记录被改过没有 |
| `ledger_digest` | `sha256(ledger_public.jsonl 的原始字节)` | **整表**被改过没有（改一行就变） |

## 复算

```bash
# 复算单条输入指纹
python3 verify.py input.json          # {"model":..., "state":..., "questions":{...}}

# 复算整表摘要
python3 -c "import hashlib;print(hashlib.sha256(open('ledger_public.jsonl','rb').read()).hexdigest())"
```

## 为什么不公开原文

公开原文会泄露商业情报（合作主体、报价、赏金单）。**哈希足以证明「这份记录没被改」**：
把原文交给你信任的第三方 → 它重算哈希 → 与这里公开的值比对 → 对得上就说明我们没动过手脚。
