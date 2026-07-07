#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Baseline evaluation script for O3 prediction.

Baselines implemented:
1. Persistence (last observed value)
2. Historical Mean (mean of input sequence)
3. Simple GRU baseline
4. Linear regression baseline

Metrics: RMSE, MAE, MAPE, Peak_RMSE, Step6_RMSE
"""

import argparse
import json
import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


def set_seed(seed=42):
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def compute_metrics(preds, targets, max_value=100.0):
    preds = np.asarray(preds)
    targets = np.asarray(targets)
    diff = preds - targets
    rmse = np.sqrt(np.mean(diff ** 2))
    mae = np.mean(np.abs(diff))
    mape = np.mean(np.abs(diff) / (np.abs(targets) + 1e-8)) * 100
    return rmse, mae, mape


def compute_peak_metrics(preds, targets, max_value=100.0, peak_percentile=90.0):
    preds = np.asarray(preds)
    targets = np.asarray(targets)
    flat_targets = targets.flatten()
    peak_threshold = np.percentile(flat_targets, peak_percentile)
    peak_mask = targets >= peak_threshold
    if np.sum(peak_mask) > 0:
        peak_diff = preds[peak_mask] - targets[peak_mask]
        peak_rmse = np.sqrt(np.mean(peak_diff ** 2))
    else:
        peak_rmse = np.nan
    return peak_rmse, peak_threshold


def persistence_baseline(testX):
    return np.repeat(testX[:, -1:, :], 6, axis=1)


def historical_mean_baseline(testX):
    mean_val = np.mean(testX, axis=1, keepdims=True)
    return np.repeat(mean_val, 6, axis=1)


class GRUBaseline(nn.Module):
    def __init__(self, input_dim=95, hidden_dim=64, output_steps=6):
        super().__init__()
        self.gru = nn.GRU(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_steps * input_dim)
        self.output_steps = output_steps
        self.input_dim = input_dim

    def forward(self, x):
        _, h_n = self.gru(x)
        out = self.fc(h_n.squeeze(0))
        return out.reshape(-1, self.output_steps, self.input_dim)


class LinearBaseline(nn.Module):
    def __init__(self, seq_len=12, pred_len=6, num_nodes=95):
        super().__init__()
        self.linear = nn.Linear(seq_len * num_nodes, pred_len * num_nodes)

    def forward(self, x):
        batch_size = x.shape[0]
        x_flat = x.reshape(batch_size, -1)
        out = self.linear(x_flat)
        return out.reshape(batch_size, 6, 95)


def train_baseline_model(model, trainX, trainY, validX, validY, epochs=50, lr=1e-3, device='cpu'):
    model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    train_dataset = TensorDataset(torch.Tensor(trainX), torch.Tensor(trainY))
    valid_dataset = TensorDataset(torch.Tensor(validX), torch.Tensor(validY))
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    valid_loader = DataLoader(valid_dataset, batch_size=32)
    
    best_valid_rmse = float('inf')
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            pred = model(x)
            loss = criterion(pred, y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * x.size(0)
        train_loss /= len(train_loader.dataset)
        
        model.eval()
        valid_loss = 0.0
        all_preds = []
        all_targets = []
        with torch.no_grad():
            for x, y in valid_loader:
                x, y = x.to(device), y.to(device)
                pred = model(x)
                valid_loss += criterion(pred, y).item() * x.size(0)
                all_preds.append(pred.cpu().numpy())
                all_targets.append(y.cpu().numpy())
        valid_loss /= len(valid_loader.dataset)
        valid_preds = np.concatenate(all_preds)
        valid_targets = np.concatenate(all_targets)
        valid_rmse = np.sqrt(np.mean((valid_preds - valid_targets) ** 2))
        
        if valid_rmse < best_valid_rmse:
            best_valid_rmse = valid_rmse
            torch.save(model.state_dict(), 'best_baseline.pt')
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.6f} | Valid RMSE: {valid_rmse:.4f}")
    
    model.load_state_dict(torch.load('best_baseline.pt', map_location=device))
    os.remove('best_baseline.pt')
    return model


def evaluate_baselines(args):
    data_dir = args.data_dir
    max_value = args.max_value
    
    trainX = np.load(os.path.join(data_dir, 'matrix_N95', 'trainX.npy')).astype(np.float32)
    trainY = np.load(os.path.join(data_dir, 'matrix_N95', 'trainY.npy')).astype(np.float32)
    validX = np.load(os.path.join(data_dir, 'matrix_N95', 'validX.npy')).astype(np.float32)
    validY = np.load(os.path.join(data_dir, 'matrix_N95', 'validY.npy')).astype(np.float32)
    testX = np.load(os.path.join(data_dir, 'matrix_N95', 'testX.npy')).astype(np.float32)
    testY = np.load(os.path.join(data_dir, 'matrix_N95', 'testY.npy')).astype(np.float32)
    
    print(f"Data shapes:")
    print(f"  trainX: {trainX.shape}, trainY: {trainY.shape}")
    print(f"  validX: {validX.shape}, validY: {validY.shape}")
    print(f"  testX: {testX.shape}, testY: {testY.shape}")
    
    results = []
    
    print("\n--- Persistence Baseline ---")
    preds_persistence = persistence_baseline(testX)
    rmse, mae, mape = compute_metrics(preds_persistence, testY, max_value)
    peak_rmse, _ = compute_peak_metrics(preds_persistence, testY, max_value)
    step6_rmse = np.sqrt(np.mean((preds_persistence[:, -1, :] - testY[:, -1, :]) ** 2))
    results.append({
        'Method': 'Persistence (L=12)',
        'RMSE': rmse,
        'MAE': mae,
        'MAPE': mape,
        'Peak_RMSE': peak_rmse,
        'Step6_RMSE': step6_rmse
    })
    print(f"RMSE: {rmse:.4f}, MAE: {mae:.4f}, MAPE: {mape:.2f}%, Peak_RMSE: {peak_rmse:.4f}, Step6_RMSE: {step6_rmse:.4f}")
    
    print("\n--- Historical Mean Baseline ---")
    preds_mean = historical_mean_baseline(testX)
    rmse, mae, mape = compute_metrics(preds_mean, testY, max_value)
    peak_rmse, _ = compute_peak_metrics(preds_mean, testY, max_value)
    step6_rmse = np.sqrt(np.mean((preds_mean[:, -1, :] - testY[:, -1, :]) ** 2))
    results.append({
        'Method': 'Historical Mean (L=12)',
        'RMSE': rmse,
        'MAE': mae,
        'MAPE': mape,
        'Peak_RMSE': peak_rmse,
        'Step6_RMSE': step6_rmse
    })
    print(f"RMSE: {rmse:.4f}, MAE: {mae:.4f}, MAPE: {mape:.2f}%, Peak_RMSE: {peak_rmse:.4f}, Step6_RMSE: {step6_rmse:.4f}")
    
    print("\n--- GRU Baseline ---")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    gru_model = GRUBaseline(input_dim=95, hidden_dim=64, output_steps=6)
    gru_model = train_baseline_model(gru_model, trainX, trainY, validX, validY, 
                                     epochs=args.gru_epochs, lr=args.gru_lr, device=device)
    
    gru_model.eval()
    with torch.no_grad():
        test_tensor = torch.Tensor(testX).to(device)
        preds_gru = gru_model(test_tensor).cpu().numpy()
    
    rmse, mae, mape = compute_metrics(preds_gru, testY, max_value)
    peak_rmse, _ = compute_peak_metrics(preds_gru, testY, max_value)
    step6_rmse = np.sqrt(np.mean((preds_gru[:, -1, :] - testY[:, -1, :]) ** 2))
    results.append({
        'Method': 'GRU Baseline',
        'RMSE': rmse,
        'MAE': mae,
        'MAPE': mape,
        'Peak_RMSE': peak_rmse,
        'Step6_RMSE': step6_rmse
    })
    print(f"RMSE: {rmse:.4f}, MAE: {mae:.4f}, MAPE: {mape:.2f}%, Peak_RMSE: {peak_rmse:.4f}, Step6_RMSE: {step6_rmse:.4f}")
    
    print("\n--- Linear Regression Baseline ---")
    linear_model = LinearBaseline(seq_len=12, pred_len=6, num_nodes=95)
    linear_model = train_baseline_model(linear_model, trainX, trainY, validX, validY,
                                        epochs=args.linear_epochs, lr=args.linear_lr, device=device)
    
    linear_model.eval()
    with torch.no_grad():
        test_tensor = torch.Tensor(testX).to(device)
        preds_linear = linear_model(test_tensor).cpu().numpy()
    
    rmse, mae, mape = compute_metrics(preds_linear, testY, max_value)
    peak_rmse, _ = compute_peak_metrics(preds_linear, testY, max_value)
    step6_rmse = np.sqrt(np.mean((preds_linear[:, -1, :] - testY[:, -1, :]) ** 2))
    results.append({
        'Method': 'Linear Regression',
        'RMSE': rmse,
        'MAE': mae,
        'MAPE': mape,
        'Peak_RMSE': peak_rmse,
        'Step6_RMSE': step6_rmse
    })
    print(f"RMSE: {rmse:.4f}, MAE: {mae:.4f}, MAPE: {mape:.2f}%, Peak_RMSE: {peak_rmse:.4f}, Step6_RMSE: {step6_rmse:.4f}")
    
    df = pd.DataFrame(results)
    out_dir = args.output_dir
    os.makedirs(out_dir, exist_ok=True)
    
    csv_path = os.path.join(out_dir, 'baseline_results.csv')
    df.to_csv(csv_path, index=False)
    print(f"\nResults saved to: {csv_path}")
    
    results_serializable = [{k: float(v) if isinstance(v, (np.floating, np.float32, np.float64)) else v for k, v in r.items()} for r in results]
    with open(os.path.join(out_dir, 'baseline_results.json'), 'w', encoding='utf-8') as f:
        json.dump(results_serializable, f, ensure_ascii=False, indent=2)
    
    print("\n=== Summary ===")
    print(df.to_string(index=False))
    
    return results


def parse_args():
    parser = argparse.ArgumentParser(description='Baseline evaluation for O3 prediction')
    parser.add_argument('--data_dir', type=str, default='/mnt/d/时空数据/臭氧预测资料',
                        help='Path to data directory')
    parser.add_argument('--output_dir', type=str, default='/mnt/d/时空数据/白文豪/week1/output',
                        help='Output directory for results')
    parser.add_argument('--max_value', type=float, default=100.0,
                        help='Max O3 concentration for metrics calculation')
    parser.add_argument('--gru_epochs', type=int, default=50,
                        help='Number of epochs for GRU training')
    parser.add_argument('--gru_lr', type=float, default=1e-3,
                        help='Learning rate for GRU')
    parser.add_argument('--linear_epochs', type=int, default=100,
                        help='Number of epochs for linear regression')
    parser.add_argument('--linear_lr', type=float, default=1e-2,
                        help='Learning rate for linear regression')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    set_seed(args.seed)
    evaluate_baselines(args)