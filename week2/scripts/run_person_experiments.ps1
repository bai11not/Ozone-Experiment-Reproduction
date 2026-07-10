# run_person_experiments.ps1
# 批量运行指定人员的全部 16 组实验
#
# 用法:
#   .\run_person_experiments.ps1 -Person A [-DataDir "d:\时空数据\臭氧预测资料"] [-Device cuda] [-StartFrom 1]
#
# 参数:
#   -Person   人员编号: A, B, C, D
#   -DataDir  数据目录
#   -Device   设备: cuda 或 cpu
#   -StartFrom 从第几组开始 (用于断点续跑, 默认 1)
#   -DryRun   仅打印命令不执行

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("A", "B", "C", "D")]
    [string] $Person,

    [string] $DataDir = "d:\时空数据\臭氧预测资料",
    [string] $Device = "cuda",
    [int] $StartFrom = 1,
    [switch] $DryRun
)

$ErrorActionPreference = "Stop"

# 人员固定参数
$PersonConfig = @{
    "A" = @{ Seed = 42; UseDiffusion = 0; Dir = "person_A_seed42_nodiff" }
    "B" = @{ Seed = 42; UseDiffusion = 1; Dir = "person_B_seed42_diff" }
    "C" = @{ Seed = 52; UseDiffusion = 0; Dir = "person_C_seed52_nodiff" }
    "D" = @{ Seed = 52; UseDiffusion = 1; Dir = "person_D_seed52_diff" }
}

$cfg = $PersonConfig[$Person]
$Seed = $cfg.Seed
$UseDiffusion = $cfg.UseDiffusion

