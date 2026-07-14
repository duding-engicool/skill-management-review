#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""管理评审三阶段文档生成器（txt + md）。

用法：
  python build_report.py --stage prepare  --input info.json --out-dir .
  python build_report.py --stage meeting  --input info.json --out-dir .
  python build_report.py --stage closure  --input info.json --out-dir .

info.json 为各阶段收集到的信息（字段均可选，缺失自动标「待补充」）。
所有产物写入 --out-dir（默认当前工作目录），不依赖任何第三方库。
"""
import argparse
import json
import os
import datetime


def _g(d, key, default="待补充"):
    v = d.get(key)
    if v in (None, "", [], {}):
        return default
    return v


def _lines(v):
    if isinstance(v, list):
        return "\n".join(f"- {x}" for x in v) if v else "待补充"
    return str(v)


def render_prepare(d):
    files = {}
    files["管理评审计划"] = f"""# 管理评审计划

## 1. 基本信息
- 公司全称：{_g(d,'company')}
- 所属行业：{_g(d,'industry')}
- 执行标准：{_g(d,'standard')}
- 计划召开时间：{_g(d,'plan_time')}
- 会议主持人：{_g(d,'host')}
- 拟参会部门/人员：{_g(d,'attendees')}

## 2. 评审范围与依据
{_g(d,'scope','依据 '+_g(d,'standard'))}
"""
    files["会议议程"] = f"""# 管理评审会议议程

- 会议时间：{_g(d,'plan_time')}
- 主持人：{_g(d,'host')}
- 参会人员：{_g(d,'attendees')}
- 议程要点：
{_g(d,'agenda', _lines(['1. 听取体系运行报告','2. 各部门输入汇报','3. 最高管理者评价','4. 确定改进事项','5. 方针目标评审']))}
"""
    files["管理评审输入材料汇总"] = f"""# 管理评审输入材料汇总

## 1. 上次管评报告及整改关闭情况
{_g(d,'last_review')}

## 2. 本周期内外审结果及不符合项关闭
{_g(d,'audit_results')}

## 3. 质量目标达成 / 客户满意 / 投诉反馈
{_g(d,'performance')}

## 4. 内外部环境变化 / 风险机遇 / 资源缺口
{_g(d,'context_resource')}
"""
    files["体系三性初步分析报告"] = f"""# 体系三性（适宜性/充分性/有效性）初步分析报告

- 适宜性初步判断：{_g(d,'suitability','结合内外部环境变化待分析')}
- 充分性初步判断：{_g(d,'adequacy','结合资源与过程覆盖待分析')}
- 有效性初步判断：{_g(d,'effectiveness','结合目标达成与审核结果待分析')}
"""
    return files


def render_meeting(d):
    files = {}
    files["管理评审会议纪要"] = f"""# 管理评审会议纪要

## 1. 会议基本情况
{_g(d,'meeting_basic')}

## 2. 各部门核心发言要点
{_g(d,'dept_speech')}

## 3. 最高管理者评价（适宜性/充分性/有效性）
{_g(d,'top_management_review')}
"""
    files["评审结论初稿"] = f"""# 管理评审评审结论初稿

- 体系总体评价：{_g(d,'conclusion_draft','待形成')}
- 关键发现：{_g(d,'key_findings')}
"""
    files["改进项清单"] = f"""# 管理评审改进项清单

| 序号 | 改进事项 | 责任部门 | 完成期限 |
|------|----------|----------|----------|
{_g(d,'improvement_table', '| 1 | 待补充 | 待补充 | 待补充 |')}
"""
    return files


def render_closure(d):
    files = {}
    files["管理评审报告"] = f"""# 管理评审报告

## 1. 评审概况
{_g(d,'review_overview')}

## 2. 评审输入综述
{_g(d,'input_summary')}

## 3. 体系有效性评价（适宜性/充分性/有效性）
{_g(d,'effectiveness_eval')}

## 4. 改进措施与决议
{_g(d,'improvements')}

## 5. 质量方针与目标调整
{_g(d,'policy_objective_change','本次无调整 / 待补充')}

## 6. 评审结论
{_g(d,'final_conclusion')}
"""
    files["改进措施跟踪台账"] = f"""# 改进措施全周期跟踪台账

| 序号 | 改进措施 | 责任部门 | 整改完成情况 | 佐证/验证 | 是否关闭 | 未关闭原因/后续 |
|------|----------|----------|--------------|-----------|----------|----------------|
{_g(d,'tracking_table', '| 1 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |')}
"""
    files["评审闭环总结"] = f"""# 管理评审闭环总结报告

## 1. 改进措施整体完成情况
{_g(d,'closure_summary')}

## 2. 未关闭事项及处理方案
{_g(d,'open_items')}

## 3. 对下一次管理评审的输入
{_g(d,'next_input')}
"""
    return files


STAGES = {
    "prepare": render_prepare,
    "meeting": render_meeting,
    "closure": render_closure,
}


def md_to_txt(md: str) -> str:
    out = []
    for line in md.splitlines():
        s = line.rstrip()
        if s.startswith("# "):
            out.append(s[2:])
            out.append("=" * 40)
        elif s.startswith("## "):
            out.append(s[3:])
            out.append("-" * 36)
        elif s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            out.append(" | ".join(cells))
        elif s.startswith("- "):
            out.append(s)
        else:
            out.append(s)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="管理评审三阶段文档生成器")
    ap.add_argument("--stage", required=True, choices=list(STAGES.keys()), help="阶段")
    ap.add_argument("--input", required=True, help="收集信息 JSON 文件路径")
    ap.add_argument("--out-dir", default=os.getcwd(), help="输出目录，默认当前工作目录")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    files = STAGES[args.stage](data)
    date = datetime.date.today().strftime("%Y%m%d")
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    for name, content in files.items():
        with open(os.path.join(out_dir, f"{name}_{date}.md"), "w", encoding="utf-8") as f:
            f.write(content)
        with open(os.path.join(out_dir, f"{name}_{date}.txt"), "w", encoding="utf-8") as f:
            f.write(md_to_txt(content))
        print(f"已生成：{os.path.join(out_dir, name)}_{date}.md / .txt")


if __name__ == "__main__":
    main()
