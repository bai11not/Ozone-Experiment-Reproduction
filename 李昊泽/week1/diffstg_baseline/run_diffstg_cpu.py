#!/usr/bin/env python
"""Minimal runner for DiffSTG baseline on CPU — no NNI dependency.
Usage: python run_diffstg_cpu.py
"""
# Mock NNI module before any other imports
class MockNNI:
    def get_next_parameter(self):
        return {}
    def report_intermediate_result(self, x):
        pass
    def report_final_result(self, x):
        pass

import sys
import types
nni_mod = types.ModuleType('nni')
nni_mod.get_next_parameter = MockNNI().get_next_parameter
nni_mod.report_intermediate_result = MockNNI().report_intermediate_result
nni_mod.report_final_result = MockNNI().report_final_result
sys.modules['nni'] = nni_mod

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['NNI_OUTPUT_DIR'] = os.path.join(os.path.dirname(__file__), 'output', 'nni_tmp')
os.makedirs(os.environ['NNI_OUTPUT_DIR'], exist_ok=True)

from train import main

params = {
    'data': 'AIR_N95',
    'is_train': True,
    'is_test': False,
    'nni': False,
    'lr': 0.002,
    'batch_size': 4,
    'mask_ratio': 0.0,
    'N': 20,              # minimal diffusion steps for CPU test
    'T_h': 24,            # 24h input → 24h output (matches our task)
    'epsilon_theta': 'UGnet',
    'sample_steps': 20,
    'hidden_size': 8,     # tiny for CPU quick test
    'beta_end': 0.02,
    'beta_schedule': 'quad',
    'ss': 'ddpm',
    'n_samples': 1,
}
main(params)
