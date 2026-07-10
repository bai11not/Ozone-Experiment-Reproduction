# run_single_experiment.ps1
# 运行单组 PE-DiffWaveNet 实验
#
# 用法:
#   .\run_single_experiment.ps1 -Seed 42 -SeqLen 12 -PreLen 6 -UseDiffusion 0 -UsePEGraph 0 -UsePEFiLM 0 -ExpName "A01_s42-d0-l12-p6-g0-f0"
#
# 参数说明:
#   -Seed          随机种子 (42 或 52)
#   -SeqLen        输入窗口长度 (12 或 24)
#   -PreLen        预测步长 (6 或 3)
#   -UseDiffusion  是否使用扩散 (0 或 1)
#   -UsePEGraph    是否使用 PE 图 (0 或 1)
#   -UsePEFiLM     是否使用 PE FiLM (0 或 1)
#   -ExpName       实验名称标签
#   -DataDir       数据目录 (默认: d:\时空数据\臭氧预测资料)
#   -Device        设备 (默认: cuda)

param(
    [Parameter(Mandatory=$true)] [int] $Seed,
    [Parameter(Mandatory=$true)] [int] $SeqLen,
    [Parameter(Mandatory=$true)] [int] $PreLen,
    [Parameter(Mandatory=$true)] [int] $UseDiffusion,
    [Parameter(Mandatory=$true)] [int] $UsePEGraph,
    [Parameter(Mandatory=$true)] [int] $UsePEFiLM,
    [Parameter(Mandatory=$true)] [string] $ExpName,
    [string] $DataDir = "d:\时空数据\臭氧预测资料",
    [string] $Device = "cuda"
)

$ErrorActionPreference = "Stop"

# 设置 PYTHONPATH
$env:PYTHONPATH = "$DataDir\code;$env:PYTHONPATH"

# 代码路径
$TrainScript = "$DataDir\code\train_pediffwavenet_noleak.py"

# 检查训练脚本是否存在
if (-not (Test-Path $TrainScript)) {
    Write-Error "训练脚本不存在: $TrainScript"
    exit 1
}

# 构建 horizon_weights (根据 pre_len 自动生成均匀权重)
$HorizonWeights = (1..$PreLen | ForEach-Object { "1.0" }) -join ","

# 固定参数
$NNode = 95
$InputDim = 15
$HiddenSize = 64
$BatchSize = 16
$EvalBatchSize = 16
$LR = "7e-4"
$LRMin = "1e-5"
$Epochs = 120
$Patience = 15
$MinDelta = "0.001"
$DiffSteps = 50
$InferenceSteps = 50
$NumSamples = 3
$TStartRatio = "0.25"
$CoarseWeight = "0.08"
$UseAdaptiveAdj = 1
$PESource = "train"
$PEScales = "6,9,12,24,48,72"
$PEDim = 3
$PEDelay = 1
$PEWindowStep = 1
$PEGraphAlpha = "1.0"
$PEFiLMScale = "1.0"
$PEFiLMZeroInit = 0
$NormalizePEFeatures = 1
$Amp = 1
$GradClip = "1.0"
$WeightDecay = "1e-4"
$LogInterval = 50
$SavePredictions = 1
$UseMetCache = 1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " PE-DiffWaveNet 单次实验" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  实验名称:     $ExpName" -ForegroundColor Yellow
Write-Host "  Seed:         $Seed" -ForegroundColor Yellow
Write-Host "  Seq Len:      $SeqLen" -ForegroundColor Yellow
Write-Host "  Pre Len:      $PreLen" -ForegroundColor Yellow
Write-Host "  UseDiffusion: $UseDiffusion" -ForegroundColor Yellow
Write-Host "  UsePEGraph:   $UsePEGraph" -ForegroundColor Yellow
Write-Host "  UsePEFiLM:    $UsePEFiLM" -ForegroundColor Yellow
Write-Host "  Device:       $Device" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 记录开始时间
$StartTime = Get-Date
Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] 开始训练..." -ForegroundColor Green

# 构建命令行参数
$ArgsList = @(
    "-u", $TrainScript,
    "--data_dir", $DataDir,
    "--device", $Device,
    "--exp_name", $ExpName,
    "--seed", $Seed,
    "--seq_len", $SeqLen,
    "--pre_len", $PreLen,
    "--use_diffusion", $UseDiffusion,
    "--use_pe_graph", $UsePEGraph,
    "--use_pe_film", $UsePEFiLM,
    "--N_node", $NNode,
    "--m", $InputDim,
    "--hidden_size", $HiddenSize,
    "--batch_size", $BatchSize,
    "--eval_batch_size", $EvalBatchSize,
    "--lr", $LR,
    "--lr_min", $LRMin,
    "--epochs", $Epochs,
    "--patience", $Patience,
    "--min_delta", $MinDelta,
    "--diff_steps", $DiffSteps,
    "--inference_steps", $InferenceSteps,
    "--num_samples", $NumSamples,
    "--t_start_ratio", $TStartRatio,
    "--coarse_weight", $CoarseWeight,
    "--horizon_weights", $HorizonWeights,
    "--use_adaptive_adj", $UseAdaptiveAdj,
    "--pe_source", $PESource,
    "--pe_scales", $PEScales,
    "--pe_dim", $PEDim,
    "--pe_delay", $PEDelay,
    "--pe_window_step", $PEWindowStep,
    "--pe_graph_alpha", $PEGraphAlpha,
    "--pe_film_scale", $PEFiLMScale,
    "--pe_film_zero_init", $PEFiLMZeroInit,
    "--normalize_pe_features", $NormalizePEFeatures,
    "--amp", $Amp,
    "--grad_clip", $GradClip,
    "--weight_decay", $WeightDecay,
    "--log_interval", $LogInterval,
    "--save_predictions", $SavePredictions,
    "--use_met_cache", $UseMetCache
)

try {
    # 运行训练
    $process = Start-Process -FilePath "python" -ArgumentList $ArgsList -NoNewWindow -PassThru -Wait

    $EndTime = Get-Date
    $Duration = $EndTime - $StartTime

    if ($process.ExitCode -eq 0) {
        Write-Host ""
        Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] 训练完成! 耗时: $($Duration.TotalMinutes.ToString('F1')) 分钟" -ForegroundColor Green

        # 检查输出文件
        $OutDir = "$DataDir\matrix_N95_PEDiffWaveNet_noleak_$ExpName"
        $MetricsFile = "$OutDir\metrics_summary.json"

        if (Test-Path $MetricsFile) {
            Write-Host ""
            Write-Host "========== 实验结果 ==========" -ForegroundColor Cyan
            Get-Content $MetricsFile | ConvertFrom-Json | ForEach-Object {
                Write-Host "  Test RMSE: $($_.test_rmse)" -ForegroundColor White
                Write-Host "  Test MAE:  $($_.test_mae)" -ForegroundColor White
                Write-Host "  Test MAPE: $($_.test_mape)%" -ForegroundColor White
                Write-Host "  Best Epoch: $($_.best_epoch)" -ForegroundColor White
            }
            Write-Host "==============================" -ForegroundColor Cyan
            Write-Host "  输出目录: $OutDir" -ForegroundColor Yellow
        } else {
            Write-Warning "未找到 metrics_summary.json，请检查输出目录"
        }
    } else {
        Write-Host ""
        Write-Error "训练失败! 退出码: $($process.ExitCode)"
        exit $process.ExitCode
    }
} catch {
    Write-Error "运行出错: $_"
    exit 1
}