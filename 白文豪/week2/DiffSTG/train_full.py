# -*- coding: utf-8 -*-
"""DiffSTG 正式训练脚本 -- 完整训练，无 debug 模式"""

import os, sys

# 导入 week1 DiffSTG 模块
_WEEK1 = os.path.join(os.path.dirname(__file__), '..', '..', 'week1', 'DiffSTG')
sys.path.insert(0, _WEEK1)

import torch
import argparse
import json
import numpy as np
import torch.utils.data
from easydict import EasyDict as edict
from timeit import default_timer as timer

from utils.eval import Metric
from utils.gpu_dispatch import GPU
from utils.common_utils import dir_check, to_device, ws, unfold_dict, dict_merge, GpuId2CudaId, Logger

from algorithm.dataset import CleanDataset, TrafficDataset
from algorithm.diffstg.model import DiffSTG, save2file


def setup_seed(seed):
    import random
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    torch.backends.cudnn.deterministic = True


def get_params():
    parser = argparse.ArgumentParser(description='DiffSTG full training')
    # model
    parser.add_argument("--epsilon_theta", type=str, default='UGnet')
    parser.add_argument("--hidden_size", type=int, default=32)
    parser.add_argument("--N", type=int, default=200)
    parser.add_argument("--beta_schedule", type=str, default='quad')
    parser.add_argument("--beta_end", type=float, default=0.1)
    parser.add_argument("--sample_steps", type=int, default=200)
    parser.add_argument("--ss", type=str, default='ddpm')
    parser.add_argument("--T_h", type=int, default=12)
    parser.add_argument("--T_p", type=int, default=12)
    # eval
    parser.add_argument('--n_samples', type=int, default=8)
    # train
    parser.add_argument("--data", type=str, default='AIR_N95')
    parser.add_argument("--lr", type=float, default=0.0001)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mask_ratio", type=float, default=0.0)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--early_stop", type=int, default=10)
    parser.add_argument("--min_delta", type=float, default=0.001)
    parser.add_argument("--output_dir", type=str, default="")

    args, _ = parser.parse_known_args()
    return args


def default_config(data='AIR_N95'):
    config = edict()
    config.PATH_MOD = ws + '/output/model/'
    config.PATH_LOG = ws + '/output/log/'
    config.PATH_FORECAST = ws + '/output/forecast/'

    config.data = edict()
    config.data.name = data
    config.data.path = ws + '/data/dataset/'
    config.data.feature_file = config.data.path + config.data.name + '/flow.npy'
    config.data.spatial = config.data.path + config.data.name + '/adj.npy'
    config.data.num_recent = 1

    if config.data.name == 'PEMS08':
        config.data.num_features = 1
        config.data.num_vertices = 170
        config.data.points_per_hour = 12
        config.data.val_start_idx = int(17856 * 0.6)
        config.data.test_start_idx = int(17856 * 0.8)

    if config.data.name == "AIR_BJ":
        config.data.num_features = 1
        config.data.num_vertices = 34
        config.data.points_per_hour = 1
        config.data.val_start_idx = int(8760 * 0.6)
        config.data.test_start_idx = int(8760 * 0.8)

    if config.data.name == 'AIR_GZ':
        config.data.num_features = 1
        config.data.num_vertices = 41
        config.data.points_per_hour = 1
        config.data.val_start_idx = int(8760 * 10 / 12)
        config.data.test_start_idx = int(8160 * 11 / 12)

    if config.data.name == 'AIR_N95':
        config.data.num_features = 1
        config.data.num_vertices = 95
        config.data.points_per_hour = 1
        config.data.val_start_idx = 7378
        config.data.test_start_idx = 8047

    if config.data.name == 'AIR_N95_PM25':
        config.data.num_features = 1
        config.data.num_vertices = 95
        config.data.points_per_hour = 1
        config.data.val_start_idx = 7378
        config.data.test_start_idx = 8047

    if config.data.name == 'AIR_N95_PM10':
        config.data.num_features = 1
        config.data.num_vertices = 95
        config.data.points_per_hour = 1
        config.data.val_start_idx = 7378
        config.data.test_start_idx = 8047

    if config.data.name == 'AIR_N95_CORR':
        config.data.num_features = 1
        config.data.num_vertices = 95
        config.data.points_per_hour = 1
        config.data.val_start_idx = 7378
        config.data.test_start_idx = 8047

    if config.data.name == 'AIR_N95_PE':
        config.data.num_features = 1
        config.data.num_vertices = 95
        config.data.points_per_hour = 1
        config.data.val_start_idx = 7378
        config.data.test_start_idx = 8047

    gpu_id = GPU().get_usefuel_gpu(max_memory=6000, condidate_gpu_id=[0,1,2,3,4,6,7,8])
    config.gpu_id = gpu_id
    if gpu_id is not None:
        cuda_id = GpuId2CudaId(gpu_id)
        torch.cuda.set_device(f"cuda:{cuda_id}")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    config.model = edict()
    config.model.T_p = 12
    config.model.T_h = 12
    config.model.V = config.data.num_vertices
    config.model.F = config.data.num_features
    config.model.week_len = 7
    config.model.day_len = config.data.points_per_hour * 24
    config.model.device = device
    config.model.d_h = 32

    config.model.N = 200
    config.model.sample_steps = 200
    config.model.epsilon_theta = 'UGnet'
    config.model.is_label_condition = True
    config.model.beta_end = 0.02
    config.model.beta_schedule = 'quad'
    config.model.sample_strategy = 'ddpm'

    config.n_samples = 2
    config.model.channel_multipliers = [1, 2]
    config.model.supports_len = 2

    config.model_name = 'DiffSTG'
    config.is_test = False  # 始终关闭 debug 模式
    config.epoch = 300
    config.optimizer = "adam"
    config.lr = 1e-4
    config.batch_size = 32
    config.wd = 1e-5
    config.early_stop = 10
    config.start_epoch = 0
    config.device = device
    config.logger = Logger()

    for p in [config.PATH_MOD, config.PATH_LOG, config.PATH_FORECAST]:
        os.makedirs(p, exist_ok=True)
    return config


