# import random 
# with open('data/split-data/randomly/train_id.txt') as f:
#     train = [l.strip() for l in f.readlines()]

# valid = random.sample(train,1000)

# train_rm = set(train).difference(set(valid))
# print(len(valid),len(train_rm),len(train))
# with open('data/split-data/randomly/train_id.txt','w+') as f:
#     f.write('\n'.join(list(train_rm)))
# with open('data/split-data/randomly/valid_id.txt','w+') as f:
#     f.write('\n'.join(list(valid)))
file = 'train_id.txt'
with open(f'data/split-data/randomly/{file}') as f:
    train = [l.strip().replace('_file_fc_patch.csv','') for l in f.readlines()]
with open(f'data/split-data/randomly/{file}','w+') as f:
    f.write('\n'.join(list(train)))
file = 'test_id.txt'
with open(f'data/split-data/randomly/{file}') as f:
    train = [l.strip().replace('_file_fc_patch.csv','') for l in f.readlines()]
with open(f'data/split-data/randomly/{file}','w+') as f:
    f.write('\n'.join(list(train)))
file = 'valid_id.txt'
with open(f'data/split-data/randomly/{file}') as f:
    train = [l.strip().replace('_file_fc_patch.csv','') for l in f.readlines()]
with open(f'data/split-data/randomly/{file}','w+') as f:
    f.write('\n'.join(list(train)))