# 16 组实验的 (seq_len, pre_len, use_pe_graph, use_pe_film) 组合
$Experiments = @(
    # seq_len, pre_len, pe_graph, pe_film
    @(12, 6, 0, 0),
    @(12, 6, 0, 1),
    @(12, 6, 1, 0),
    @(12, 6, 1, 1),
    @(12, 3, 0, 0),
    @(12, 3, 0, 1),
    @(12, 3, 1, 0),
    @(12, 3, 1, 1),
    @(24, 6, 0, 0),
    @(24, 6, 0, 1),
    @(24, 6, 1, 0),
    @(24, 6, 1, 1),
    @(24, 3, 0, 0),
    @(24, 3, 0, 1),
    @(24, 3, 1, 0),
    @(24, 3, 1, 1)
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  批量实验: Person $Person" -ForegroundColor Cyan
Write-Host "  Seed: $Seed, UseDiffusion: $UseDiffusion" -ForegroundColor Cyan
Write-Host "  共 16 组实验" -ForegroundColor Cyan
if ($StartFrom -gt 1) {
    Write-Host "  从第 $StartFrom 组开始" -ForegroundColor Yellow
}
if ($DryRun) {
    Write-Host "  [DRY RUN] 仅打印命令" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$TotalExperiments = 16
$SuccessCount = 0
$FailCount = 0
$FailedList = @()

# 结果目录
$ResultDir = Join-Path $PSScriptRoot ".." "results" $cfg.Dir
if (-not (Test-Path $ResultDir)) {
    New-Item -ItemType Directory -Path $ResultDir -Force | Out-Null
}

for ($i = $StartFrom - 1; $i -lt $TotalExperiments; $i++) {
    $exp = $Experiments[$i]
    $SeqLen = $exp[0]
    $PreLen = $exp[1]
    $PEGraph = $exp[2]
    $PEFiLM = $exp[3]

    $ExpNum = $i + 1
    $ExpId = "{0}{1:D2}" -f $Person, $ExpNum
    $ExpLabel = "s{0}-d{1}-l{2}-p{3}-g{4}-f{5}" -f $Seed, $UseDiffusion, $SeqLen, $PreLen, $PEGraph, $PEFiLM
    $ExpName = "{0}_{1}" -f $ExpId, $ExpLabel

    Write-Host ""
    Write-Host "--- 实验 $ExpNum / $TotalExperiments : $ExpId ($ExpLabel) ---" -ForegroundColor Yellow
    Write-Host "    参数: seed=$Seed, seq_len=$SeqLen, pre_len=$PreLen, diffusion=$UseDiffusion, pe_graph=$PEGraph, pe_film=$PEFiLM"

    if ($DryRun) {
        Write-Host "    [DRY RUN] 将运行: python train_pediffwavenet_noleak.py --exp_name $ExpName --seed $Seed ..." -ForegroundColor Gray
        $SuccessCount++
        continue
    }

    try {
        $startTime = Get-Date

        # 调用单次实验脚本
        $scriptPath = Join-Path $PSScriptRoot "run_single_experiment.ps1"
        & $scriptPath `
            -Seed $Seed `
            -SeqLen $SeqLen `
            -PreLen $PreLen `
            -UseDiffusion $UseDiffusion `
            -UsePEGraph $PEGraph `
            -UsePEFiLM $PEFiLM `
            -ExpName $ExpName `
            -DataDir $DataDir `
            -Device $Device

        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalMinutes

        # 复制结果到 week2/results/
        $sourceOutDir = "$DataDir\matrix_N95_PEDiffWaveNet_noleak_$ExpName"
        $destDir = Join-Path $ResultDir $ExpId

        if (Test-Path $sourceOutDir) {
            # 创建目标目录
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }

            # 复制关键文件
            $keyFiles = @("metrics_summary.json", "config.json")
            foreach ($file in $keyFiles) {
                $src = Join-Path $sourceOutDir $file
                if (Test-Path $src) {
                    Copy-Item $src $destDir -Force
                }
            }

            # 保存实验记录
            $recordFile = Join-Path $destDir "experiment_record.txt"
            $recordContent = @"
实验编号: $ExpId
实验标签: $ExpLabel
人员: Person $Person
运行时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
耗时: $($duration.ToString('F1')) 分钟
参数:
  seed: $Seed
  seq_len: $SeqLen
  pre_len: $PreLen
  use_diffusion: $UseDiffusion
  use_pe_graph: $PEGraph
  use_pe_film: $PEFiLM
状态: 成功
源码输出目录: $sourceOutDir
"@
            $recordContent | Out-File -FilePath $recordFile -Encoding UTF8
        }

        Write-Host "    ✓ 完成 (耗时: $($duration.ToString('F1')) 分钟)" -ForegroundColor Green
        $SuccessCount++
    }
    catch {
        Write-Host "    ✗ 失败: $_" -ForegroundColor Red
        $FailCount++
        $FailedList += $ExpId

        # 记录失败信息
        $destDir = Join-Path $ResultDir $ExpId
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        $failFile = Join-Path $destDir "FAILURE_LOG.txt"
        @"
实验编号: $ExpId
实验标签: $ExpLabel
失败时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
错误信息: $_
参数:
  seed: $Seed
  seq_len: $SeqLen
  pre_len: $PreLen
  use_diffusion: $UseDiffusion
  use_pe_graph: $PEGraph
  use_pe_film: $PEFiLM
"@ | Out-File -FilePath $failFile -Encoding UTF8
    }
}

# 汇总报告
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Person $Person 实验完成" -ForegroundColor Cyan
Write-Host "  成功: $SuccessCount / $TotalExperiments" -ForegroundColor Green
if ($FailCount -gt 0) {
    Write-Host "  失败: $FailCount / $TotalExperiments" -ForegroundColor Red
    Write-Host "  失败列表: $($FailedList -join ', ')" -ForegroundColor Red
}
Write-Host "  结果目录: $ResultDir" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# 生成简要汇总
$summaryFile = Join-Path $ResultDir "person_${Person}_summary.csv"
@"
exp_id,seed,seq_len,pre_len,use_diffusion,use_pe_graph,use_pe_film,status,test_rmse,test_mae,test_mape,best_epoch
"@ | Out-File -FilePath $summaryFile -Encoding UTF8

for ($i = 0; $i -lt $TotalExperiments; $i++) {
    $exp = $Experiments[$i]
    $ExpNum = $i + 1
    $ExpId = "{0}{1:D2}" -f $Person, $ExpNum
    $destDir = Join-Path $ResultDir $ExpId
    $metricsFile = Join-Path $destDir "metrics_summary.json"

    if (Test-Path $metricsFile) {
        $metrics = Get-Content $metricsFile | ConvertFrom-Json
        $status = "success"
        $rmse = $metrics.test_rmse
        $mae = $metrics.test_mae
        $mape = $metrics.test_mape
        $bestEpoch = $metrics.best_epoch
    } else {
        $status = "failed"
        $rmse = ""
        $mae = ""
        $mape = ""
        $bestEpoch = ""
    }

    "$ExpId,$($exp[0]),$($exp[1]),$UseDiffusion,$($exp[2]),$($exp[3]),$status,$rmse,$mae,$mape,$bestEpoch" | Out-File -FilePath $summaryFile -Encoding UTF8 -Append
}

Write-Host ""
Write-Host "汇总文件已保存: $summaryFile" -ForegroundColor Green