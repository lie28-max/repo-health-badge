# -*- coding: utf-8 -*-
"""Repo Health Badge - GitHub Action 入口"""
import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyze import analyze_repo
from src.badge import generate_badge, generate_summary


def main():
    """主函数"""
    # 从环境变量获取配置
    repo_full = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    output_format = os.environ.get("OUTPUT_FORMAT", "svg")
    output_path = os.environ.get("OUTPUT_PATH", "health-badge.svg")

    if "/" not in repo_full:
        print("错误: 无法识别仓库信息")
        print(f"GITHUB_REPOSITORY: {repo_full}")
        sys.exit(1)

    owner, repo = repo_full.split("/", 1)
    print(f"正在分析仓库: {owner}/{repo}")

    # 分析仓库
    result = analyze_repo(owner, repo, token)

    if result["score"] == 0 and not result["checks"]:
        print("错误: 无法获取仓库信息")
        sys.exit(1)

    print(f"\n评分结果: {result['score']}/100 ({result['grade']})")
    for check in result["checks"]:
        print(f"  {check['name']}: {check['score']}/{check['max']} - {check['detail']}")

    # 生成徽章
    badge = generate_badge(result["score"], result["grade"], output_format)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(badge)
    print(f"\n徽章已保存到: {output_path}")

    # 生成摘要
    summary = generate_summary(result)

    # 尝试写入 GitHub Actions 输出
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(summary)
        print("摘要已写入 Actions Step Summary")

    # 设置输出变量
    output_file = os.environ.get("GITHUB_OUTPUT", "")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"score={result['score']}\n")
            f.write(f"grade={result['grade']}\n")
            f.write(f"badge_path={output_path}\n")
            f.write(f"summary<<EOF\n{summary}\nEOF\n")
        print("输出变量已设置")

    # 保存 JSON 结果
    json_path = output_path.rsplit(".", 1)[0] + ".json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"JSON 结果已保存到: {json_path}")

    return result


if __name__ == "__main__":
    main()
