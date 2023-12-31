# -*- coding: utf-8 -*- 
#!/usr/bin/env python
"""
    Main training workflow
"""
from __future__ import division

import argparse
import os
from multiSummarizer.clustering import Custer
import kss
from summerizer import summarize
from others.logging import init_logger
import yaml
import psycopg2

# from train_abstractive import validate_abs, train_abs, baseline, test_abs, test_text_abs
from train_extractive import train_ext, validate_ext, test_ext

model_flags = [
    "hidden_size",
    "ff_size",
    "heads",
    "emb_size",
    "enc_layers",
    "enc_hidden_size",
    "enc_ff_size",
    "dec_layers",
    "dec_hidden_size",
    "dec_ff_size",
    "encoder",
    "ff_actv",
    "use_interval",
]


def str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-task", default="ext", type=str, choices=["ext", "abs"])
    parser.add_argument(
        "-encoder", default="bert", type=str, choices=["bert", "baseline"]
    )
    parser.add_argument(
        "-mode", default="test", type=str, choices=["train", "validate", "test"]
    )
    parser.add_argument("-bert_data_path", default="../bert_data_new/cnndm")
    parser.add_argument("-model_path", default="../models/")
    parser.add_argument("-result_path", default="../results/cnndm")
    parser.add_argument("-use_model", default="skt/kobert-base-v1")

    parser.add_argument("-batch_size", default=140, type=int)
    parser.add_argument("-test_batch_size", default=200, type=int)

    parser.add_argument("-max_pos", default=512, type=int)
    parser.add_argument(
        "-use_interval", type=str2bool, nargs="?", const=True, default=True
    )
    parser.add_argument("-load_from_extractive", default="", type=str)

    parser.add_argument(
        "-sep_optim", type=str2bool, nargs="?", const=True, default=False
    )
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
    parser.add_argument("-alpha", default=0.6, type=float)
    parser.add_argument("-beam_size", default=5, type=int)
    parser.add_argument("-min_length", default=15, type=int)
    parser.add_argument("-max_length", default=150, type=int)
    parser.add_argument("-max_tgt_len", default=140, type=int)

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

    parser.add_argument("-visible_gpus", default="-1", type=str)
    parser.add_argument("-gpu_ranks", default="0", type=str)
    parser.add_argument("-log_file", default="../logs/cnndm.log")
    parser.add_argument("-seed", default=666, type=int)

    parser.add_argument(
        "-test_all", type=str2bool, nargs="?", const=True, default=False
    )
    parser.add_argument("-test_from", default="")
    parser.add_argument("-test_start_from", default=-1, type=int)
    parser.add_argument("-make_gold", default="false", type=str)

    parser.add_argument("-train_from", default="")
    parser.add_argument(
        "-report_rouge", type=str2bool, nargs="?", const=True, default=True
    )
    parser.add_argument(
        "-block_trigram", type=str2bool, nargs="?", const=True, default=True
    )
    args = parser.parse_args()
    args.gpu_ranks = [int(i) for i in range(len(args.visible_gpus.split(",")))]
    args.world_size = len(args.gpu_ranks)
    os.environ["CUDA_VISIBLE_DEVICES"] = args.visible_gpus

    init_logger(args.log_file)
    device = "cpu" if args.visible_gpus == "-1" else "cuda"
    device_id = 0 if device == "cuda" else -1

    # PostgreSQL 데이터베이스 연결 정보
    with open('../config/DBConfig.yaml', 'r') as yaml_file:
        config_data = yaml.safe_load(yaml_file)

    print(config_data.get('host'))
    # PostgreSQL 연결 정보
    db_config = {
        'host': config_data.get('host', 'localhost'),
        'database': config_data.get('database', 'postgres'),
        'user': config_data.get('user', 'postgres'),
        'password': config_data.get('password', ''),
        'port': config_data.get('port', 5432)
    }

    documents=[]
    try:
        # PostgreSQL에 연결
        connection = psycopg2.connect(**db_config)

        # 커서 생성
        cursor = connection.cursor()

        # 데이터 조회 쿼리 실행
        select_data_query = "SELECT * FROM news;"
        cursor.execute(select_data_query)

        # 결과 가져오기
        rows = cursor.fetchall()
        #print(f'전체 기사:\n{rows}\n')

        # 결과 출력
        for i,row in enumerate(rows):
            article_str=f'{row[5]}'
            article_list = [item.strip() for item in article_str.strip('{}').split(',')]
            documents.append(article_list)
            
            #print(f'{i}번째 기사:\n{article_list}\n')
        

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # 연결 및 커서 닫기
        if connection:
            connection.close()
        if cursor:
            cursor.close()

    #DB에서 가져온 값으로 클러스터링
    articles_by_topic=Custer(documents).hierachyClustering()
    
    for i, articles in enumerate(articles_by_topic.values()):
        print(f"${i}번째:${articles}")
    
    cp = args.test_from
    try:
        step = int(cp.split(".")[-2].split("_")[-1])
    except:
        step = 0
    
    summarys=[]
    for i, articles in enumerate(articles_by_topic.values()):
        data=[]
        print(f'{i}번째')
        for article in articles:
            data.append(kss.split_sentences(article))
        summary=summarize(data,args, device_id, cp, step)
        summarys.append(summary)
        data=[]
    print(summarys)
