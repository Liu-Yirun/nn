# 将 mujoco_plex 项目合并到 nn 课程仓库
# 用法: powershell -ExecutionPolicy Bypass -File integrate_to_nn.ps1
# 前提: 已克隆 https://github.com/Liu-Yirun/nn 到 C:\Users\18022\Desktop\nn

$ErrorActionPreference = "Stop"
$nnRoot = "C:\Users\18022\Desktop\nn"
$bundle = "C:\Users\18022\Desktop\mujoco_plex\nn_bundle"

if (-not (Test-Path "$nnRoot\.git")) {
    Write-Host "错误: 未找到 nn 仓库，请先克隆到 $nnRoot"
    Write-Host "git clone --depth 1 https://github.com/Liu-Yirun/nn.git $nnRoot"
    exit 1
}

# 复制源码与文档
Copy-Item "$bundle\src\mujoco_plex" "$nnRoot\src\mujoco_plex" -Recurse -Force
Copy-Item "$bundle\docs\mujoco_plex" "$nnRoot\docs\mujoco_plex" -Recurse -Force
Write-Host "已复制 src/mujoco_plex 和 docs/mujoco_plex"

# 更新 mkdocs.yml 导航
$mkdocs = Join-Path $nnRoot "mkdocs.yml"
$content = Get-Content $mkdocs -Raw -Encoding UTF8
$navLine = "- ANYmal C四足机器人仿真: 'mujoco_plex/README.md'"
if ($content -notmatch "mujoco_plex") {
    $content = $content -replace "(- CARLA多传感器自动驾驶仿真平台: 'carla_multisensor_platform/carla_multisensor_platform.md')", "`$1`n$navLine"
    Set-Content $mkdocs $content -Encoding UTF8 -NoNewline
    Write-Host "已更新 mkdocs.yml 导航"
} else {
    Write-Host "mkdocs.yml 已包含 mujoco_plex，跳过"
}

# 更新 docs/index.md 索引
$index = Join-Path $nnRoot "docs\index.md"
$idx = Get-Content $index -Raw -Encoding UTF8
$link = "- [__ANYmal C四足机器人仿真__](./mujoco_plex/README.md) - 基于 MuJoCo 的 ANYmal C 四足机器人仿真与腿部摆动控制"
if ($idx -notmatch "mujoco_plex") {
  $idx = $idx -replace "(- \[__机器人仿真\(MuJoCo\)__\]\(ant_robot/机器人仿真系统.md\))", "`$1`n`n$link"
    Set-Content $index $idx -Encoding UTF8 -NoNewline
    Write-Host "已更新 docs/index.md 索引"
} else {
    Write-Host "docs/index.md 已包含 mujoco_plex，跳过"
}

Write-Host ""
Write-Host "合并完成! 下一步:"
Write-Host "  cd $nnRoot"
Write-Host "  git add src/mujoco_plex docs/mujoco_plex mkdocs.yml docs/index.md"
Write-Host "  git commit -m '添加 MuJoCo ANYmal C 四足机器人仿真项目'"
Write-Host "  git push origin main"
