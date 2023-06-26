import yaml
from comet.models.regression.referenceless import ReferencelessRegression
from comet.models.regression.regression_metric import RegressionMetric
from comet.models.ranking.ranking_metric import RankingMetric
from comet.models.multitask.unified_metric import UnifiedMetric
import pandas as pd
import os
from comet import download_model, load_from_checkpoint
import time


def load_comet_model(checkpoint_path, hparams_path):
    """
    Load wmt21-comet-mqm model.
    
    :param str checkpoint_path: path to the model.ckpt file 
    :param str hparams_path: path to the hparams.yaml file 
    :return: wmt21-comet-mqm model
    """   
    str2model = {'referenceless_regression_metric': ReferencelessRegression,
                 'regression_metric': RegressionMetric,
                 'ranking_metric': RankingMetric,
                 'unified_metric': UnifiedMetric}

    with open(hparams_path) as yaml_file:
        hparams = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)
    model_class = str2model[hparams['class_identifier']]
    model = model_class.load_from_checkpoint(checkpoint_path, load_pretrained_weights=False)

    return model
    
    
news_data = pd.read_csv(r'../Data/all_news_data.tsv', sep='\t') 
news_candidates = r'../Data/WMT21-data/system-outputs/newstest2021'
news_source = list(news_data['news_source'])
news_references_A = list(news_data['news_ref_A'])
news_references_B = list(news_data['news_ref_B'])

all_news_references = []
for A, B in zip(news_references_A, news_references_B):
    all_news_references.append([A, B])
    
ted_data = pd.read_csv(r'../Data/all_TED_data.tsv', sep='\t') 
ted_candidates = r'../Data/WMT21-data/system-outputs/tedtalks'
ted_source = list(ted_data['TED_source'])
ted_references = list(ted_data['TED_ref'])

try: # load the model from Hugging Face
    model_path = download_model('NataliaKhaidanova/wmt21-comet-mqm')
    comet_mqm_2021_model = load_from_checkpoint(model_path)
except Exception: # load the model from local storage 
    checkpoint_path = r'wmt21-comet-mqm/checkpoints/model.ckpt' # set your model's path 
    hparams_path = r'wmt21-comet-mqm/hparams.yaml' # set your hyperparameters' path 
    comet_mqm_2021_model = load_comet_model(checkpoint_path, hparams_path) 


for file_name in os.listdir(news_candidates):
    if file_name[23:-3] not in ['ref-A','ref-B','']:

        data_dict, comet_mqm_2021_scores_ref_A, comet_mqm_2021_scores_ref_B = {}, [], []
        start_time = time.time()
        count = 0
        print(f'computing scores for {file_name[23:-3]}:')
        candidates = list(news_data[file_name[23:-3]])

        for source, references, candidate in zip(news_source, all_news_references, candidates):
            count += 1
            inputs_ref_A = [{'src':source,'mt':candidate,'ref':references[0]}]
            inputs_ref_B = [{'src':source,'mt':candidate,'ref':references[1]}]
            try:
                # compute COMET-MQM_2021 scores for reference A
                comet_mqm_2021_score_ref_A = comet_mqm_2021_model.predict(inputs_ref_A, batch_size=8, gpus=1)
                comet_mqm_2021_scores_ref_A.append(f'{comet_mqm_2021_score_ref_A[0][0]:.3f}')
                # compute COMET-MQM_2021 scores for reference B
                comet_mqm_2021_score_ref_B = comet_mqm_2021_model.predict(inputs_ref_B, batch_size=8, gpus=1)
                comet_mqm_2021_scores_ref_B.append(f'{comet_mqm_2021_score_ref_B[0][0]:.3f}')
            except Exception:
                comet_mqm_2021_scores_ref_A.append('0.000')
                comet_mqm_2021_scores_ref_B.append('0.000')
                
            if count == 250:
                print('------------------')
                print('SCORES FOR 250 CANDIDATES ARE COMPUTED') 
                print('------------------')
            if count == 501:
                print('------------------')
                print('HALF OF THE SCORES IS COMPUTED') 
                print('------------------')
            if count == 800:
                print('------------------')
                print('SCORES FOR 800 CANDIDATES ARE COMPUTED')  
                print('------------------')
            if count == 950:
                print('------------------')
                print('ALMOST DONE')
                print('------------------')
                          
        data_dict['COMET-MQM_2021_ref_A'] = comet_mqm_2021_scores_ref_A 
        data_dict['COMET-MQM_2021_ref_B'] = comet_mqm_2021_scores_ref_B  

        end_time = time.time()
        total_time = end_time - start_time
        print(f'COMET-MQM_2021 runtime on the newstest2021 data for {file_name[23:-3]}: {total_time:.2f} seconds')
        print('==================')
          
        news_comet_mqm_2021_data = pd.DataFrame(data_dict)
        news_comet_mqm_2021_data.to_csv(f'../Data/newstest2021/COMET-MQM_2021/{file_name[23:-3]}_COMET-MQM_2021.tsv', sep='\t', index=False) 
        
        
for file_name in os.listdir(ted_candidates):
    if file_name[19:-3] != 'ref-A':

        data_dict, comet_mqm_2021_scores = {}, []
        start_time = time.time()
        count = 0
        print(f'computing scores for {file_name[19:-3]}:')
        candidates = list(ted_data[file_name[19:-3]])

        for source, reference, candidate in zip(ted_source, ted_references, candidates):
            count += 1
            inputs = [{'src':source,'mt':candidate,'ref':reference}]             
            comet_mqm_2021_score = comet_mqm_2021_model.predict(inputs, batch_size=8, gpus=1)
            comet_mqm_2021_scores.append(f'{comet_mqm_2021_score[0][0]:.3f}')
                              
            if count == 120:
                print('------------------')
                print('SCORES FOR 120 CANDIDATES ARE COMPUTED') 
                print('------------------')
            if count == 256:
                print('------------------')
                print('HALF OF THE SCORES IS COMPUTED') 
                print('------------------')
            if count == 350:
                print('------------------')
                print('SCORES FOR 350 CANDIDATES ARE COMPUTED')  
                print('------------------')
            if count == 480:
                print('------------------')
                print('ALMOST DONE')
                print('------------------')
                          
        data_dict['COMET-MQM_2021'] = comet_mqm_2021_scores

        end_time = time.time()
        total_time = end_time - start_time
        print(f'COMET-MQM_2021 runtime on the tedtalks data for {file_name[19:-3]}: {total_time:.2f} seconds')
        print('==================')
          
        ted_comet_mqm_2021_data = pd.DataFrame(data_dict)
        ted_comet_mqm_2021_data.to_csv(f'../Data/tedtalks/COMET-MQM_2021/{file_name[19:-3]}_COMET-MQM_2021.tsv', sep='\t', index=False) 