def evals(model, data_loader, epoch, metric, config, clean_data, mode='Test'):
    setup_seed(2022)
    y_pred, y_true, time_lst = [], [], []
    metrics_future = Metric(T_p=config.model.T_p)
    metrics_history = Metric(T_p=config.model.T_h)
    model.eval()
    samples, targets = [], []

    for i, batch in enumerate(data_loader):
        time_start = timer()
        future, history, pos_w, pos_d = to_device(batch, config.device)

        x = torch.cat((history, future), dim=1).to(config.device)
        x_masked = torch.cat((history, torch.zeros_like(future)), dim=1).to(config.device)
        targets.append(x.cpu())
        x = x.transpose(1, 3)
        x_masked = x_masked.transpose(1, 3)

        n_samples = 1 if mode == 'Val' else config.n_samples
        x_hat = model((x_masked, pos_w, pos_d), n_samples)
        samples.append(x_hat.transpose(2, 4).cpu())

        if x_hat.shape[-1] != (config.model.T_h + config.model.T_p):
            x_hat = x_hat.transpose(2, 4)

        time_lst.append((timer() - time_start))
        x, x_hat = clean_data.reverse_normalization(x), clean_data.reverse_normalization(x_hat)
        x_hat = x_hat.detach()
        f_x, f_x_hat = x[:, :, :, -config.model.T_p:], x_hat[:, :, :, :, -config.model.T_p:]

        _y_true_ = f_x.transpose(1, 3).cpu().numpy()
        _y_pred_ = f_x_hat.transpose(2, 4).cpu().numpy()
        _y_pred_ = np.clip(_y_pred_, 0, np.inf)
        metrics_future.update_metrics(_y_true_, _y_pred_)

        y_pred.append(_y_pred_)
        y_true.append(_y_true_)

        h_x, h_x_hat = x[:, :, :, :config.model.T_h], x_hat[:, :, :, :, :config.model.T_h]
        _y_true_ = h_x.transpose(1, 3).cpu().numpy()
        _y_pred_ = h_x_hat.transpose(2, 4).cpu().numpy()
        _y_pred_ = np.clip(_y_pred_, 0, np.inf)
        metrics_history.update_metrics(_y_true_, _y_pred_)

    y_true = np.concatenate(y_true, axis=0)
    y_pred = np.concatenate(y_pred, axis=0)

    time_cost = np.sum(time_lst)
    metric.update_metrics(y_true, y_pred)
    metric.update_best_metrics(epoch=epoch)
    metric.metrics['time'] = time_cost

    if metric.best_metrics['epoch'] == epoch:
        message = f" |[{metric.metrics['mae']:<7.4f}{metric.metrics['rmse']:<7.4f}]"
    else:
        message = f" | {metric.metrics['mae']:<7.4f}{metric.metrics['rmse']:<7.4f}"
    print(message, end='', flush=False)
    config.logger.message_buffer += message

    message = f" | {metrics_history.metrics['mae']:<7.4f}{metrics_history.metrics['rmse']:<7.4f}{time_cost:<5.2f}s"
    print(message, end='\n', flush=False)
    config.logger.message_buffer += f"{message}\n"
    config.logger.write_message_buffer()

    torch.cuda.empty_cache()
    return metric


