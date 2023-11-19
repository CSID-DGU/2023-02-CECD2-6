import os
import sys
import time
import argparse

# from src.others.test_rouge_score import RougeScorer

## define paths 
PROJECT_DIR = os.getcwd() # current path
print(PROJECT_DIR)

DATA_DIR = f"{PROJECT_DIR}/datasets"
#RAW_DATA_DIR = DATA_DIR + "/raw"
#JSON_DATA_DIR = DATA_DIR + "/json"
#BERT_DATA_DIR = DATA_DIR + "/bert"
LOG_DIR = f"{PROJECT_DIR}/results/logs"
LOG_PREPO_FILE = LOG_DIR + "/preprocessing.log"

MODEL_DIR = f"{PROJECT_DIR}/model"
RESULT_DIR = f"{PROJECT_DIR}/results"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", default="ext", type=str, choices=["ext", "abs"])
    parser.add_argument(
        "--mode",
        default="test",
        type=str,
        choices=["install", "make_data", "train", "valid", "test"],
    )   

    parser.add_argument("--n_cpus", default="2", type=str)
    parser.add_argument("--visible_gpus", default="-1", type=str) #cpu 주 
    parser.add_argument("--train_from", default=None, type=str)
    parser.add_argument("--use_model", default="kobert", type=str)
    parser.add_argument("--test_from", default="model_step_20500.pt", type=str)
    parser.add_argument("--make_gold", default="false", type=str)
    args = parser.parse_args()

    now = time.strftime('%m%d_%H%M')

    if args.mode == "test":
        os.chdir(PROJECT_DIR + "/src")
        if(args.test_from != "model_step_20500.pt"):
            model_folder, model_name = args.test_from.rsplit("/", 1)
            model_name = model_name.split("_", 1)[1].split(".")[0]
        else:
            model_name = "step_20500"

        do_str = "python train.py -task ext -mode test"
        
        if args.use_model == "kobert":
            use_model = "skt/kobert-base-v1"
        elif args.use_model == "distilkobert":
            use_model = "monologg/distilkobert"
        
        param = (f" -test_from {MODEL_DIR}/{args.test_from}" +
            f" -bert_data_path {PROJECT_DIR}/datasets/bert" +
            f" -result_path {RESULT_DIR}/result" +
            f" -log_file {LOG_DIR}/{model_name}.log" +
            " -test_batch_size 1 -batch_size 3000" +
            f" -sep_optim true -use_interval true -visible_gpus {args.visible_gpus}" +
            " -max_pos 512 -max_length 200 -alpha 0.95 -min_length 50" +
            f" -report_rouge False -max_tgt_len 100 -make_gold {args.make_gold} -use_model {use_model}")

        do_str += param
        print( param)
        print(do_str)

        os.system(do_str)