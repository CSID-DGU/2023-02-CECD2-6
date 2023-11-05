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

    text= '''
    [디지털데일리 최민지 기자] “나부터 ‘준법과 신뢰위원회’ 결정을 존중할 것이며, 그렇지 않은 계열사들의 행동이나 사업에 대해선 대주주로서 할 수 있는 최대한의 책임을 묻겠다.”

    최근 카카오를 향한 사법리스크가 커지는 가운데, 3일 카카오 창업자 김범수 미래이니셔티브센터장은 관계사 준법·윤리경영을 감시할 외부 기구인 ‘준법과 신뢰 위원회(이하 위원회)’ 위원장으로 김소영 전 대법관을 위촉하며 이같이 밝혔다.

    김범수 센터장의 이번 발언은 카카오 창업 역사상 처음 있는 일이다. 그동안 계열사에 경영 간섭을 하지 않는 것을 경영철학으로 삼아 온 카카오다. 심지어, 그 철학을 만든 창업자가 직접 계열사에게 공동의 행동을 하지 않을 경우 책임을 묻겠다는 강도 높은 발언을 했다.

    김 센터장이 여러 번 밝혔듯, 카카오 설립 목표는 100인의 최고경영자(CEO)를 육성하는 것이다. 독립경영을 통해 카카오 신사업을 키워내 왔고, 창의성과 역동성이 중요한 만큼 계열사들은 자율적인 경영을 최대한 보장받았다. 카카오 본사에서도 계열사 경영에 간섭할 수 없는 구조를 확립했다.

    카카오가 그룹 관계사를 계열사 또는 자회사 등으로 부르지 않고 ‘공동체’라고 말해 왔던 이유이기도 하다. 그러나, 김 센터장은 이번 발언에서 공동체라는 단어 대신 계열사로 지칭했다. 기존 방식에서 탈피해 달라지겠다는 의지가 강하게 읽히는 대목이다.

    김 센터장은 “지금 카카오는 기존 경영방식으로는 더이상 지속 가능하지 않은 상황이라는 위기의식을 갖고 있다”며 “처음부터 끝까지 철저히 빠르게 점검하고 국민의 눈높이에 맞는 경영시스템을 갖출 때까지 뼈를 깎는 노력을 다할 것”이라고 말했다.

    성장을 이끌었던 과거와 달리, 기존의 경영방침은 오히려 독이 되고 있다. 각자가 따로 행동했을 때, 통제하지 못한 리스크가 곳곳에서 튀어나와 카카오 전체를 잠식시킬 수도 있는 상황이다.

    김 센터장은 카카오페이 경영진 스톡옵션 논란, 카카오 서비스 장애 등 굵직한 현안이 발생했을 때도 현 경영진들 역할을 넘어서지 않도록 지원 역할을 맡아 왔었다. 하지만, 경영일선에서 물러난 창업자가 직접 목소리를 내고, 경영방식을 바꾸는 등 강력한 의지로 움직이고 있다. 카카오를 지키기 위해 그룹 계열사가 모두 같은 방향으로 위기에 함께 대응해야 하기 때문이다. 그만큼 카카오가 존폐를 걱정할 정도로 전례 없는 위기라는 판단이다.

    금융감독원(이하 금감원)은 에스엠엔터테인먼트 인수 관련 시세 조작 혐의를 조사하면서, 김 센터장을 금감원 특별사법경찰 출범 이후 처음 마련된 포토라인에 세웠다. 마치 검찰처럼 현직 경영진이 아닌 창업주를 포토라인에 세우는 이례적인 퍼포먼스를 펼친 것이다. 일각에선 혐의가 확정되지도 않은 상황에서, 금감원이 무리하게 욕심을 내 과도한 연출을 한 것 아니냐는 목소리도 제기한다.

    그러나, 아직 의혹이 풀리지 않은 만큼 고강도 조사는 계속될 수밖에 없는 상황이다. 배재현 카카오 공동체 투자총괄 대표는 법정 구속됐고, 김 센터장을 향해서도 구속영장 카드를 만지작거리고 있다.

    여기에서 그치지 않고, 윤석열 대통령까지 카카오모빌리티 문제점을 지적하며 카카오를 ‘나쁜 기업’으로 낙인찍었다. 윤 대통령이 지난 1일 비상경제민생회의에서 카카오모빌리티 수수료를 문제 삼는 발언을 듣고 “카카오의 택시 횡포는 독과점 행위 중 아주 부도덕한 행태이기에 정부가 제재해야 한다”고 강하게 비판한 것이다.

    카카오가 ‘최고 비상 경영 단계’를 선포한 가운데, 벌어진 일이다. 카카오모빌리티는 택시업계와 긴급 간담회를 개최하기로 했다. 이후 카카오는 예고했던 대로, 빠르게 관계사 준법·윤리경영을 감시할 외부 기구인 ‘준법과 신뢰 위원회(이하 위원회)’를 설립했다.

    이번 위원회는 카카오와 독립된 외부 조직으로, 개별 관계사의 준법감시와 내부 통제 체계를 일신할 수 있는 강력한 집행기구 역할을 한다. 카카오 관계사의 주요 위험 요인 선정 및 그에 대한 준법감시 시스템 구축 및 운영 단계부터 관여할 예정이다. 또한 과도한 관계사 상장, 공정거래법 위반, 시장 독과점, 이용자 이익 저해, 최고경영진의 준법 의무 위반에 대한 감시 통제 등 카카오가 사회적으로 지적 받았던 여러 문제에 대한 관리 감독과 능동적 조사 권한을 갖는다.

    앞서, 김 센터장은 지난달 30일 계열사 CEO들과 공동체 경영회의를 열고 “최근 상황을 겪으며 나부터 부족했던 부분을 반성하고, 더 강화된 내외부의 준법 경영 및 통제 시스템을 마련하는 게 필요하다고 생각했다”고 전한 바 있다.
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
            summarize(data,args, device_id, cp, step)
            #test_ext(args, device_id, cp, step)


