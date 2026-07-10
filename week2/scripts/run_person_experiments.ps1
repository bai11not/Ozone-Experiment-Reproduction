# run_person_experiments.ps1
# 批量运行指定人员的全部 8 组消融实验
#
# 用法:
#   .\run_person_experiments.ps1 -Person A
#   .\run_person_experiments.ps1 -Person A -StartFrom 3
#   .\run_person_experiments.ps1 -Person A -DryRun

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

# 人员配置: seed + 2 个消融类型 (name, d, g, f)
$PersonConfig = @{
    "A" = @{
        Seed = 42
        Types = @( @("full", 1, 1, 1), @("no_diff", 0, 1, 1) )
        Dir = "person_A_seed42_full_nodiff"
    }
    "B" = @{
        Seed = 42
        Types = @( @("no_graph", 1, 0, 1), @("no_film", 1, 1, 0) )
        Dir = "person_B_seed42_nograph_nofilm"
    }
    "C" = @{
        Seed = 52
        Types = @( @("full", 1, 1, 1), @("no_diff", 0, 1, 1) )
        Dir = "person_C_seed52_full_nodiff"
    }
    "D" = @{
        Seed = 52
        Types = @( @("no_graph", 1, 0, 1), @("no_film", 1, 1, 0) )
        Dir = "person_D_seed52_nograph_nofilm"
    }
}

$cfg = $PersonConfig[$Person]
$Seed = $cfg.Seed
$ResultDir = Join-Path $PSScriptRoot ".." "results" $cfg.Dir

# 构建 8 组实验: 2 类型 × 2 seq_len × 2 pre_len
$Experiments = @()
foreach ($type in $cfg.Types) {
    foreach ($seq in @(12, 24)) {
        foreach ($pre in @(6, 3)) {
            $Experiments += @{
                AblName = $type[0]
                D = $type[1]
                G = $type[2]
                F = $type[3]
                SeqLen = $seq
                PreLen = $pre
            }
        }
    }
}

$Total = $Experiments.Count
$SuccessCount = 0
$FailCount = 0
$FailedList = @()

if (-not (Test-Path $ResultDir)) {
    New-Item -ItemType Directory -Path $ResultDir -Force | Out-Null
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  消融实验: Person $Person" -ForegroundColor Cyan
Write-Host "  Seed: $Seed" -ForegroundColor Cyan
Write-Host "  共 $Total 组实验" -ForegroundColor Cyan
if ($DryRun) { Write-Host "  [DRY RUN]" -ForegroundColor Yellow }
Write-Host "========================================" -ForegroundColor Cyan

for ($i = $StartFrom - 1; $i -lt $Total; $i++) {
    $exp = $Experiments[$i]
    $ExpNum = $i + 1
    $ExpId = "{0}{1:D2}" -f $Person, $ExpNum
    $ExpLabel = "s{0}-{1}-l{2}-p{3}" -f $Seed, $exp.AblName, $exp.SeqLen, $exp.PreLen
    $ExpName = "{0}_{1}" -f $ExpId, $ExpLabel

    Write-Host ""
    Write-Host "--- 实验 $ExpNum / $Total : $ExpId ($ExpLabel) ---" -ForegroundColor Yellow

    if ($DryRun) {
        Write-Host "    [DRY RUN] seed=$Seed ablation=$($exp.AblName) seq=$($exp.SeqLen) pre=$($exp.PreLen)"
        $SuccessCount++
        continue
    }

    try {
        $startTime = Get-Date
        $scriptPath = Join-Path $PSScriptRoot "run_single_experiment.ps1"
        & $scriptPath `
            -Seed $Seed -SeqLen $exp.SeqLen -PreLen $exp.PreLen `
            -UseDiffusion $exp.D -UsePEGraph $exp.G -UsePEFiLM $exp.F `
            -ExpName $ExpName -DataDir $DataDir -Device $Device

        $duration = ((Get-Date) - $startTime).TotalMinutes

        $srcDir = "$DataDir\matrix_N95_PEDiffWaveNet_noleak_$ExpName"
        $destDir = Join-Path $ResultDir $ExpId
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        foreach ($f in @("metrics_summary.json", "config.json")) {
            $src = Join-Path $srcDir $f
            if (Test-Path $src) { Copy-Item $src $destDir -Force }
        }

        $SuccessCount++
        Write-Host "    ✓ 完成" -ForegroundColor Green
    } catch {
        $FailCount++
        $FailedList += $ExpId
        Write-Host "    ✗ 失败: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Person $Person 完成: 成功 $SuccessCount / $Total" -ForegroundColor Green
if ($FailCount -gt 0) {
    Write-Host "  失败: $FailCount ($($FailedList -join ', '))" -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Cyan