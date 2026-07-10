#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""查看训练结果 — 中文版 — 自动生成中文曲线图和散点图。"""

import numpy as np, json, os, sys, glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def list_experiments():
    pattern = os.path.join(PROJECT_DIR, 'matrix_N95_PEDiffWaveNet_noleak_*')
    dirs = sorted(glob.glob(pattern))
    if not dirs:
        print('未找到任何实验。')
        return
    print('可查看的实验:')
    for d in dirs:
        name = os.path.basename(d).replace('matrix_N95_PEDiffWaveNet_noleak_', '') or '(默认, 无exp_name)'
        print(f'  {name}')


def view_experiment(exp_name):
    out_dir = os.path.join(PROJECT_DIR, f'matrix_N95_PEDiffWaveNet_noleak_{exp_name}')
    if not os.path.isdir(out_dir):
        print(f'[错误] 未找到实验: {exp_name}')
        list_experiments()
        sys.exit(1)

    print(f'=== 实验结果: {exp_name} ===')
    print(f'目录: {out_dir}')

    metrics_file = os.path.join(out_dir, 'metrics_summary.json')
    if os.path.exists(metrics_file):
        with open(metrics_file, encoding='utf-8') as f:
            m = json.load(f)
        print(f'\n--- 评估指标 ---')
        labels = {
            'test_rmse': '测试RMSE', 'test_mae': '测试MAE', 'test_mape': '测试MAPE(%)',
            'best_epoch': '最佳轮次', 'best_valid_rmse': '最佳验证RMSE',
            'best_valid_mae': '最佳验证MAE', 'best_valid_mape': '最佳验证MAPE(%)',
            'use_diffusion': '使用扩散', 'use_pe_graph': '使用PE图', 'use_pe_film': '使用PE-FiLM',
        }
        for key, label in labels.items():
            if key in m:
                val = m[key]
                s = f'{val:.4f}' if isinstance(val, float) else str(val)
                print(f'  {label:18s}: {s}')
        if 'per_step_rmse' in m:
            print(f'\n  逐步误差:')
            print(f'  {"步数":>4}  {"RMSE":>10}  {"MAE":>10}')
            for i, (r, a) in enumerate(zip(m['per_step_rmse'], m.get('per_step_mae', [0]*len(m['per_step_rmse']))), 1):
                print(f'  {i:>4}  {r:>10.4f}  {a:>10.4f}')

    print(f'\n--- .npy 文件 ---')
    for f in sorted(os.listdir(out_dir)):
        if f.endswith('.npy'):
            path = os.path.join(out_dir, f)
            arr = np.load(path)
            print(f'  {f:30s}  形状={str(arr.shape):20s}  范围=[{arr.min():.4f}, {arr.max():.4f}]')

    # ---- 画图 ----
    fig_dir = os.path.join(out_dir, 'figures')
    os.makedirs(fig_dir, exist_ok=True)
    has_curves = False

    train_loss_path = os.path.join(out_dir, 'train_loss.npy')
    valid_rmse_path = os.path.join(out_dir, 'valid_rmse.npy')
    valid_mae_path = os.path.join(out_dir, 'valid_mae.npy')

    if os.path.exists(train_loss_path) and os.path.exists(valid_rmse_path):
        train_loss = np.load(train_loss_path)
        valid_rmse = np.load(valid_rmse_path)
        if len(train_loss) > 1:
            has_curves = True
            ncols = 3 if os.path.exists(valid_mae_path) else 2
            fig, axes = plt.subplots(1, ncols, figsize=(5*ncols, 4))
            if ncols == 2:
                axes = [axes[0], axes[1], None]

            axes[0].plot(train_loss, 'b-', linewidth=1.5)
            axes[0].set_title('训练损失', fontsize=13, fontweight='bold')
            axes[0].set_xlabel('轮次 (Epoch)')
            axes[0].set_ylabel('损失值')
            axes[0].grid(True, alpha=0.3)

            axes[1].plot(valid_rmse, 'r-', linewidth=1.5)
            axes[1].set_title('验证RMSE', fontsize=13, fontweight='bold')
            axes[1].set_xlabel('轮次 (Epoch)')
            axes[1].set_ylabel('RMSE')
            axes[1].grid(True, alpha=0.3)

            if ncols == 3 and os.path.exists(valid_mae_path):
                valid_mae = np.load(valid_mae_path)
                axes[2].plot(valid_mae, 'g-', linewidth=1.5)
                axes[2].set_title('验证MAE', fontsize=13, fontweight='bold')
                axes[2].set_xlabel('轮次 (Epoch)')
                axes[2].set_ylabel('MAE')
                axes[2].grid(True, alpha=0.3)

            plt.tight_layout()
            save_path = os.path.join(fig_dir, 'training_curves.png')
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
            print(f'\n已保存: {save_path}')

    test_preds_path = os.path.join(out_dir, 'test_predictions.npy')
    test_targets_path = os.path.join(out_dir, 'test_targets.npy')
    if os.path.exists(test_preds_path) and os.path.exists(test_targets_path):
        has_curves = True
        preds = np.load(test_preds_path)
        targets = np.load(test_targets_path)
        n_nodes = preds.shape[2] if preds.ndim == 3 else preds.shape[1]
        sample_nodes = np.random.choice(min(n_nodes, 95), size=min(6, n_nodes), replace=False)

        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        for idx, node in enumerate(sample_nodes):
            ax = axes[idx // 3, idx % 3]
            p = preds[:, :, node].flatten() if preds.ndim == 3 else preds[:, node].flatten()
            t = targets[:, :, node].flatten() if targets.ndim == 3 else targets[:, node].flatten()
            ax.scatter(t, p, alpha=0.3, s=10, color='steelblue')
            lim = [min(t.min(), p.min()), max(t.max(), p.max())]
            ax.plot(lim, lim, 'r--', linewidth=1)
            ax.set_xlabel('真实值')
            ax.set_ylabel('预测值')
            ax.set_title(f'站点 {node}')
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        save_path = os.path.join(fig_dir, 'predictions.png')
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f'已保存: {save_path}')

    if not has_curves:
        print('\n(仅1个epoch，无训练曲线可画)')

    print('\n完成。')


if __name__ == '__main__':
    if '--list' in sys.argv or '-l' in sys.argv:
        list_experiments()
    else:
        exp = sys.argv[1] if len(sys.argv) > 1 else 'student_smoke_cpu'
        view_experiment(exp)
