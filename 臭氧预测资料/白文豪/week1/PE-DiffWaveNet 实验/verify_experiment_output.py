#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify PE-DiffWaveNet experiment output."""

import argparse
import json
import os
import numpy as np


def check_output_dirs(args):
    out_dir = os.path.join(args.data_dir, f"matrix_N95_PEDiffWaveNet_noleak_{args.exp_name}")
    weight_dir = os.path.join(args.data_dir, f"weights_N95/weights_pediffwavenet_noleak_{args.exp_name}")
    
    print("="*60)
    print("PE-DiffWaveNet 实验输出检查")
    print("="*60)
    
    print(f"\n1. 输出目录: {out_dir}")
    if os.path.exists(out_dir):
        print("   ✓ 目录存在")
        files = sorted(os.listdir(out_dir))
        print(f"   文件数量: {len(files)}")
        print(f"   文件列表:")
        for f in files[:20]:
            size = os.path.getsize(os.path.join(out_dir, f)) / 1024 / 1024
            print(f"     - {f} ({size:.2f} MB)")
        if len(files) > 20:
            print(f"     ... 还有 {len(files) - 20} 个文件")
    else:
        print("   ✗ 目录不存在")
        return False
    
    print(f"\n2. 权重目录: {weight_dir}")
    if os.path.exists(weight_dir):
        print("   ✓ 目录存在")
        files = sorted(os.listdir(weight_dir))
        print(f"   文件列表: {files}")
    else:
        print("   ✗ 目录不存在")
    
    print(f"\n3. metrics_summary.json 检查")
    metrics_path = os.path.join(out_dir, "metrics_summary.json")
    if os.path.exists(metrics_path):
        print("   ✓ 文件存在")
        with open(metrics_path, 'r', encoding='utf-8') as f:
            metrics = json.load(f)
        print("   内容摘要:")
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                print(f"     {key}: {value}")
            elif isinstance(value, list) and len(value) <= 10:
                print(f"     {key}: {value}")
            else:
                print(f"     {key}: {type(value).__name__}")
    else:
        print("   ✗ 文件不存在")
    
    print(f"\n4. config.json 检查")
    config_path = os.path.join(out_dir, "config.json")
    if os.path.exists(config_path):
        print("   ✓ 文件存在")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("   关键配置:")
        keys_to_show = ['seq_len', 'pre_len', 'hidden_size', 'N_node', 'm', 
                        'diff_steps', 'epochs', 'seed', 'exp_name']
        for key in keys_to_show:
            if key in config:
                print(f"     {key}: {config[key]}")
    else:
        print("   ✗ 文件不存在")
    
    print(f"\n5. 训练曲线检查")
    train_loss_path = os.path.join(out_dir, "train_loss.npy")
    if os.path.exists(train_loss_path):
        print("   ✓ 文件存在")
        train_loss = np.load(train_loss_path)
        print(f"     训练损失形状: {train_loss.shape}")
        print(f"     训练损失范围: {train_loss.min():.6f} ~ {train_loss.max():.6f}")
        print(f"     训练损失均值: {train_loss.mean():.6f}")
    else:
        print("   ✗ 文件不存在")
    
    print(f"\n6. 验证指标检查")
    valid_mae_path = os.path.join(out_dir, "valid_mae.npy")
    valid_rmse_path = os.path.join(out_dir, "valid_rmse.npy")
    if os.path.exists(valid_mae_path):
        print("   ✓ valid_mae.npy 存在")
        valid_mae = np.load(valid_mae_path)
        print(f"     验证 MAE: {valid_mae}")
    else:
        print("   ✗ valid_mae.npy 不存在")
    
    if os.path.exists(valid_rmse_path):
        print("   ✓ valid_rmse.npy 存在")
        valid_rmse = np.load(valid_rmse_path)
        print(f"     验证 RMSE: {valid_rmse}")
    else:
        print("   ✗ valid_rmse.npy 不存在")
    
    print(f"\n7. 数据数组检查")
    for fname in ['testX.npy', 'testY.npy', 'S_matrix.npy', 'T_matrix.npy', 
                  'PE_matrix.npy', 'pe_node_features.npy']:
        fpath = os.path.join(out_dir, fname)
        if os.path.exists(fpath):
            arr = np.load(fpath)
            print(f"   ✓ {fname}: shape={arr.shape}, dtype={arr.dtype}")
        else:
            print(f"   ✗ {fname}: 不存在")
    
    print("\n" + "="*60)
    print("检查完成！")
    print("="*60)
    return True


def parse_args():
    parser = argparse.ArgumentParser(description='Verify PE-DiffWaveNet experiment output')
    parser.add_argument('--data_dir', type=str, default='/mnt/d/时空数据/臭氧预测资料',
                        help='Path to data directory')
    parser.add_argument('--exp_name', type=str, default='student_smoke_gpu',
                        help='Experiment name suffix')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    check_output_dirs(args)