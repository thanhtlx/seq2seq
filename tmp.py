import os
import numpy as np
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import  Cider
import bleu

def calc_prec(pred, tgt):
    prds = pred.split()
    tgs = tgt.split()
    count = 0 
    for prd in prds:
        if prd in tgs:
            count += 1
    return count/ len(prds)

def cal_metrics(index):
    prd_dir = os.path.join(f'{output_dir}','test_1.output')
    gold_dir = os.path.join(f'{output_dir}','test_1.gold')
    predictions = list()
    golds = list()
    
    with open(prd_dir) as f:
        predictions =  [line.strip() for line in f.readlines()]
    with open(gold_dir) as f:
        golds =  [line.strip() for line in f.readlines()]
    tmp_file= 'tmpgold.txt'
    with open(tmp_file,'w+') as f:
        f.write('\n'.join(golds))
    
    EM = list()
    precs = list()
    for i, (ref, gold) in enumerate(zip(predictions, golds)):
        EM.append(ref.split() == gold.split())
        precs.append(calc_prec(ref,gold))
    (goldMap, predictionMap) = bleu.computeMaps(
        predictions, tmp_file)
    dev_bleu = round(bleu.bleuFromMaps(goldMap, predictionMap)[0], 3)
    (goldMap2, predictionMap2) = bleu.computeMaps(
        predictions, tmp_file)
    dev_bleu2 = round(bleu.bleuFromMaps(goldMap2, predictionMap2)[0], 3)
    EM = round(np.mean(EM)*100, 3)
    precs = round(np.mean(precs)*100, 3)
    res = {k: [' '.join(v.split('\t')[1:]).strip().lower()] for k, v in enumerate(predictions)}
    tgt = {k: [' '.join(v.split('\t')[1:]).strip().lower()] for k, v in enumerate(golds)}
    
    # precision 1-gram
    print(len(res))
    print(len(tgt))
    score_Meteor, scores_Meteor = Meteor().compute_score(tgt, res)
    print("Meteor: %s" % (float(score_Meteor)*100))
    score_Rouge, scores_Rouge = Rouge().compute_score(tgt, res)
    print("ROUGE-L: %s" % (float(score_Rouge)*100))
    print(" %s = %s " % ("EM", str(EM)))
    print(" %s = %s " % ("precs", str(precs)))
    print("  %s = %s " % ("bleu-4", str(dev_bleu)))
    print("  %s = %s " % ("bleu-normal", str(dev_bleu2)))
    os.remove(tmp_file)
tt = 't1002'
output_dir = 'output'
for i in range(1,2):
    print(i)
    cal_metrics(i)
# !for pid in $(ps -ef | grep meteor | awk {'print $2'}); do kill -9 $pid; done