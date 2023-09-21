from tqdm import tqdm

DATA_DIR = 'data/cmg-data'

import pandas as pd 
df = pd.read_parquet(f'{DATA_DIR}/cmg-data-processed.parquet', engine='fastparquet')
print(f'Num of commits:', df['index'].nunique())

with open('cms.txt') as f:
    cms = [l.strip() for l in f.readlines()]

def get_id(dir_path='cmg-data/split-data', type='randomly'):
    with open(f'{dir_path}/{type}/train_id.txt') as file:
        train_val_id = [line.rstrip() for line in file]
    with open(f'{dir_path}/{type}/test_id.txt') as file:
        test_id = [line.rstrip() for line in file]
        
    test_id = list(set(cms).intersection(set(test_id)))
    train_val_id = list(set(cms).intersection(set(train_val_id)))

    df = pd.DataFrame(train_val_id, columns=['index'])
    train_percent = 0.9
    train_id = list(df['index'].sample(int(df['index'].nunique() - 1000), random_state=42))
    val_id = list(df[~df['index'].isin(train_id)]['index'])

    print(f'Training size: {len(train_id)}   |   Val size: {len(val_id)}   |   Test size: {len(test_id)}')
    
    return train_id, val_id, test_id

train_id, val_id, test_id = get_id(dir_path=f'{DATA_DIR}/split-data', type='cross_project')
# train_id, val_id, test_id = get_id(dir_path=f'{DATA_DIR}/split-data')

df_type = pd.read_csv('meta_patch_db.csv')
type_dict = dict()
for _,row in df_type.iterrows():
    index = str(row['commit_id'])
    index = index.lower()
    type_dict[index] = 1 if row['category'] == 'security' else 0 
    
data = list()
index_list = set(df['index'])

for id in tqdm(index_list):
    df_commit = df[df['index']==id]
    codes = list()
    for _, row in df_commit .iterrows():
        diff = row['change_abstract']
        msg = row['msg_change_abstract'].split()
        if row['old_path_file'] == row['new_path_file']:
            file_name = row['new_path_file']
        else:
            if row['old_path_file'] is not None and row['new_path_file'] is not None:
                file_name = row['old_path_file'] + ' SEP ' + row['new_path_file']
            else:
                file_name = row['old_path_file'] if row['old_path_file'] is not None else row['new_path_file']

        code = file_name + ' SEP ' + diff
        code = code.split() + ["SEP"]
        codes.extend(code)
    commit_id = id.split('_')[-1]

    if commit_id in type_dict.keys():
        type = type_dict[commit_id]
    else:
        type = 1

    data.append({'code_tokens': codes, 
                 'docstring_tokens': msg, 
                 'index': id.replace('_file_fc_patch.csv',''), 
                 'type': type
                })



len(data)
train,test,val = [],[],[]
for el in data:
    if el['index'] in train_id:
        train.append(el)
    elif el['index'] in val_id:
        val.append(el)
    else:
        test.append(el)

import json
def dump_to_file(obj, file):
    with open(file, 'w') as f:
        for el in obj:
            f.write(json.dumps(el)+'\n')

print(len(train), len(val), len(test))
dump_to_file(train,f'{DATA_DIR}/train.jsonl')
dump_to_file(test,f'{DATA_DIR}/test.jsonl')
dump_to_file(val,f'{DATA_DIR}/valid.jsonl')