# Repo Health Badge - 一键发布脚本
# 使用方法: .\publish.ps1 -GitHubUsername "你的用户名"

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [string]$RepoName = "repo-health-badge",
    [string]$ProjectPath = "."
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Repo Health Badge - 一键发布脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 gh CLI
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "❌ GitHub CLI 未安装" -ForegroundColor Red
    Write-Host "正在安装..." -ForegroundColor Yellow
    winget install --id GitHub.cli -e --accept-source-agreements --accept-package-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 检查登录状态
Write-Host "📋 检查 GitHub 登录状态..." -ForegroundColor Yellow
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  未登录 GitHub" -ForegroundColor Yellow
    Write-Host "请在弹出的浏览器中完成登录：" -ForegroundColor Yellow
    Write-Host ""
    
    # 使用 device flow 登录
    gh auth login --hostname github.com --git-protocol https --web
    Write-Host ""
    Write-Host "✅ 登录成功！" -ForegroundColor Green
} else {
    Write-Host "✅ 已登录 GitHub" -ForegroundColor Green
}

Write-Host ""

# 更新 README 中的用户名
Write-Host "📝 更新 README 中的用户名..." -ForegroundColor Yellow
$readmePath = Join-Path $ProjectPath "README.md"
$readmeContent = Get-Content $readmePath -Raw
$readmeContent = $readmeContent -replace "GITHUB_USER", $GitHubUsername
Set-Content -Path $readmePath -Value $readmeContent -NoNewline

# 更新 FUNDING.yml
$fundingPath = Join-Path $ProjectPath ".github\FUNDING.yml"
$fundingContent = Get-Content $fundingPath -Raw
$fundingContent = $fundingContent -replace "GITHUB_USER", $GitHubUsername
Set-Content -Path $fundingPath -Value $fundingContent -NoNewline

Write-Host "✅ 用户名已更新为: $GitHubUsername" -ForegroundColor Green
Write-Host ""

# 初始化 git (如果还没有)
Set-Location $ProjectPath
if (-not (Test-Path ".git")) {
    Write-Host "📦 初始化 Git 仓库..." -ForegroundColor Yellow
    git init
    git branch -M main
}

# 提交代码
Write-Host "📦 提交代码..." -ForegroundColor Yellow
git add .
git commit -m "feat: initial release - repo health badge generator

- Repository health scoring (0-100)
- SVG badge generation
- GitHub Actions integration
- Detailed health reports
- 10+ health checks (README, LICENSE, CI/CD, tests, docs, etc.)"

Write-Host "✅ 代码已提交" -ForegroundColor Green
Write-Host ""

# 创建 GitHub 仓库
Write-Host "🌐 创建 GitHub 仓库..." -ForegroundColor Yellow
$repoExists = gh repo view "$GitHubUsername/$RepoName" 2>&1
if ($LASTEXITCODE -ne 0) {
    gh repo create $RepoName --public --description "Generate a health score badge for your repository" --source . --push
    Write-Host "✅ 仓库已创建并推送" -ForegroundColor Green
} else {
    Write-Host "⚠️  仓库已存在，正在推送..." -ForegroundColor Yellow
    git remote add origin "https://github.com/$GitHubUsername/$RepoName.git" 2>$null
    git push -u origin main
    Write-Host "✅ 代码已推送" -ForegroundColor Green
}

Write-Host ""

# 设置 GitHub Sponsors
Write-Host "💰 设置 GitHub Sponsors..." -ForegroundColor Yellow
Write-Host ""
Write-Host "请手动完成以下步骤启用 GitHub Sponsors：" -ForegroundColor Yellow
Write-Host "1. 访问 https://github.com/sponsors/dashboard" -ForegroundColor White
Write-Host "2. 点击 'Get started' 启用 Sponsors" -ForegroundColor White
Write-Host "3. 完成个人资料和银行/PayPal 信息" -ForegroundColor White
Write-Host "4. 等待审核通过（通常 1-2 天）" -ForegroundColor White
Write-Host ""

# 运行首次健康检查
Write-Host "🏥 触发首次健康检查..." -ForegroundColor Yellow
gh workflow run health-check.yml --ref main 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 健康检查已触发" -ForegroundColor Green
} else {
    Write-Host "⚠️  首次检查将在 push 后自动运行" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ 发布完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📦 仓库地址: https://github.com/$GitHubUsername/$RepoName" -ForegroundColor Cyan
Write-Host "🏥 健康检查: https://github.com/$GitHubUsername/$RepoName/actions" -ForegroundColor Cyan
Write-Host "💰 Sponsors: https://github.com/sponsors/$GitHubUsername" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "1. 启用 GitHub Sponsors（见上面的步骤）" -ForegroundColor White
Write-Host "2. 在社交媒体分享你的项目" -ForegroundColor White
Write-Host "3. 在 Reddit/HN 发布介绍" -ForegroundColor White
Write-Host ""
Write-Host "预期收入：" -ForegroundColor Yellow
Write-Host "- GitHub Sponsors: $5-50/月（取决于关注者）" -ForegroundColor White
Write-Host "- 贡献者赞助: $1-10/次" -ForegroundColor White
Write-Host ""
