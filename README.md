# 管理评审（management-review）

> 范式：三阶段交互式（一问一答强制锁），产出 txt + md 文档，可直接打印。
> 内核提示词见 `references/management_review_phases.md`（忠实移植自 IMA 知识库「质量管理体系管理评审（三阶段AI辅助提示）」）。

## 简介

面向管理者代表与质量总监的管理评审助手。按三阶段（评审前准备 → 评审中会议 → 评审后闭环）逐步引导，每次只提 1 个问题、严格按固定提问清单序号推进，依据 ISO 9001:2015 第 9.3 条生成标准化管理评审计划、会议纪要、报告与改进项全周期跟踪台账。覆盖年度 / 季度评审场景。

## 适用角色

- 管理者代表（管代）：策划并主持评审、汇总输入、形成输出。
- 质量总监 / 最高管理者：审阅结论、批准改进决策与资源需求。

## 目录结构

```
management-review/
├── SKILL.md                      # 技能定义（10 节结构 + TRACE 自评）
├── README.md                     # 本文件
├── scripts/
│   └── build_report.py           # 三阶段文档生成器（txt + md）
└── references/
    ├── management_review_phases.md # 三阶段完整交互式提示词（铁律/提问清单/交付物）
    └── iso9001_clause93.md         # 第9.3条条款要点与输入映射
```

## 三阶段流程

1. **阶段1 评审前准备**（固定提问 1-6）→ 管评计划 / 会议议程 / 输入材料汇总 / 三性初步分析
2. **阶段2 评审中会议**（固定提问 1-5）→ 会议纪要 / 评审结论初稿 / 改进项清单
3. **阶段3 评审后闭环**（固定提问 1-3）→ 管评报告 / 改进措施跟踪台账 / 闭环总结

## 快速开始

1. 调用技能，Agent 按阶段1固定提问清单逐步引导（每次只问 1 个问题）。
2. 每阶段信息收齐后，Agent 输出该阶段正式交付物并请你确认。
3. 也可将收集到的信息写入 JSON，运行脚本直接生成文档：

```bash
python scripts/build_report.py --stage prepare --input info.json --out-dir .
python scripts/build_report.py --stage meeting --input info.json --out-dir .
python scripts/build_report.py --stage closure --input info.json --out-dir .
```

## 注意事项

- 决策与签字由企业人员负责，技能仅提供方法与模板。
- 标准条款以 ISO 9001:2015 第 9.3 条为准；IATF 补充输入以「待企业补充」标注。
- 演示数据为内置小样本，正式使用前请替换为真实数据。
