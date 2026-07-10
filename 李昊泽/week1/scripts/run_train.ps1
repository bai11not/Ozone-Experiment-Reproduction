# PE-DiffWaveNet 正式训练 — Windows PowerShell
#
# 用法：
#   .\scripts\run_train.ps1                    # 默认: pre_len=6, seq_len=24, seed=42
#   .\scripts\run_train.ps1 6 24 52            # 指定 pre_len, seq_len, seed
#
# 环境变量覆盖（可选）：
#   $env:DEVICE="cpu"; .\scripts\run_train.ps1  # CPU 训练
#   $env:EPOCHS="60"; .\scripts\run_train.ps1   # 只跑 60 轮
#   $env:EXP_NAME="my_exp"; .\scripts\run_train.ps1  # 自定义实验名
#
# 常用组合：
#   # Smoke 级别快速验证（CPU）
#   $env:DEVICE="cpu"; $env:EPOCHS="1"; $env:HIDDEN_SIZE="16"; $env:MAX_TRAIN_WINDOWS="8"; .\scripts\run_train.ps1
#
#   # GPU 小配置 debug
#   $env:EPOCHS="3"; $env:HIDDEN_SIZE="16"; $env:MAX_TRAIN_WINDOWS="64"; .\scripts\run_train.ps1
#
#   # 消融: 去掉扩散
#   $env:USE_DIFFUSION="0"; $env:EXP_NAME="ablation_no_diff"; .\scripts\run_train.ps1
#
#   # 消融: 去掉 PE
#   $env:USE_PE_GRAPH="0"; $env:USE_PE_FILM="0"; $env:EXP_NAME="ablation_no_pe"; .\scripts\run_train.ps1

param(
    [int]$PreLen = 6,
    [int]$SeqLen = 24,
    [int]$Seed = 42
)

$ROOT = (Resolve-Path "$PSScriptRoot\..").Path
$env:PYTHONPATH = "$ROOT\code"

# 可被环境变量覆盖的默认值
$DEVICE       = if ($env:DEVICE)       { $env:DEVICE }       else { "cuda" }
$EXP_NAME     = if ($env:EXP_NAME)     { $env:EXP_NAME }     else { "pedw_p${PreLen}_l${SeqLen}_s${Seed}" }
$EPOCHS       = if ($env:EPOCHS)       { $env:EPOCHS }       else { "120" }
$HIDDEN_SIZE  = if ($env:HIDDEN_SIZE)  { $env:HIDDEN_SIZE }  else { "64" }
$BATCH_SIZE   = if ($env:BATCH_SIZE)   { $env:BATCH_SIZE }   else { "16" }
$LR           = if ($env:LR)           { $env:LR }           else { "7e-4" }
$PATIENCE     = if ($env:PATIENCE)     { $env:PATIENCE }     else { "15" }

$DIFF_STEPS       = if ($env:DIFF_STEPS)       { $env:DIFF_STEPS }       else { "50" }
$INFERENCE_STEPS  = if ($env:INFERENCE_STEPS)  { $env:INFERENCE_STEPS }  else { "50" }
$NUM_SAMPLES      = if ($env:NUM_SAMPLES)      { $env:NUM_SAMPLES }      else { "3" }

$USE_DIFFUSION  = if ($env:USE_DIFFUSION)  { $env:USE_DIFFUSION }  else { "1" }
$USE_PE_GRAPH   = if ($env:USE_PE_GRAPH)   { $env:USE_PE_GRAPH }   else { "1" }
$USE_PE_FILM    = if ($env:USE_PE_FILM)    { $env:USE_PE_FILM }    else { "1" }
$PE_SHUFFLE_SEED = if ($env:PE_SHUFFLE_SEED) { $env:PE_SHUFFLE_SEED } else { "-1" }

$AMP            = if ($env:AMP)            { $env:AMP }            else { "1" }
$MAX_TRAIN_WINDOWS  = if ($env:MAX_TRAIN_WINDOWS)  { $env:MAX_TRAIN_WINDOWS }  else { "0" }
$MAX_VALID_WINDOWS  = if ($env:MAX_VALID_WINDOWS)  { $env:MAX_VALID_WINDOWS }  else { "0" }
$MAX_TEST_WINDOWS   = if ($env:MAX_TEST_WINDOWS)   { $env:MAX_TEST_WINDOWS }   else { "0" }
$LOG_INTERVAL   = if ($env:LOG_INTERVAL)   { $env:LOG_INTERVAL }   else { "50" }

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "PE-DiffWaveNet Training" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  pre_len=$PreLen, seq_len=$SeqLen, seed=$Seed"
Write-Host "  device=$DEVICE, epochs=$EPOCHS, hidden_size=$HIDDEN_SIZE"
Write-Host "  exp_name=$EXP_NAME"
Write-Host "============================================" -ForegroundColor Cyan

python -u "$ROOT\code\train_pediffwavenet_noleak.py" `
  --data_dir "$ROOT" `
  --device "$DEVICE" `
  --exp_name "$EXP_NAME" `
  --pre_len "$PreLen" `
  --seq_len "$SeqLen" `
  --seed "$Seed" `
  --hidden_size "$HIDDEN_SIZE" `
  --batch_size "$BATCH_SIZE" `
  --eval_batch_size "$BATCH_SIZE" `
  --lr "$LR" `
  --epochs "$EPOCHS" `
  --patience "$PATIENCE" `
  --diff_steps "$DIFF_STEPS" `
  --inference_steps "$INFERENCE_STEPS" `
  --num_samples "$NUM_SAMPLES" `
  --use_diffusion "$USE_DIFFUSION" `
  --use_pe_graph "$USE_PE_GRAPH" `
  --use_pe_film "$USE_PE_FILM" `
  --pe_shuffle_seed "$PE_SHUFFLE_SEED" `
  --max_train_windows "$MAX_TRAIN_WINDOWS" `
  --max_valid_windows "$MAX_VALID_WINDOWS" `
  --max_test_windows "$MAX_TEST_WINDOWS" `
  --amp "$AMP" `
  --log_interval "$LOG_INTERVAL"
