import yaml
from comet.models.regression.referenceless import ReferencelessRegression
from comet.models.regression.regression_metric import RegressionMetric
from comet.models.ranking.ranking_metric import RankingMetric
from comet.models.multitask.unified_metric import UnifiedMetric
import pandas as pd
from comet import download_model, load_from_checkpoint


def load_comet_model(checkpoint_path, hparams_path):
    """
    Load wmt21-comet-qe-mqm model.
    
    :param str checkpoint_path: path to the model.ckpt file 
    :param str hparams_path: path to the hparams.yaml file 
    :return: wmt21-comet-qe-mqm model
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


try: # load the model from Hugging Face 
    model_path = download_model('NataliaKhaidanova/wmt21-comet-qe-mqm')
    comet_qe_mqm_2021_model = load_from_checkpoint(model_path)
except Exception: # load the model from local storage 
    checkpoint_path = r'wmt21-comet-qe-mqm/checkpoints/model.ckpt' # set your model's path 
    hparams_path = r'wmt21-comet-qe-mqm/hparams.yaml' # set your hyperparameters' path 
    comet_qe_mqm_2021_model = load_comet_model(checkpoint_path, hparams_path) 
    

for file in [r'baby_k.tsv', r'a_beautiful_mind.tsv']:
    
    seg_data_dict, sys_data_dict = {}, {}
    comet_qe_mqm_2021_human_scores, comet_qe_mqm_2021_opus_mt_scores = [], []
    
    df = pd.read_csv(f'Data/{file}', sep='\t') 
    sources = list(df['source'])
    human_translations = list(df['human_translation'])
    opus_mt_translations = list(df['opus_mt_translation'])

    for source, human_translation in zip(sources, human_translations):
        inputs = [{'src':source,'mt':human_translation}]
            
        comet_qe_mqm_2021_score = comet_qe_mqm_2021_model.predict(inputs, batch_size=8, gpus=1)
        comet_qe_mqm_2021_human_scores.append(f'{comet_qe_mqm_2021_score[0][0]:.3f}')
        
    for source, opus_mt_translation in zip(sources, opus_mt_translations):
        inputs = [{'src':source,'mt':opus_mt_translation}]
            
        comet_qe_mqm_2021_score = comet_qe_mqm_2021_model.predict(inputs, batch_size=8, gpus=1)
        comet_qe_mqm_2021_opus_mt_scores.append(f'{comet_qe_mqm_2021_score[0][0]:.3f}')

    seg_data_dict['human_scores'] = comet_qe_mqm_2021_human_scores    
    seg_data_dict['opus_mt_scores'] = comet_qe_mqm_2021_opus_mt_scores   
    
    sys_data_dict['human_scores'] = f'{sum([float(x) for x in comet_qe_mqm_2021_human_scores]) / len(comet_qe_mqm_2021_human_scores):.3f}'
    sys_data_dict['opus_mt_scores'] = f'{sum([float(x) for x in comet_qe_mqm_2021_opus_mt_scores]) / len(comet_qe_mqm_2021_opus_mt_scores):.3f}'
    # save segment-level scores
    seg_comet_qe_mqm_2021_data = pd.DataFrame(seg_data_dict)
    seg_comet_qe_mqm_2021_data.to_csv(f'Data/seg_COMET-QE-MQM_2021_{file[5:-4]}.tsv', sep='\t', index=False) 
    # save system-level scores 
    sys_comet_qe_mqm_2021_data = pd.DataFrame(sys_data_dict, index=[0])
    sys_comet_qe_mqm_2021_data.to_csv(f'Data/sys_COMET-QE-MQM_2021_{file[5:-4]}.tsv', sep='\t', index=False) 
