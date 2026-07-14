# 管理评审（management-review）

> 主色：`#C8102E`
> 范式：混合式双版（MD + HTML），由 `scripts/build_report.py` 生成。

## 简介

面向管理者代表与质量总监的管理评审助手。依据 ISO 9001:2015 第 9.3 条，引导收集七大类评审输入、评价体系的适宜性/充分性/有效性，生成标准化管理评审报告与改进项跟踪台账。覆盖年度 / 季度评审场景。

## 适用角色

- 管理者代表（管代）：策划并主持评审、汇总输入、形成输出。
- 质量总监 / 最高管理者：审阅结论、批准改进决策与资源需求。

## 目录结构

```
management-review/
├── SKILL.md                  # 技能定义（10 节结构 + TRACE 自评）
├── README.md                 # 本文件
├── scripts/
│   └── build_report.py       # 双版评审报告生成器（MD + HTML）
└── references/
    └── iso9001_clause93.md   # 第9.3条条款要点与输入映射
```

## 快速开始

1. 调用技能，提供：企业名称、评审周期、日期、主持人、参会、上次评审日期。
2. 逐项提供七大类评审输入（至少 4 类）。
3. 运行脚本产出评审报告双版：

```bash
python scripts/build_report.py --input sample.json --md-out output/review_report.md --html-out output/review_report.html
# 或使用内置演示数据：
python scripts/build_report.py
```

## 报告双版说明

- **MD 版**：适合归档、版本管理与签字批注。
- **HTML 版**：适合评审会演示，主色 `#C8102E`，含输入综述、目标达成、有效性评价与改进项跟踪卡。

## 注意事项

- 决策与签字由企业人员负责，技能仅提供方法与模板。
- 标准条款以 ISO 9001:2015 第 9.3 条为准；IATF 补充输入以「待企业补充」标注。
- 演示数据为内置小样本，正式使用前请替换为真实数据。
