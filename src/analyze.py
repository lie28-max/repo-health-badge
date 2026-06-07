# -*- coding: utf-8 -*-
"""仓库健康分析模块 - 兼容 GitHub Actions 和本地环境"""
import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta


def _api_get(url, headers, timeout=30):
    """通过 urllib 调用 GitHub API（无第三方依赖）"""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def _api_get_gh(url, headers):
    """通过 gh CLI 调用（本地环境备选）"""
    import subprocess
    try:
        api_path = url.replace("https://api.github.com/", "")
        result = subprocess.run(
            ["gh", "api", api_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return None


def _get(url, headers):
    """统一 API 调用入口，优先 urllib，gh CLI 备选"""
    result = _api_get(url, headers)
    if result is not None:
        return result
    return _api_get_gh(url, headers)


def analyze_repo(owner, repo, token=None):
    """分析仓库健康状况，返回评分和详情"""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    result = {
        "score": 0,
        "grade": "?",
        "details": {},
        "checks": []
    }

    # 获取仓库基本信息
    repo_info = _get(f"https://api.github.com/repos/{owner}/{repo}", headers)
    if not repo_info:
        return result

    score = 0

    # 1. 基础指标 (30分)
    stars = repo_info.get("stargazers_count", 0)
    forks = repo_info.get("forks_count", 0)
    watchers = repo_info.get("subscribers_count", 0)

    star_score = min(stars / 100, 1) * 15
    fork_score = min(forks / 50, 1) * 10
    watcher_score = min(watchers / 20, 1) * 5
    score += star_score + fork_score + watcher_score

    result["checks"].append({
        "name": "基础指标",
        "score": round(star_score + fork_score + watcher_score, 1),
        "max": 30,
        "detail": f"Stars {stars} | Forks {forks} | Watchers {watchers}"
    })

    # 2. 活跃度 (25分)
    since = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={since}&per_page=1"
    commits_info = _get(commits_url, headers)
    recent_commits = len(commits_info) if isinstance(commits_info, list) else 0
    # 如果只有 1 条，尝试用 link header 判断总数
    if commits_info and isinstance(commits_info, list) and len(commits_info) == 1:
        recent_commits = _count_commits(owner, repo, since, headers)
    commit_score = min(recent_commits / 30, 1) * 15

    open_issues = repo_info.get("open_issues_count", 0)
    issues_score = 10 if 0 < open_issues < 50 else 5 if open_issues > 0 else 0

    score += commit_score + issues_score

    result["checks"].append({
        "name": "项目活跃度",
        "score": round(commit_score + issues_score, 1),
        "max": 25,
        "detail": f"近30天 {recent_commits} 次提交 | {open_issues} 个开放Issue"
    })

    # 3. 代码质量 (25分)
    has_license = 1 if repo_info.get("license") else 0
    has_readme = 1 if _check_file(owner, repo, "README.md", headers) else 0
    has_contributing = 1 if _check_file(owner, repo, "CONTRIBUTING.md", headers) else 0
    has_security = 1 if _check_file(owner, repo, "SECURITY.md", headers) else 0
    has_funding = 1 if _check_file(owner, repo, ".github/FUNDING.yml", headers) else 0
    has_topics = 1 if repo_info.get("topics") else 0

    quality_score = (has_license + has_readme + has_contributing +
                     has_security + has_funding + has_topics) * (25 / 6)
    score += quality_score

    quality_items = []
    if has_license: quality_items.append("License")
    if has_readme: quality_items.append("README")
    if has_contributing: quality_items.append("CONTRIBUTING")
    if has_security: quality_items.append("SECURITY")
    if has_funding: quality_items.append("FUNDING")
    if has_topics: quality_items.append("Topics")
    result["checks"].append({
        "name": "代码质量",
        "score": round(quality_score, 1),
        "max": 25,
        "detail": ", ".join(quality_items) if quality_items else "None"
    })

    # 4. 社区健康 (20分)
    issues_list = _get(
        f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=10&sort=updated",
        headers
    )
    prs_list = _get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=10&sort=updated",
        headers
    )
    has_issue_template = 1 if _check_file(owner, repo, ".github/ISSUE_TEMPLATE", headers, is_dir=True) else 0
    has_pr_template = 1 if _check_file(owner, repo, ".github/PULL_REQUEST_TEMPLATE.md", headers) else 0

    num_issues = len(issues_list) if isinstance(issues_list, list) else 0
    num_prs = len(prs_list) if isinstance(prs_list, list) else 0

    community_score = min(num_issues / 5, 1) * 8 + \
                      min(num_prs / 5, 1) * 8 + \
                      has_issue_template * 2 + has_pr_template * 2
    score += community_score

    community_items = []
    if num_issues: community_items.append(f"{num_issues}个近期Issue")
    if num_prs: community_items.append(f"{num_prs}个近期PR")
    if has_issue_template: community_items.append("Issue模板")
    if has_pr_template: community_items.append("PR模板")
    result["checks"].append({
        "name": "社区健康",
        "score": round(community_score, 1),
        "max": 20,
        "detail": " | ".join(community_items) if community_items else "无"
    })

    # 计算总分和等级
    final_score = min(round(score), 100)
    if final_score >= 80: grade = "A"
    elif final_score >= 60: grade = "B"
    elif final_score >= 40: grade = "C"
    elif final_score >= 20: grade = "D"
    else: grade = "F"

    result["score"] = final_score
    result["grade"] = grade
    result["repo"] = f"{owner}/{repo}"
    result["name"] = repo_info.get("name", repo)
    result["description"] = repo_info.get("description", "")
    result["updated_at"] = datetime.utcnow().isoformat()

    return result


def _count_commits(owner, repo, since, headers):
    """估算提交数（GitHub API 默认最多返回 1000 条）"""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={since}&per_page=100"
    commits = _get(url, headers)
    return len(commits) if isinstance(commits, list) else 0


def _check_file(owner, repo, path, headers, is_dir=False):
    """检查文件是否存在"""
    info = _get(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}", headers)
    if info is None:
        return False
    if is_dir:
        return info.get("type") == "dir"
    return info.get("type") == "file"
