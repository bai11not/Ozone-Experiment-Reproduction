#!/usr/bin/env python
"""Generate flow.npy and adj.npy for DiffSTG from our project data."""
import numpy as np
import os

PROJECT = r'H:\Trae Project\O3predict'
DST = os.path.join(PROJECT, 'external_baselines', 'DiffSTG', 'DiffSTG-main', 'data', 'dataset', 'AIR_N95')
os.makedirs(DST, exist_ok=True)

# 1. flow.npy: (T, N, F) = (8717, 95, 1)
o3 = np.load(os.path.join(PROJECT, 'matrix_N95', 'data.npy')).astype(np.float32)  # (95, 8717)
flow = o3.T[:, :, np.newaxis]  # (8717, 95, 1)
np.save(os.path.join(DST, 'flow.npy'), flow)
print(f'flow.npy: {flow.shape} saved to {DST}')

# 2. adj.npy: (N, N) — binarize the spatial distance graph
S = np.load(os.path.join(PROJECT, 'matrix_N95', 'S_matrix.npy')).astype(np.float32)
# Binarize: values > threshold become 1 (connected), rest 0
threshold = 0.1
adj = (S > threshold).astype(np.float32)
np.save(os.path.join(DST, 'adj.npy'), adj)
print(f'adj.npy: {adj.shape}, edges={int(adj.sum())}, saved to {DST}')
print('Done.')
