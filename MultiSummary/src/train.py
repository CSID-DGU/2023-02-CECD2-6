# -*- coding: utf-8 -*- 
#!/usr/bin/env python
"""
    Main training workflow
"""
from __future__ import division

import argparse
import os
import kss
from summerizer import summarize
from others.logging import init_logger

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

    data=[]
    text = '''
        경기도가 추석을 앞두고 다음달 6일까지 도내 유통 제수 및 선물용 농축산물을 대상으로 원산지표시 특별점검을 실시한다.
        
        특히 이번 단속에는 지난달 광역 최초로 발족한 '경기도 원산지표시 감시원' 120명이 전격 투입된다.
        
        공정거래 질서를 확립하고자 마련된 이번 점검에서 점검단은 도내 농축수산물 판매장 및 전통시장을 대상으로 쇠고기, 돼지고기, 닭고기, 고사리, 조기 등 '제수용 농축수산물'과 갈비세트, 과일바구니, 한과류 등 '선물용 농축산물'의 원산지 표시 위반여부 등을 집중 점검할 예정이다.
        
        이와 함께 원산지표시 감시원을 중심으로 구성된 점검단은 원산지 표시 방법이 담긴 홍보물 및 안내표지판을 배부하는 등 원산지 표시 제도에 대한 계도 활동도 병행 실시할 계획이다.
        
        이해원 경기도 농식품유통과장은 "원산지표시를 위반한 식재료가 도민들의 식탁에 오르지 않도록 철저한 지도·점검을 실시하겠다"고 말했다.
        
        한편, 농수산물 원산지를 잘못 표시할 경우 7년 이하의 징역 또는 1억원 이하의 벌금에 처해진다.
        
        이와 함께 원산지를 표시하지 않거나 표시방법을 위반할 경우 1,000만 원 이하의 과태료가 부과된다.
        
        원산지표시 점검에서 적발된 위반업체 및 위반 유형은 국립농산물품질관리원 홈페이지(http://www.naqs.go.kr/main/main.do)에서 확인할 수 있다.
    '''
    data.append(kss.split_sentences(text))

    text='''
    [디지털데일리 권하영 기자] KT(대표 김영섭)는 타타대우상용차와 출시한 상용차 커넥티드카 솔루션 ‘쎈링크(XENLINK)’에 AI 편의기능을 대폭 강화한다고 29일 밝혔다.

    KT는 지난해 4월 타타대우상용차와 함께 내놓은 쎈링크에 상용차 전용 AI 보이스봇과 운행기록 자동 제출 서비스를 출시했다. 
    
    더불어 ‘쎈링크’의 차별화 서비스였던 원격 차량품질 관리 솔루션 ‘타타대우 VRM’을 고도화했다.

    쎈링크에 도입된 AI 보이스봇은 AS 접수 등 단순 업무 처리를 돕고 보증기간과 소모품 교체 주기 사전 알림을 제공한다. 
    
    서비스 만족도 조사에도 활용된다. 
    
    보이스봇을 통해 고객 상담 시간은 줄어들고 고객이 필요한 정보를 신속히 제공할 수 있다. 
    
    KT는 이 보이스봇에 KT의 AICC 기술을 적용했다.

    디지털운행기록(DTG) 제출 의무가 있는 사업자를 위한 ‘운행기록 자동 제출 서비스’도 새로 제공한다. 
    
    KT는 교통안전법상 교통안전공단에 디지털운행기록제출 의무가 있는 사업자로부터 운행기록 제출책임을 위탁 받아, KT 자체 플랫폼을 통해 차량에서 수집된 운행기록 정보를 교통안전공단의 연동 규격에 맞춰 자동 제출한다.

    이로써 제출 지연에 따른 과태료 부과를 막고 차주가 직접 자료를 다운로드·업로드 해야하는 번거로움을 해소할 수 있다. 
    
    운행기록 제출 자동화 기능을 이용하고 싶은 ‘쎈링크’ 가입 차주는 서비스 이용을 위한 고객 동의를 하면 된다.
    '''
    data.append(kss.split_sentences(text))
    
    if args.task == "ext":
        if args.mode == "train":
            train_ext(args, device_id)
        elif args.mode == "validate":
            validate_ext(args, device_id)
        elif args.mode == "test":
            cp = args.test_from
            try:
                step = int(cp.split(".")[-2].split("_")[-1])
            except:
                step = 0
            summarize(data,args,cp)
            #test_ext(args, device_id, cp, step)


