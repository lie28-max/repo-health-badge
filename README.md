# 🏥 Repo Health Badge

[![Health Check](https://github.com/GITHUB_USER/repo-health-badge/actions/workflows/health-check.yml/badge.svg)](https://github.com/GITHUB_USER/repo-health-badge/actions)

> 🏥 一键生成仓库健康度评分徽章 — 检查 README、LICENSE、CI/CD、测试、文档等 10+ 项指标

## ✨ 功能

- 📊 **健康评分**: 0-100 分的综合评分
- 🎨 **SVG 徽章**: 自动生成美观的徽章图片
- ✅ **10+ 检查项**: README、LICENSE、CI/CD、测试、文档、安全等
- 🔄 **自动更新**: 每天自动运行，保持评分最新
- 📝 **详细报告**: 在 GitHub Actions Summary 中显示详细检查结果

## 🚀 快速开始

### 方法 1: 复制 Workflow 文件

将 `.github/workflows/health-check.yml` 复制到你的仓库中：

```bash
# 下载 workflow 文件
curl -o .github/workflows/health-check.yml https://raw.githubusercontent.com/GITHUB_USER/repo-health-badge/main/.github/workflows/health-check.yml
```

### 方法 2: 作为 GitHub Action 使用

```yaml
- name: Repository Health Check
  uses: GITHUB_USER/repo-health-badge@main
```

## 📊 评分标准

| 检查项 | 分值 | 说明 |
|--------|------|------|
| README | 20分 | 存在 +10，内容充实 +10 |
| LICENSE | 10分 | 存在 +10 |
| CONTRIBUTING | 10分 | 存在 +10 |
| .gitignore | 5分 | 存在 +5 |
| CI/CD | 15分 | 有 workflow +10，包含测试 +5 |
| 测试文件 | 10分 | 存在测试 +10 |
| 文档 | 10分 | 额外文档 +5，docs 目录 +5 |
| Issue 模板 | 5分 | 存在 +5 |
| SECURITY | 5分 | 存在 +5 |
| CHANGELOG | 5分 | 存在 +5 |
| 代码质量 | 5分 | 配置 linting +5 |

### 评分等级

- 🟢 **80-100**: 优秀 — 你的仓库非常健康！
- 🟢 **60-79**: 良好 — 还有一些改进空间
- 🟡 **40-59**: 一般 — 建议补充关键文件
- 🔴 **0-39**: 较差 — 需要大量改进

## 🎨 徽章示例

健康评分徽章会自动添加到你的 README 中：

```markdown
![Health](https://github.com/GITHUB_USER/repo-health-badge/raw/main/.github/health-badge.svg)
```

## 📝 详细报告

每次运行都会在 GitHub Actions 的 Summary 中生成详细报告：

```
## 🏥 Repo Health Score: 85/100

✅ README 存在 (+10)
✅ README 内容充实 (45行, +10)
✅ LICENSE 存在 (+10)
✅ CONTRIBUTING 存在 (+10)
✅ .gitignore 存在 (+5)
✅ GitHub Actions 存在 (2个workflow, +10)
✅ 包含测试 workflow (+5)
✅ 找到 12 个测试文件 (+10)
✅ 有额外文档 (3个文件, +5)
✅ docs 目录存在 (+5)
✅ Issue 模板存在 (+5)
✅ SECURITY.md 存在 (+5)
✅ CHANGELOG 存在 (+5)
```

## 🔧 自定义

你可以修改 workflow 文件来自定义检查项：

1. **修改分值**: 调整每个检查项的分值
2. **添加检查**: 添加新的检查项
3. **修改颜色**: 自定义评分等级的颜色

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 💖 支持

如果这个项目对你有帮助，请考虑赞助我！

[![Sponsor](https://img.shields.io/badge/-Sponsor-ea4aaa?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sponsors/GITHUB_USER)
