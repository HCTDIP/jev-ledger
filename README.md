# jev 公开哈希账本 · 白箱

**白箱，不是黑箱。** jev 每做一次判定，都会留下指纹，公开在这里，谁都能取、谁都能复核。

- 🌐 验证页（直接点开）：<https://hctdip.github.io/jev-ledger/>
- 📄 逐条数据：<https://raw.githubusercontent.com/HCTDIP/jev-ledger/main/ledger_public.jsonl>
- 📐 哈希口径：<https://github.com/HCTDIP/jev-ledger/blob/main/SPEC.md>

## 只存哈希，不存原文

公开的字段：**预测概率 `p` · 判定 `verdict` · 到期日 `due` · 结果 `outcome` · `input_hash` · `output_hash` · `code_hash` · `subject_hash` · `record_digest`**
不公开：主体真名、输入原文、证据细节 —— 哈希不泄露内容，但**能证明记录没被改过**。

## 四个指纹

| 指纹 | 公式 | 用来查 |
|---|---|---|
| `input_hash` | `sha256(canon({model,state,questions}))[:32]` | **输入是不是给偏了**（首查） |
| `output_hash` | `sha256(canon(response−_cache))[:32]` | 同输入重跑，**模型是不是漂了** |
| `code_hash` | git sha / `src-` + 脚本哈希 | 是不是**改过判定逻辑** |
| `ledger_digest` | `sha256(ledger_public.jsonl 原始字节)` | **整表**被改过没有（改一行就变） |

## 自己验（不用信任何人）

```bash
curl -O https://raw.githubusercontent.com/HCTDIP/jev-ledger/main/ledger_public.jsonl
curl -O https://raw.githubusercontent.com/HCTDIP/jev-ledger/main/verify.py
curl -O https://raw.githubusercontent.com/HCTDIP/jev-ledger/main/SPEC.md
python3 verify.py digest            # 复算整表摘要
python3 verify.py input.json        # 复算某条判定的 input_hash（{"model":…,"state":…,"questions":…}）
```

静态页 + 原始文件 = **没有服务端，不会 503**。
