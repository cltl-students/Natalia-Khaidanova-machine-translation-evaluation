import pandas as pd
import os 
import torch
from bleurt_pytorch import BleurtConfig, BleurtForSequenceClassification, BleurtTokenizer
import time


news_data = pd.read_csv(r'../Data/all_news_data.tsv', sep='\t') 
news_candidates = r'../Data/WMT21-data/system-outputs/newstest2021'
news_references_A = list(news_data['news_ref_A'])
news_references_B = list(news_data['news_ref_B'])

all_news_references = []
for A, B in zip(news_references_A, news_references_B):
    all_news_references.append([A, B])
    
ted_data = pd.read_csv(r'../Data/all_TED_data.tsv', sep='\t') 
ted_candidates = r'../Data/WMT21-data/system-outputs/tedtalks'
ted_references = list(ted_data['TED_ref'])

bleurt_20_config = BleurtConfig.from_pretrained('lucadiliello/BLEURT-20')
bleurt_20_model = BleurtForSequenceClassification.from_pretrained('lucadiliello/BLEURT-20')
bleurt_20_tokenizer = BleurtTokenizer.from_pretrained('lucadiliello/BLEURT-20')
bleurt_20_model.eval()


for file_name in os.listdir(news_candidates):
    if file_name[23:-3] not in ['ref-A','ref-B','']:
        
        data_dict, bleurt_20_scores_ref_A, bleurt_20_scores_ref_B = {}, [], []
        start_time = time.time()
        count = 0
        print(f'computing scores for {file_name[23:-3]}:')
        candidates = list(news_data[file_name[23:-3]])

        for references, candidate in zip(all_news_references, candidates):
            count += 1
            with torch.no_grad():
                try:
                    # compute BLEURT-20 scores for reference A
                    inputs = bleurt_20_tokenizer(references[0], candidate, padding='longest', return_tensors='pt')
                    bleurt_20_score_ref_A = bleurt_20_model(**inputs).logits.flatten().tolist()
                    bleurt_20_scores_ref_A.append(f'{bleurt_20_score_ref_A[0]:.2f}')
                    # compute BLEURT-20 scores for reference B
                    inputs = bleurt_20_tokenizer(references[1], candidate, padding='longest', return_tensors='pt')
                    bleurt_20_score_ref_B = bleurt_20_model(**inputs).logits.flatten().tolist()
                    bleurt_20_scores_ref_B.append(f'{bleurt_20_score_ref_B[0]:.2f}')
                except Exception:
                    bleurt_20_scores_ref_A.append('0.00')
                    bleurt_20_scores_ref_B.append('0.00')

            if count == 250:
                print('scores for 250 candidates are computed')    
            if count == 501:
                print('half of the scores is computed') 
            if count == 800:
                print('scores for 800 candidates are computed')  
            if count == 950:
                print('almost done')

        data_dict['BLEURT-20_ref_A'] = bleurt_20_scores_ref_A 
        data_dict['BLEURT-20_ref_B'] = bleurt_20_scores_ref_B  

        end_time = time.time()
        total_time = end_time - start_time
        print(f'BLEURT-20 runtime on the newstest2021 data for{file_name[23:-3]}: {total_time:.2f} seconds')
        print('==================')

        news_bleurt_20_data = pd.DataFrame(data_dict)
        news_bleurt_20_data.to_csv(f'../Data/newstest2021/BLEURT-20/{file_name[23:-3]}_BLEURT-20.tsv', sep='\t', index=False) 

        
for file_name in os.listdir(ted_candidates):
    if file_name[19:-3] != 'ref-A':
        
        data_dict, bleurt_20_scores = {}, []
        start_time = time.time()
        count = 0
        print(f'computing scores for {file_name[19:-3]}:')
        candidates = list(ted_data[file_name[19:-3]])

        for reference, candidate in zip(ted_references, candidates):
            count += 1
            with torch.no_grad():
                inputs = bleurt_20_tokenizer(reference, candidate, padding='longest', return_tensors='pt')
                bleurt_20_score = bleurt_20_model(**inputs).logits.flatten().tolist()
                bleurt_20_scores.append(f'{bleurt_20_score[0]:.2f}')

            if count == 120:
                print('scores for 120 candidates are computed')    
            if count == 256:
                print('half of the scores is computed') 
            if count == 350:
                print('scores for 350 candidates are computed')  
            if count == 480:
                print('almost done')

        data_dict['BLEURT-20'] = bleurt_20_scores 

        end_time = time.time()
        total_time = end_time - start_time
        print(f'BLEURT-20 runtime on the tedtalks data for {file_name[19:-3]}: {total_time:.2f} seconds')
        print('==================')

        ted_bleurt_20_data = pd.DataFrame(data_dict)
        ted_bleurt_20_data.to_csv(f'../Data/tedtalks/BLEURT-20/{file_name[19:-3]}_BLEURT-20.tsv', sep='\t', index=False) 
            
