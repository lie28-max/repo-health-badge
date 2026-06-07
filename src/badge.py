# -*- coding: utf-8 -*-
"""徽章生成模块 - 生成 SVG 健康评分徽章"""


def generate_badge(score, grade, format="svg"):
    """生成健康评分徽章"""
    if format == "svg":
        return _generate_svg(score, grade)
    elif format == "json":
        return _generate_json(score, grade)
    else:
        return _generate_svg(score, grade)


def _get_color(score):
    """根据分数返回颜色"""
    if score >= 80: return "#4c1"    # 绿色
    elif score >= 60: return "#97ca00"  # 浅绿
    elif score >= 40: return "#dfb317"  # 黄色
    elif score >= 20: return "#fe7d37"  # 橙色
    else: return "#e05d44"              # 红色


def _get_label_color(score):
    """根据分数返回标签背景色"""
    if score >= 80: return "#555"
    elif score >= 60: return "#555"
    elif score >= 40: return "#555"
    elif score >= 20: return "#555"
    else: return "#555"


def _generate_svg(score, grade):
    """生成 SVG 格式徽章"""
    color = _get_color(score)
    label_bg = _get_label_color(score)
    value = f"{score}/100 {grade}"

    # 计算宽度
    label_width = 90
    value_width = len(value) * 9 + 20
    total_width = label_width + value_width

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r">
    <rect width="{total_width}" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_width}" height="20" fill="{label_bg}"/>
    <rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>
    <rect width="{total_width}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="{label_width/2}" y="14" fill="#010101" fill-opacity=".3">repo health</text>
    <text x="{label_width/2}" y="13" fill="#fff">repo health</text>
    <text x="{label_width + value_width/2}" y="14" fill="#010101" fill-opacity=".3">{value}</text>
    <text x="{label_width + value_width/2}" y="13" fill="#fff">{value}</text>
  </g>
</svg>'''
    return svg


def _generate_json(score, grade):
    """生成 JSON 格式的徽章数据"""
    return {
        "schemaVersion": 1,
        "label": "repo health",
        "message": f"{score}/100 {grade}",
        "color": _get_color(score).lstrip("#")
    }


def generate_summary(result):
    """生成 Markdown 格式的摘要"""
    lines = [
        f"## 🏥 仓库健康报告: {result['repo']}",
        "",
        f"**总分: {result['score']}/100 ({result['grade']})**",
        "",
        "| 检查项 | 得分 | 详情 |",
        "|--------|------|------|",
    ]

    for check in result["checks"]:
        lines.append(f"| {check['name']} | {check['score']}/{check['max']} | {check['detail']} |")

    lines.extend([
        "",
        f"📅 生成时间: {result['updated_at']}",
        "",
        "---",
        "*由 [repo-health-badge](https://github.com/LIE28-MAX/repo-health-badge) 生成*"
    ])

    return "\n".join(lines)
