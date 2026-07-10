# 查看训练结果
# 用法: .\scripts\view_results.ps1 [实验名]
# 例:   .\scripts\view_results.ps1 student_smoke_cpu
#       .\scripts\view_results.ps1 --list    # 列出所有实验

param([string]$ExpName = "student_smoke_cpu")

$ROOT = (Resolve-Path "$PSScriptRoot\..").Path
python "$ROOT\scripts\view_results.py" $ExpName
