#!/usr/bin/env python3
"""
match_report.py — 把匹配结果渲染为 Markdown 表格，给 Step 4 的用户确认环节使用。

输入: JSON via stdin 或 --input 文件
格式:
[
  {"module": "顶部导航", "decision": "REUSE", "component": "src/components/AppHeader",
   "confidence": 0.95, "notes": "完全匹配"},
  ...
]

decision ∈ {REUSE, EXTEND, NEW}
"""
import argparse
import json
import sys

DECISION_ORDER = {"REUSE": 0, "EXTEND": 1, "NEW": 2}


def render(items: list[dict]) -> str:
    items = sorted(items, key=lambda x: (DECISION_ORDER.get(x.get("decision", "NEW"), 9), -float(x.get("confidence") or 0)))
    lines = ["| 模块 | 决策 | 组件 | 置信度 | 备注 |", "|------|------|------|--------|------|"]
    for it in items:
        conf = it.get("confidence")
        conf_str = f"{conf:.2f}" if isinstance(conf, (int, float)) else "—"
        comp = it.get("component") or "—"
        lines.append(
            f"| {it.get('module', '?')} | {it.get('decision', 'NEW')} | `{comp}` | {conf_str} | {it.get('notes', '')} |"
        )
    counts = {"REUSE": 0, "EXTEND": 0, "NEW": 0}
    for it in items:
        counts[it.get("decision", "NEW")] = counts.get(it.get("decision", "NEW"), 0) + 1
    lines.append("")
    lines.append(
        f"**汇总**：复用 {counts.get('REUSE', 0)}，扩展 {counts.get('EXTEND', 0)}，新写 {counts.get('NEW', 0)}"
    )
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=str, default=None)
    args = ap.parse_args()

    raw = open(args.input).read() if args.input else sys.stdin.read()
    data = json.loads(raw)
    print(render(data))


if __name__ == "__main__":
    main()
