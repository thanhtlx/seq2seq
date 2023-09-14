import pandas as pd 
df = pd.read_parquet(f'data/cmg-data-processed.parquet', engine='fastparquet')
# df = df.sort_values(by=['extract_level'])
print(df.head(1)['index'])
result = list()
cms = set(df['index'])
from tqdm import tqdm
for idx in tqdm(cms):
    rows = df[df['index']==idx]
    index = idx.replace('_file_fc_patch.csv','')
    codes = list()
    for _, row in rows.iterrows():
        diff = row['change_abstract']
        # for l in row['diff'].splitlines():
        #     if l.startswith('-') or l.startswith('+'):
        #         diff.append(l)
        doc = row['msg_change_abstract'].split()
        if row['old_path_file'] == row['new_path_file']:
            file = row['new_path_file']
        else:
            if row['old_path_file'] is not None and row['new_path_file'] is not None:
                file = row['old_path_file'] + ' SEP ' + row['new_path_file']
            else:
                file = row['old_path_file'] if row['old_path_file'] is not None else row['new_path_file']
        file = file+ ' SEP'
        code = file + diff
        code = code.split() + ["SEP"]
        codes.extend(code)
    result.append({'code_tokens':codes,'docstring_tokens':doc,'index':index})
import random 
with open('data/split-data/randomly/train_id.txt') as f:
    train_id = [l.strip() for l in f.readlines()]
with open('data/split-data/randomly/test_id.txt') as f:
    test_id = [l.strip() for l in f.readlines()]
with open('data/split-data/randomly/valid_id.txt') as f:
    val_id = [l.strip() for l in f.readlines()]
train,test,val = [],[],[]
for el in result:
    if el['index'] in train_id:
        train.append(el)
    elif el['index'] in val_id:
        val.append(el)
    else:
        test.append(el)
import json
def dump_to_file(obj, file):
    with open(file,'w+') as f:
        for el in obj:
            f.write(json.dumps(el)+'\n')
dump_to_file(train,'data/train3.jsonl')
dump_to_file(test,'data/test3.jsonl')
dump_to_file(val,'data/valid3.jsonl')