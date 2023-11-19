import argparse
import yaml
import os

import sys
sys.path.append("../src")
from others.logging import init_logger

def str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")

def parse_args():
    with open('../config/SummaryConfig.yaml', 'r', encoding='utf-8') as file:
            yaml_args = yaml.safe_load(file)
    
    parser = argparse.ArgumentParser()
    for key, value in yaml_args.items():
        parser.add_argument(f"-{key}", default=value)

    parser.add_argument(
        "-encoder", default="bert", type=str, choices=["bert", "baseline"]
    )
    parser.add_argument("-model_path", default="../models/")
    parser.add_argument("-load_from_extractive", default="", type=str)
    parser.add_argument("-lr_bert", default=2e-3, type=float)
    parser.add_argument("-lr_dec", default=2e-3, type=float)
    parser.add_argument(
        "-use_bert_emb", type=str2bool, nargs="?", const=True, default=False
    )
    parser.add_argument(
        "-share_emb", type=str2bool, nargs="?", const=True, default=False
    )
    parser.add_argument(
        "-finetune_bert", type=str2bool, nargs="?", const=True, default=True
    )
    parser.add_argument("-dec_dropout", default=0.2, type=float)
    parser.add_argument("-dec_layers", default=6, type=int)
    parser.add_argument("-dec_hidden_size", default=768, type=int)
    parser.add_argument("-dec_heads", default=8, type=int)
    parser.add_argument("-dec_ff_size", default=2048, type=int)
    parser.add_argument("-enc_hidden_size", default=512, type=int)
    parser.add_argument("-enc_ff_size", default=512, type=int)
    parser.add_argument("-enc_dropout", default=0.2, type=float)
    parser.add_argument("-enc_layers", default=6, type=int)
    parser.add_argument('-min_src_nsents', default=1, type=int)    # 3
    parser.add_argument('-max_src_nsents', default=120, type=int)    # 100
    parser.add_argument('-min_src_ntokens_per_sent', default=1, type=int)    # 5
    parser.add_argument('-max_src_ntokens_per_sent', default=300, type=int)    # 200
    parser.add_argument('-min_tgt_ntokens', default=1, type=int)    # 5
    parser.add_argument('-max_tgt_ntokens', default=500, type=int)    # 500

    # params for EXT
    parser.add_argument("-ext_dropout", default=0.2, type=float)
    parser.add_argument("-ext_layers", default=2, type=int)
    parser.add_argument("-ext_hidden_size", default=768, type=int)
    parser.add_argument("-ext_heads", default=8, type=int)
    parser.add_argument("-ext_ff_size", default=2048, type=int)
    parser.add_argument("-label_smoothing", default=0.1, type=float)
    parser.add_argument("-generator_shard_size", default=32, type=int)
    parser.add_argument("-beam_size", default=5, type=int)
    parser.add_argument("-param_init", default=0, type=float)
    parser.add_argument(
        "-param_init_glorot", type=str2bool, nargs="?", const=True, default=True
    )
    parser.add_argument("-optim", default="adam", type=str)
    parser.add_argument("-lr", default=1, type=float)
    parser.add_argument("-beta1", default=0.9, type=float)
    parser.add_argument("-beta2", default=0.999, type=float)
    parser.add_argument("-warmup_steps", default=8000, type=int)
    parser.add_argument("-warmup_steps_bert", default=8000, type=int)
    parser.add_argument("-warmup_steps_dec", default=8000, type=int)
    parser.add_argument("-max_grad_norm", default=0, type=float)
    parser.add_argument("-save_checkpoint_steps", default=5, type=int)
    parser.add_argument("-accum_count", default=1, type=int)
    parser.add_argument("-report_every", default=1, type=int)
    parser.add_argument("-train_steps", default=1000, type=int)
    parser.add_argument("-valid_steps", default=500, type=int)
    parser.add_argument("-stop_training", default=5, type=int)
    parser.add_argument(
        "-recall_eval", type=str2bool, nargs="?", const=True, default=False
    )
    parser.add_argument("-gpu_ranks", default="0", type=str)
    parser.add_argument("-seed", default=666, type=int)
    parser.add_argument(
        "-test_all", type=str2bool, nargs="?", const=True, default=False
    )
    parser.add_argument("-test_start_from", default=-1, type=int)
    parser.add_argument("-train_from", default="")
    parser.add_argument(
        "-block_trigram", type=str2bool, nargs="?", const=True, default=True
    )

    args = parser.parse_args([]) 
    args.gpu_ranks = [int(i) for i in range(len(args.visible_gpus.split(",")))]
    args.world_size = len(args.gpu_ranks)
    os.environ["CUDA_VISIBLE_DEVICES"] = args.visible_gpus

    print(args)
    init_logger(args.log_file)

    cp = args.test_from
    try:
        step = int(cp.split(".")[-2].split("_")[-1])
    except:
        step = 0

    return args, cp, step