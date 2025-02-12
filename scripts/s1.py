import os
import subprocess

# Define paths and configurations
HF_ENDPOINT = "https://hf-mirror.com"
tushare_token = "376beb3a08a44b4d583a87193cddb664016307bbc505f1775e6adbac"
chatglm_path = "/path/to/chatglm2_6b"
stockgpt1_path = "/path/to/stockgpt_stage1_lora"
testdata_path = "data/stage1_testdata.json"
output_path = "../outputs"

stockgpt_pred_jsonl = "stockgpt_prediction.jsonl"
mldl_pred_xlsx = "mldl_prediction.xlsx"
stockgpt_mldl_pred_xlsx = "stockgpt_mldl.xlsx"
final_name = "strategy_result"

# Step 1: Preparation - Download kline db data
db_file_dir = './db_file'
os.makedirs(db_file_dir, exist_ok=True)
download_command = [
    'huggingface-cli', 'download', '--resume-download', '--local-dir-use-symlinks', 'False',
    'AlphaFin/stage1_db_file', '--local-dir', db_file_dir, '--repo-type', 'dataset'
]
#subprocess.run(download_command, check=True)

# Step 2: Inference - Stock trend prediction
stockgpt_inf_command = [
    'python', '../src/stage1_trend_prediction/stockgpt_inf.py',
    '--model_name_or_path', chatglm_path,
    '--lora_name_or_path', stockgpt1_path,
    '--data_path', testdata_path,
    '--output_path', os.path.join(output_path, stockgpt_pred_jsonl)
]
subprocess.run(stockgpt_inf_command, check=True)

# Step 3: PostProcess - Handle invalid values
dataprocess_command = [
    'python', 'stage1_trend_prediction/dataprocess_stockgpt.py',
    '--stockgpt_pred_path', os.path.join(output_path, stockgpt_pred_jsonl),
    '--mldl_pred_path', os.path.join(output_path, mldl_pred_xlsx),
    '--save_path', os.path.join(output_path, stockgpt_mldl_pred_xlsx)
]
subprocess.run(dataprocess_command, check=True)

# Step 4: Execute - Strategy simulation
strategy_test_command = [
    'python', 'stage1_trend_prediction/test_strategy.py',
    '--tushare_token', tushare_token,
    '--stockgpt_mldl_path', os.path.join(output_path, stockgpt_mldl_pred_xlsx),
    '--save_dir', os.path.join(output_path, final_name),
    '--file_name', final_name
]

with open(os.path.join(output_path, 'strategy_test.log'), 'w') as log_file:
    subprocess.run(strategy_test_command, check=True, stdout=log_file, stderr=subprocess.STDOUT)
