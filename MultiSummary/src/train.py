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
    AI(인공지능)가 유머감각까지 갖출까.

    일론 머스크 테슬라 CEO(최고경영자)가 새로 설립한 AI(인공지능) 스타트업 'xAI'가 선보일 AI 기술을 일부 공개했다.

    머스크는 4일(현지시간) 자신의 엑스(X·옛 트위터) 계정에 xAI가 내놓을 첫 작품인 AI 비서에 대한 정보를 공개했다. 
    
    머스크는 xAI의 생성형 AI가 '그록(Grok)'이라고 밝혔다. 그는 '이해하다', '공감하다'라는 의미를 가진 '그록'은 다른 AI 모델에 비해 실시간 접근이 가능하고 풍자와 같은 유머감각을 포함하도록 설계했다고 언급했다.

    '그록'이란 말은 로버트 A.하인리히의 1961년 장편 SF 소설인 '낯선 땅 이방인'에서 처음 사용됐고, 히피 문화에 이 신조어를 퍼뜨린 것으로 알려졌다. 기술 업계에서는 '깊은 이해'를 나타내는 단어로 활용된다.

    머스크는 X에서 '그록'의 기능을 과시하기도 했다. 코카인의 단계별 제조방법을 묻는 요청에 대해 그록은 "코카인 레시피를 불러오는 동안 잠시 기다려 달라"고 답하며 4단계에 걸친 제조법을 제시했다. 
    
    화학 학위 취득, 비밀 실험실 설치, 다량의 코카잎과 화학물질 구하기, 스스로 폭발하지 않기 바라는 마음으로 요리하기 등 단계를 나열했다. 
    
    하지만 이어 그록은 "단지 농담"이라고 밝히며 "그것은 불법적이고 위험하며 권장할 일이 아니다"고 언급했다.

    실제 머스크가 그록에게 건넨 같은 질문으로 챗GPT에 물어보자 "미안하다, 제가 도와드릴 일은 아니다"라는 답이 돌아왔고, 구글 바드에 질문하니 "저는 언어모델일 뿐 필요한 정보나 능력이 없어 도움을 드릴 수 없다"는 답이 돌아왔다.

    또 지난 2일 가상화폐 거래소 FTX 설립자 샘 뱅크먼-프리드가 금융사기 등으로 유죄 평결을 받은 데 대해서도 "믿어지시나요? 배심원단은 세계에서 가장 똑똑한 최고의 벤처캐피털이 몇 년 동안 하지 못한 일, 즉 그가 다양한 종류의 사기를 저질렀다는 사실을 알아내는 데 단 8시간밖에 걸리지 않았다"며 풍자하는 답변을 내놓았다.

    그록은 선별된 그룹에 테스트 버전으로 공개된 후 X 계정을 통해서만 실시간으로 이용할 수 있게 될 전망이다. 
    
    머스크는 웹으로는 월 16달러에 X 프리미엄 구독자들에게 '그록'이 제공된다고 밝혔다.
    '''
    data.append(kss.split_sentences(text))

    text='''
    (샌프란시스코=연합뉴스) 김태종 특파원 = 일론 머스크 테슬라 최고경영자(CEO)가 설립한 인공지능(AI) 스타트업 xAI가 첫번째 AI 챗봇을 내놓았다.

    xAI는 4일(현지시간) 오후 홈페이지를 통해 챗GPT와 같은 생성형 AI '그록(Grok)'을 공개했다.

    지난 7월 12일 설립한 지 약 4개월 만이다. 'grok'은 '이해하다, 공감하다'는 의미를 갖고 있다.

    이 스타트업은 "그록은 은하수를 여행하는 히치하이커의 안내서(Hitchhiker's Guide to the Galaxy)를 모델로 한 인공지능으로, 거의 모든 질문에 대답할 수 있고 어떤 질문을 해야 할지 제안하기도 한다"고 설명했다.

    또 "약간의 재치로 질문에 대답하도록 설계됐으며 반항적인 성향을 갖고 있다"며 "유머를 싫어한다면 사용하지 마라"고 적었다.

    이어 그록의 독특하고 근본적인 장점은 "플랫폼을 통해 전 세계에 대한 실시간 지식을 가지고 있다는 것"이라며 "대부분의 다른 인공지능 시스템에서 거부하는 매운 질문에도 답할 수 있다"고 강조했다.

    아울러 "그록은 아직 초기 베타 제품이며, 여러분의 도움으로 매주 빠르게 개선될 것으로 기대한다"고 덧붙였다.

    그록은 xAI가 개발한 대규모 언어 모델(LLM) 그록-1(Grok-1)을 기반으로 구동된다.

    xAI는 설립 후 330억 개의 매개 변수를 가진 Grok-0을 훈련해 추론과 코딩 기능이 크게 향상된 최첨단 언어 모델 그록-1을 달성했다고 설명했다.

    앞서 머스크는 자신의 엑스(X) 계정에 챗GPT와 같은, xAI의 생성형 AI가 '그록'(Grok)이라고 밝힌 바 있다.

    머스크는 '그록'이 다른 AI보다 많은 이점이 있다며 특히, 약간 비꼬는 듯한 유머 감각을 갖고 있다고 설명했다.

    그러면서 코카인을 만드는 방법 등에 대한 답을 제시했다.

    코카인 제조 방법을 알려달라고 하자 '그록'은 "잠깐만 기다려, 집에서 만들 수 있는 코카인 레시피를 가져올 게"라고 한 뒤 4단계에 걸친 제조법을 제시했다.

    이어 "단지 농담!"이라며 "실제 코카인은 만들려고 하지 마. 그것은 불법이고 위험하고 내가 권하지 않아"라고 답했다.

    또 지난 2일 가상화폐 거래소 FTX 설립자 샘 뱅크먼-프리드가 금융사기 등으로 유죄 평결을 받은 데 대해서도 다소 비꼬며 일부 답변을 내놓았다.

    '그록'은 이 평결에 대해 "믿어지시나요? 배심원단은 세계에서 가장 똑똑한 최고의 벤처캐피털이 몇 년 동안 하지 못한 일, 즉 그가 다양한 종류의 사기를 저질렀다는 사실을 알아내는 데 단 8시간밖에 걸리지 않았다"고 지적했다.

    머스크는 '그록'이 선별된 그룹에 테스트 버전으로 공개된 뒤 이후 X 계정을 통해서만 실시간 이용할 수 있게 될 것이라고 전했다. 
    
    특히, 웹으로는 월 16달러에 X 프리미엄 구독자들에게 '그록'이 제공된다고 덧붙였다.

    머스크는 지난 3일에는 "내일 xAI가 첫 번째 AI를 선별된 그룹에 공개할 것"이라고 밝힌 바 있다.
    '''
    data.append(kss.split_sentences(text))

    text= '''
    일론 머스크 테슬라 최고경영자(CEO)가 설립한 인공지능(AI) 스타트업 xAI가 첫 번째 AI 챗봇을 내놓았습니다.

    xAI는 4일(현지시간) 오후 홈페이지를 통해 챗GPT와 같은 생성형 AI '그록(Grok)'을 공개했습니다.

    지난 7월 12일 설립한 지 약 4개월 만입니다. 'grok'은 '이해하다, 공감하다'는 의미를 갖고 있습니다.

    이 스타트업은 "그록은 은하수를 여행하는 히치하이커의 안내서(Hitchhiker's Guide to the Galaxy)를 모델로 한 인공지능으로, 거의 모든 질문에 대답할 수 있고 어떤 질문을 해야 할지 제안하기도 한다"고 설명했습니다.

    또 "약간의 재치로 질문에 대답하도록 설계됐으며 반항적인 성향을 갖고 있다"며 "유머를 싫어한다면 사용하지 마라"고 적었습니다.

    이어 그록의 독특하고 근본적인 장점은 "플랫폼을 통해 전 세계에 대한 실시간 지식을 가지고 있다는 것"이라며 "대부분의 다른 인공지능 시스템에서 거부하는 매운 질문에도 답할 수 있다"고 강조했습니다.

    아울러 "그록은 아직 초기 베타 제품이며, 여러분의 도움으로 매주 빠르게 개선될 것으로 기대한다"고 덧붙였습니다.

    그록은 xAI가 개발한 대규모 언어 모델(LLM) 그록-1(Grok-1)을 기반으로 구동됩니다.

    xAI는 설립 후 330억 개의 매개 변수를 가진 Grok-0을 훈련해 추론과 코딩 기능이 크게 향상된 최첨단 언어 모델 그록-1을 달성했다고 설명했습니다.
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


