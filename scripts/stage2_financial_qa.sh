cd src

chatglm_path="/home/guozq/source/data/alphafin/model/chatglm2_6b"
stockgpt2_path="/home/guozq/source/data/alphafin/model/stockgpt_stage2_lora"
embedding_path="/home/guozq/source/data/alphafin/model/BGE-Large"

python stage2_financial_qa/webui/run.py \
    --base_model_path ${chatglm_path} \
    --lora_ckpt_path ${stockgpt2_path} \
    --embedding_model_path ${embedding_path}