#!/usr/bin/env python
"""查看训练结果：指标、训练曲线、预测对比图。

用法:
    python scripts/view_results.py student_smoke_cpu       # 指定实验名
    python scripts/view_results.py                         # 默认 student_smoke_cpu
    python scripts/view_results.py --list                  # 列出所有实验
"""
import numpy as np
import json
import os
import sys
import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def list_experiments():
    pattern = os.path.join(PROJECT_DIR, 'matrix_N95_PEDiffWaveNet_noleak_*')
    dirs = sorted(glob.glob(pattern))
    if not dirs:
        print('No experiments found.')
        return
    print('Available experiments:')
    for d in dirs:
        name = os.path.basename(d).replace('matrix_N95_PEDiffWaveNet_noleak_', '')
        if not name:
            name = '(default, no exp_name)'
        print(f'  {name}')


def view_experiment(exp_name):
    out_dir = os.path.join(PROJECT_DIR, f'matrix_N95_PEDiffWaveNet_noleak_{exp_name}')
    if not os.path.isdir(out_dir):
        print(f'[ERROR] Experiment not found: {exp_name}')
        print()
        list_experiments()
        sys.exit(1)

    print(f'=== Results: {exp_name} ===')
    print(f'Directory: {out_dir}')

    # ---- Metrics ----
    metrics_file = os.path.join(out_dir, 'metrics_summary.json')
    if os.path.exists(metrics_file):
        with open(metrics_file) as f:
            m = json.load(f)
        print(f'\n--- Metrics ---')
        for key in ['test_rmse', 'test_mae', 'test_mape', 'best_epoch',
                     'best_valid_rmse', 'best_valid_mae', 'best_valid_mape',
                     'use_diffusion', 'use_pe_graph', 'use_pe_film']:
            if key in m:
                val = m[key]
                if isinstance(val, float):
                    print(f'  {key:25s}: {val:.4f}')
                else:
                    print(f'  {key:25s}: {val}')
        if 'per_step_rmse' in m:
            print(f'\n  Per-step:')
            for i, (r, a) in enumerate(zip(m['per_step_rmse'],
                                            m.get('per_step_mae', [''] * len(m['per_step_rmse']))), 1):
                print(f'    Step {i}:  RMSE={r:.4f}  MAE={a:.4f}')

    # ---- .npy files ----
    print(f'\n--- .npy files ---')
    for f in sorted(os.listdir(out_dir)):
        if f.endswith('.npy'):
            path = os.path.join(out_dir, f)
            arr = np.load(path)
            print(f'  {f:30s}  shape={str(arr.shape):20s}  dtype={str(arr.dtype):10s}  range=[{arr.min():.4f}, {arr.max():.4f}]')

    # ---- Plots ----
    fig_dir = os.path.join(out_dir, 'figures')
    os.makedirs(fig_dir, exist_ok=True)
    has_curves = False

    # Training curves
    train_loss_path = os.path.join(out_dir, 'train_loss.npy')
    valid_rmse_path = os.path.join(out_dir, 'valid_rmse.npy')
    valid_mae_path = os.path.join(out_dir, 'valid_mae.npy')

    if os.path.exists(train_loss_path) and os.path.exists(valid_rmse_path):
        train_loss = np.load(train_loss_path)
        valid_rmse = np.load(valid_rmse_path)

        if len(train_loss) > 1:  # Only plot if more than 1 epoch
            has_curves = True
            ncols = 3 if os.path.exists(valid_mae_path) else 2
            fig, axes = plt.subplots(1, ncols, figsize=(5 * ncols, 4))
            if ncols == 2:
                axes = [axes[0], axes[1], None]

            axes[0].plot(train_loss, 'b-', linewidth=1)
            axes[0].set_title('Training Loss')
            axes[0].set_xlabel('Epoch')
            axes[0].grid(True, alpha=0.3)

            axes[1].plot(valid_rmse, 'r-', linewidth=1)
            axes[1].set_title('Validation RMSE')
            axes[1].set_xlabel('Epoch')
            axes[1].grid(True, alpha=0.3)

            if ncols == 3 and os.path.exists(valid_mae_path):
                valid_mae = np.load(valid_mae_path)
                axes[2].plot(valid_mae, 'g-', linewidth=1)
                axes[2].set_title('Validation MAE')
                axes[2].set_xlabel('Epoch')
                axes[2].grid(True, alpha=0.3)

            plt.tight_layout()
            save_path = os.path.join(fig_dir, 'training_curves.png')
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
            print(f'\nSaved: {save_path}')

    # Prediction scatter
    test_preds_path = os.path.join(out_dir, 'test_predictions.npy')
    test_targets_path = os.path.join(out_dir, 'test_targets.npy')

    if os.path.exists(test_preds_path) and os.path.exists(test_targets_path):
        has_curves = True
        preds = np.load(test_preds_path)
        targets = np.load(test_targets_path)
        print(f'Predictions shape: {preds.shape}, Targets shape: {targets.shape}')

        if preds.ndim == 3:
            n_nodes = preds.shape[2]
        else:
            n_nodes = preds.shape[1]

        sample_nodes = np.random.choice(min(n_nodes, 95), size=min(6, n_nodes), replace=False)

        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        for idx, node in enumerate(sample_nodes):
            ax = axes[idx // 3, idx % 3]
            if preds.ndim == 3:
                p = preds[:, :, node].flatten()
                t = targets[:, :, node].flatten()
            else:
                p = preds[:, node].flatten()
                t = targets[:, node].flatten()

            ax.scatter(t, p, alpha=0.3, s=10)
            lim = [min(t.min(), p.min()), max(t.max(), p.max())]
            ax.plot(lim, lim, 'r--', linewidth=1)
            ax.set_xlabel('True')
            ax.set_ylabel('Predicted')
            ax.set_title(f'Station {node}')
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        save_path = os.path.join(fig_dir, 'predictions.png')
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f'Saved: {save_path}')

    if not has_curves:
        print('\n(Only 1 epoch — no meaningful curves to plot)')

    print('\nDone.')


if __name__ == '__main__':
    if '--list' in sys.argv or '-l' in sys.argv:
        list_experiments()
    else:
        exp = sys.argv[1] if len(sys.argv) > 1 else 'student_smoke_cpu'
        view_experiment(exp)
