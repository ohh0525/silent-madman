# ============================================================================
#  push-to-github.ps1
#  一键把 silent-madman 仓库推送到 ohh0525/silent-madman
#  用法：在普通 PowerShell（管理员非必须）里，粘贴整段并回车
#  注意：脚本本身不包含你的 PAT；推送时会单独弹出用户名/PAT 输入框
# ============================================================================

$ErrorActionPreference = "Stop"

Write-Host "`n[1/5] 切到仓库目录" -ForegroundColor Cyan
Set-Location "D:\桌面\silent-madman"

Write-Host "`n[2/5] 核对本地状态" -ForegroundColor Cyan
git status --short --branch
git log --oneline -1

Write-Host "`n[3/5] 配置 Windows 凭据管理器 (一次配置, 永久记忆 PAT)" -ForegroundColor Cyan
git config --global credential.helper manager
Write-Host "  ✓ credential.helper = manager" -ForegroundColor Green

Write-Host "`n[4/5] 先尝试推送 — 若弹出凭据框,请填:" -ForegroundColor Yellow
Write-Host "   Username: ohh0525" -ForegroundColor Yellow
Write-Host "   Password: 粘贴你保存的 github_pat_xxxx... (不显示是正常的, 回车即可)" -ForegroundColor Yellow
Write-Host ""

git push -u origin main
$code = $LASTEXITCODE

Write-Host "`n[5/5] 推送后验证" -ForegroundColor Cyan
git status --short --branch
git ls-remote origin HEAD 2>$null | Out-Null

if ($code -eq 0) {
    Write-Host "`n✅ 推送成功!" -ForegroundColor Green
    Write-Host "   打开: https://github.com/ohh0525/silent-madman" -ForegroundColor Green
} else {
    Write-Host "`n❌ 推送失败, exit code = $code" -ForegroundColor Red
    Write-Host "   请把上面红字(报错原文)发给我, 我给你一条修复命令." -ForegroundColor Red
}
