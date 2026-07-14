#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理评审报告生成器
读入结构化结果 JSON，生成 MD 文档 + 精美网页版 HTML（主色 #C8102E）。

用法：
  python build_report.py --input result.json --md-out report.md --html-out report.html
  python build_report.py                      # 使用内置演示数据，输出到 ./output/

输入 JSON 结构：
{
  "meta": {"company":"示例制造有限公司","period":"2026年度","date":"2026-04-15","chair":"总经理","attendees":"各部门负责人","last_review":"2025-04-10"},
  "inputs": [{"category":"审核结果","summary":"内审12项，关闭率92%","trend":"稳定"}],
  "objectives": [{"name":"一次交检合格率","target":">=98%","actual":"96.5%","status":"未达成"}],
  "effectiveness": "体系基本有效，需局部优化",
  "outputs": [{"id":"MR-01","action":"修订装配SOP并培训","owner":"生产部","due":"2026-06-30","status":"待启动"}]
}
"""
import argparse
import json
import os
import sys
import html
from datetime import datetime

MAIN = "#C8102E"  # 主色


def esc(s):
    return html.escape(str(s), quote=True)


def load_result(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------- 内置演示数据 -----------------------------
DEMO = {
    "meta": {
        "company": "示例制造有限公司（演示数据，待企业补充）",
        "period": "2026年度",
        "date": "2026-04-15",
        "chair": "总经理",
        "attendees": "各部门负责人",
        "last_review": "2025-04-10"
    },
    "inputs": [
        {"category": "审核结果", "summary": "内审发现12项，整改关闭率92%；外审通过无严重不符合", "trend": "稳定"},
        {"category": "顾客反馈", "summary": "投诉28起，满意度89分，退货率1.2%", "trend": "稳定"},
        {"category": "过程绩效与产品符合性", "summary": "关键过程合格率97.2%，Cpk均值1.33", "trend": "上升"},
        {"category": "纠正措施状态", "summary": "纠正措施到期关闭率95%，重复发生2项", "trend": "稳定"},
        {"category": "以往评审跟踪措施", "summary": "上次3项措施全部完成", "trend": "—"},
        {"category": "可能影响体系的变更", "summary": "组织架构调整1项，新增产线1条", "trend": "—"},
        {"category": "改进建议", "summary": "收集改进建议6条，采纳4条", "trend": "—"}
    ],
    "objectives": [
        {"name": "产品一次交检合格率", "target": "≥98%", "actual": "96.5%", "status": "未达成"},
        {"name": "顾客满意度", "target": "≥90分", "actual": "89分", "status": "未达成"},
        {"name": "来料合格率", "target": "≥99%", "actual": "99.1%", "status": "达成"}
    ],
    "effectiveness": "体系基本有效，需局部优化：过程绩效呈上升趋势，但一次交检合格率与顾客满意度未达标，需针对性改进。",
    "outputs": [
        {"id": "MR-01", "action": "修订装配SOP并专项培训，提升一次交检合格率", "owner": "生产部", "due": "2026-06-30", "status": "待启动"},
        {"id": "MR-02", "action": "建立顾客满意度提升专项（投诉闭环+回访）", "owner": "质量部", "due": "2026-07-31", "status": "待启动"},
        {"id": "MR-03", "action": "新产线过程审核纳入下年内审方案", "owner": "体系部", "due": "2026-12-31", "status": "待启动"}
    ]
}


# ----------------------------- MD 生成 -----------------------------
def build_md(r):
    L = []
    m = r.get("meta", {})
    L.append("# 管理评审报告\n")
    L.append("## 一、评审基本信息\n")
    L.append(f"- 企业名称：{m.get('company','')}")
    L.append(f"- 评审周期：{m.get('period','')}")
    L.append(f"- 评审日期：{m.get('date','')}")
    L.append(f"- 主持人：{m.get('chair','')}")
    L.append(f"- 参会人员：{m.get('attendees','')}")
    L.append(f"- 上次评审日期：{m.get('last_review','')}")
    L.append("")
    L.append("## 二、评审输入综述\n")
    L.append("| 输入类别 | 概要 | 趋势 |")
    L.append("|----------|------|------|")
    for it in r.get("inputs", []) or []:
        L.append(f"| {it.get('category','')} | {it.get('summary','')} | {it.get('trend','')} |")
    L.append("")
    L.append("## 三、质量目标达成情况\n")
    L.append("| 目标 | 目标值 | 实际值 | 状态 |")
    L.append("|------|--------|--------|------|")
    for o in r.get("objectives", []) or []:
        L.append(f"| {o.get('name','')} | {o.get('target','')} | {o.get('actual','')} | {o.get('status','')} |")
    L.append("")
    L.append("## 四、体系有效性评价\n")
    L.append(f"- 评价结论：{r.get('effectiveness','')} 〔结论由企业签署〕")
    L.append("")
    L.append("## 五、评审输出与改进项跟踪\n")
    L.append("| 编号 | 改进措施 | 责任部门 | 计划完成 | 状态 |")
    L.append("|------|----------|----------|----------|------|")
    for o in r.get("outputs", []) or []:
        L.append(f"| {o.get('id','')} | {o.get('action','')} | {o.get('owner','')} | {o.get('due','')} | {o.get('status','')} |")
    L.append("")
    L.append(f"> 报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 主色 {MAIN}")
    return "\n".join(L)


# ----------------------------- HTML 生成 -----------------------------
CSS = """
:root{ --main:%s; --bg:#f7f8fa; --card:#fff; --ink:#1f2937; --muted:#6b7280; --line:#e5e7eb; }
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;padding:32px}
.wrap{max-width:1100px;margin:0 auto}
header{text-align:center;padding:30px 0 20px;border-bottom:3px solid var(--main);margin-bottom:28px}
header h1{font-size:27px;letter-spacing:1px}
header .meta{color:var(--muted);font-size:14px;margin-top:10px}
.sec{background:var(--card);border-radius:14px;padding:24px;box-shadow:0 4px 16px rgba(0,0,0,.06);margin-bottom:26px}
.sec h2{font-size:21px;margin-bottom:16px;border-left:5px solid var(--main);padding-left:12px}
table{width:100%%;border-collapse:collapse;font-size:14px}
th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
th{background:#fef2f4;color:var(--main);font-weight:700}
tr:nth-child(even){background:#fafafa}
.eff{background:#fef2f4;border-left:5px solid var(--main);padding:16px 18px;border-radius:8px;font-size:15px}
.s-fail{color:#b91c1c;font-weight:700} .s-ok{color:#15803d;font-weight:700}
footer{text-align:center;color:var(--muted);font-size:12px;margin-top:20px}
""" % MAIN


def build_html(r):
    m = r.get("meta", {})

    def obj_status_cls(s):
        return "s-ok" if s == "达成" else "s-fail"

    in_rows = "".join(
        f"<tr><td>{esc(it.get('category',''))}</td><td>{esc(it.get('summary',''))}</td><td>{esc(it.get('trend',''))}</td></tr>"
        for it in r.get("inputs", []) or [])
    obj_rows = "".join(
        f"<tr><td>{esc(o.get('name',''))}</td><td>{esc(o.get('target',''))}</td>"
        f"<td>{esc(o.get('actual',''))}</td><td class='{obj_status_cls(o.get('status',''))}'>{esc(o.get('status',''))}</td></tr>"
        for o in r.get("objectives", []) or [])
    out_rows = "".join(
        f"<tr><td>{esc(o.get('id',''))}</td><td>{esc(o.get('action',''))}</td>"
        f"<td>{esc(o.get('owner',''))}</td><td>{esc(o.get('due',''))}</td><td>{esc(o.get('status',''))}</td></tr>"
        for o in r.get("outputs", []) or [])

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>管理评审报告 · {esc(m.get('company',''))}</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<header>
  <h1>管理评审报告</h1>
  <div class="meta">{esc(m.get('company',''))} ｜ {esc(m.get('period',''))} ｜ {esc(m.get('date',''))}</div>
  <div class="meta">主持人：{esc(m.get('chair',''))} ｜ 参会：{esc(m.get('attendees',''))} ｜ 上次评审：{esc(m.get('last_review',''))}</div>
</header>

<section class="sec">
  <h2>一、评审输入综述</h2>
  <table><thead><tr><th>输入类别</th><th>概要</th><th>趋势</th></tr></thead>
  <tbody>{in_rows}</tbody></table>
</section>

<section class="sec">
  <h2>二、质量目标达成情况</h2>
  <table><thead><tr><th>目标</th><th>目标值</th><th>实际值</th><th>状态</th></tr></thead>
  <tbody>{obj_rows}</tbody></table>
</section>

<section class="sec">
  <h2>三、体系有效性评价</h2>
  <div class="eff">{esc(r.get('effectiveness',''))} 〔结论由企业签署〕</div>
</section>

<section class="sec">
  <h2>四、评审输出与改进项跟踪</h2>
  <table><thead><tr><th>编号</th><th>改进措施</th><th>责任部门</th><th>计划完成</th><th>状态</th></tr></thead>
  <tbody>{out_rows}</tbody></table>
</section>

<footer>本报告由 管理评审技能 生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')} · 主色 {MAIN}</footer>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="管理评审报告生成器")
    ap.add_argument("--input", help="结构化结果 JSON 路径（缺省使用内置演示数据）")
    ap.add_argument("--md-out", help="输出 MD 路径")
    ap.add_argument("--html-out", help="输出 HTML 路径")
    args = ap.parse_args()

    if args.input:
        try:
            r = load_result(args.input)
        except Exception as e:
            sys.stderr.write(f"读取输入失败：{e}\n")
            sys.exit(1)
    else:
        r = DEMO
        sys.stderr.write("未指定 --input，使用内置演示数据。\n")

    if not args.md_out and not args.html_out:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(out_dir, exist_ok=True)
        args.md_out = os.path.join(out_dir, "review_report.md")
        args.html_out = os.path.join(out_dir, "review_report.html")

    if args.md_out:
        with open(args.md_out, "w", encoding="utf-8") as f:
            f.write(build_md(r))
        sys.stderr.write(f"MD 已生成：{args.md_out}\n")
    if args.html_out:
        with open(args.html_out, "w", encoding="utf-8") as f:
            f.write(build_html(r))
        sys.stderr.write(f"HTML 已生成：{args.html_out}\n")


if __name__ == "__main__":
    main()
