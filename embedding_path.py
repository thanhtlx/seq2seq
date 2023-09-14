import torch
from transformers import RobertaTokenizer, RobertaConfig, RobertaModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")
model.to(device)
1
import json
import os
from tqdm import tqdm
with open('100path_32k_data.json') as f:
    data = json.load(f)
import random 

keys = list(data.keys())
random.shuffle(keys)
for k in tqdm(keys):
    v = data[k]
    file = f'data/path_embedding/{k}.pt'
    if os.path.exists(file):
        continue
    embedding = torch.zeros((100,768))
    for idx,path in enumerate(v.splitlines()):
        if idx > 100:
            break
        path_token = tokenizer.tokenize(path)
        path_token = path_token[:200]
        path_tokens = [tokenizer.cls_token]+path_token+[tokenizer.eos_token]
        path_ids=tokenizer.convert_tokens_to_ids(path_tokens)
        context_embeddings=model(torch.tensor(path_ids,device=device)[None,:])[0]
        # print(context_embeddings.shape)
        embedding[idx] = context_embeddings[:, 0, :]
    torch.save(embedding,file)