def main(params: dict):
    seed = params.get('seed', 42)
    setup_seed(seed)
    torch.set_num_threads(2)
    config = default_config(params['data'])

    config.lr = params['lr']
    config.batch_size = params['batch_size']
    config.mask_ratio = params['mask_ratio']
    if params.get('epochs'):
        config.epoch = params['epochs']
    if params.get('early_stop'):
        config.early_stop = params['early_stop']

    # model params
    config.model.N = params['N']
    config.T_h = config.model.T_h = params['T_h']
    config.T_p = config.model.T_p = params.get('T_p', params['T_h'])
    config.model.epsilon_theta = params['epsilon_theta']
    config.model.sample_steps = params['sample_steps']
    config.model.d_h = params['hidden_size']
    config.model.C = params['hidden_size']
    config.model.n_channels = params['hidden_size']
    config.model.beta_end = params['beta_end']
    config.model.beta_schedule = params["beta_schedule"]
    config.model.sample_strategy = params["ss"]
    config.n_samples = params['n_samples']

    if config.model.sample_steps > config.model.N:
        print('sample steps large than N, exit')
        return

    config.trial_name = '+'.join([f"{v}" for k, v in params.items()])
    config.log_path = f"{config.PATH_LOG}/{config.trial_name}.log"

    print(f"=== DiffSTG Training ===")
    print(f"  seed:     {seed}")
    print(f"  data:     {params['data']}")
    print(f"  T_h:      {config.model.T_h}")
    print(f"  T_p:      {config.model.T_p}")
    print(f"  hidden:   {params['hidden_size']}")
    print(f"  N:        {params['N']}")
    print(f"  lr:       {params['lr']}")
    print(f"  batch:    {params['batch_size']}")
    print(f"  epochs:   {config.epoch}")

    dir_check(config.log_path)
    config.logger.open(config.log_path, mode="w")
    config.logger.write(config.__str__() + '\n', is_terminal=False)

    clean_data = CleanDataset(config)
    config.model.A = clean_data.adj

    model = DiffSTG(config.model)
    model = model.to(config.device)
    print(f"  params:   {sum([p.numel() for p in model.parameters()]):,}")

    train_dataset = TrafficDataset(clean_data,
        (0 + config.model.T_p, config.data.val_start_idx - config.model.T_p + 1), config)
    train_loader = torch.utils.data.DataLoader(train_dataset, config.batch_size, shuffle=True, pin_memory=True)

    val_dataset = TrafficDataset(clean_data,
        (config.data.val_start_idx + config.model.T_p, config.data.test_start_idx - config.model.T_p + 1), config)
    val_loader = torch.utils.data.DataLoader(val_dataset, 64, shuffle=False)

    test_dataset = TrafficDataset(clean_data,
        (config.data.test_start_idx + config.model.T_p, -1), config)
    test_loader = torch.utils.data.DataLoader(test_dataset, 64, shuffle=False)

    optimizer = torch.optim.Adam(model.parameters(), lr=config.lr, weight_decay=0)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)

    metrics_val = Metric(T_p=config.model.T_h + config.model.T_p)

    model_path = config.PATH_MOD + config.trial_name + model.model_file_name()
    config.model_path = model_path
    config.logger.write(f"model path:{model_path}\n", is_terminal=False)
    print(f"  model:    {model_path}")

    dir_check(model_path)
    config.forecast_path = config.PATH_FORECAST + config.trial_name + '.pkl'
    dir_check(config.forecast_path)

    config.logger.write(model.__str__())
    config.logger.write(f'Num_of_parameters:{sum([p.numel() for p in model.parameters()])}\n', is_terminal=True)
    config.logger.write("      |---Train--- |---Val Future-- -|-----Val History----|\n", is_terminal=True)
    config.logger.write("Epoch | Loss  Time | MAE     RMSE    |  MAE    RMSE   Time|\n", is_terminal=True)

    min_delta = params.get('min_delta', 0.001)
    patience_counter = 0
    best_mae = float('inf')

    train_start_t = timer()
    for epoch in range(config.epoch):
        n, avg_loss, time_lst = 0, 0, []
        for i, batch in enumerate(train_loader):
            time_start = timer()
            future, history, pos_w, pos_d = batch
            x = torch.cat((history, future), dim=1).to(config.device)
            mask = torch.randint_like(history, low=0, high=100) < int(config.mask_ratio * 100)
            history[mask] = 0
            x_masked = torch.cat((history, torch.zeros_like(future)), dim=1).to(config.device)
            x = x.transpose(1, 3)
            x_masked = x_masked.transpose(1, 3)

            loss = 10 * model.loss(x, (x_masked, pos_w, pos_d))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            n += 1
            avg_loss = avg_loss * (n - 1) / n + loss.item() / n
            time_lst.append((timer() - time_start))
            message = f"{i / len(train_loader) + epoch:6.1f}| {avg_loss:0.3f} {np.sum(time_lst):.1f}s"
            if (i + 1) % 50 == 0 or i == 0:
                print('\r' + message, end='', flush=True)

        config.logger.message_buffer += message

        if epoch >= config.start_epoch:
            evals(model, val_loader, epoch, metrics_val, config, clean_data, mode='Val')
            scheduler.step(metrics_val.metrics['mae'])

        if metrics_val.best_metrics['epoch'] == epoch:
            torch.save(model, model_path)

        # min_delta 早停: 改善小于 min_delta 不算改进
        current_mae = metrics_val.metrics['mae']
        if best_mae - current_mae > min_delta:
            best_mae = current_mae
            patience_counter = 0
        else:
            patience_counter += 1

        if patience_counter >= config.early_stop:
            print(f"\n[EARLY STOP] epoch={epoch+1}, best_val_mae={best_mae:.4f}, patience={patience_counter}")
            break

    # Load best model and evaluate on test set
    try:
        model = torch.load(model_path, map_location=config.device)
        print(f'best model loaded: {model_path}')
    except Exception as err:
        print(f'load best model failed: {err}')

    metric_lst = []
    for sample_strategy, sample_steps in [('ddim_multi', 40)]:
        if sample_steps > config.model.N:
            break
        config.model.sample_strategy = sample_strategy
        config.model.sample_steps = sample_steps
        model.set_ddim_sample_steps(sample_steps)
        model.set_sample_strategy(sample_strategy)

        metrics_test = Metric(T_p=config.model.T_h + config.model.T_p)
        evals(model, test_loader, epoch, metrics_test, config, clean_data, mode='test')

        result_params = unfold_dict(config)
        result_params = dict_merge([result_params, metrics_test.to_dict()])
        result_params['best_epoch'] = metrics_val.best_metrics['epoch']
        result_params['model'] = config.model.epsilon_theta
        save2file(result_params)
        metric_lst.append(metrics_test.metrics['mae'])

    # Output final metrics
    metrics_output = {
        "model": "DiffSTG",
        "seed": seed,
        "data": params['data'],
        "T_h": config.model.T_h,
        "T_p": config.model.T_p,
        "best_epoch": metrics_val.best_metrics['epoch'] + 1,
        "best_val_mae": round(float(metrics_val.best_metrics['mae']), 4),
        "best_val_rmse": round(float(metrics_val.best_metrics['rmse']), 4),
        "test_mae": round(float(metrics_test.metrics['mae']), 4),
        "test_rmse": round(float(metrics_test.metrics['rmse']), 4),
        "test_mape": round(float(metrics_test.metrics['mape']), 2),
        "test_crps": round(float(metrics_test.metrics.get('crps', 0)), 4),
    }

    # Save metrics JSON
    output_dir = params.get('output_dir', '')
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        json_path = os.path.join(output_dir, 'metrics_summary.json')
        with open(json_path, 'w') as f:
            json.dump(metrics_output, f, indent=2, ensure_ascii=False)
        print(f"\nMetrics saved to: {json_path}")

    print(f"\n{'='*50}")
    print(f"  DiffSTG 训练完成")
    print(f"  Best Epoch: {metrics_output['best_epoch']}")
    print(f"  Test MAE:   {metrics_output['test_mae']}")
    print(f"  Test RMSE:  {metrics_output['test_rmse']}")
    print(f"  Test MAPE:  {metrics_output['test_mape']}%")
    print(f"{'='*50}")

    # Rename log file with MAE prefix
    if metric_lst:
        log_file, log_name = os.path.split(config.log_path)
        new_log_path = os.path.join(log_file, f"[{config.data.name}]mae{min(metric_lst):7.2f}+{log_name}")
        import shutil
        shutil.copy(config.log_path, new_log_path)

    return metrics_output


if __name__ == '__main__':
    params = vars(get_params())
    main(params)