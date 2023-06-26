import pandas as pd
import os 
from scipy.stats import kendalltau


def compute_seg_correlation(domain, metric, human_judgment):
    """
    Compute segment-level Kendall's tau for 
    SacreBLEU, TER, CHRF2, BLEURT-20, COMET-MQM_2021, COMET-QE-MQM_2021.
    Get the correlation for both newstest2021 and tedtalks datasets. 
    
    :param sting domain: domain to compute the correlation for ('newstest2021' or 'tedtalks')
    :param sting metric: the metric to compute the correlation for 
    ('sacre_BLEU', 'TER', 'CHRF2', 'BLEURT-20', 'COMET-MQM_2021', 'COMET-QE-MQM_2021')
    :param sting human_judgment: human judgment type ('mqm', 'raw_da', 'z_da') 
    :return: None
    """
    path = f'../Data/{domain}/{metric}'
    
    data_dict = {}
    
    if metric not in ['sacre_BLEU', 'TER', 'CHRF2']:
        for file in os.listdir(path):
            if file.endswith('.tsv'):

                file_df = pd.read_csv(f'../Data/{domain}/{metric}/{file}', sep='\t', on_bad_lines='skip', keep_default_na=False) 

                if metric in ['BLEURT-20', 'COMET-MQM_2021']:
                    
                    if human_judgment == 'mqm':
                        if domain == 'newstest2021':
                            ref_A = list(file_df[f'{metric}_ref_A'])
                            ref_B = list(file_df[f'{metric}_ref_B'])
                            human_ratings_df = pd.read_csv(f'human_judgments_seg/all_news_seg_{human_judgment}_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False)
                            human_ratings = list(human_ratings_df[file.split('_')[0]])
                            annotated_human_ratings, corresponding_ref_A, corresponding_ref_B = [], [], []
                            for id, human_rating in enumerate(human_ratings):
                                if human_rating != 'None':
                                    annotated_human_ratings.append(float(human_rating))
                                    corresponding_ref_A.append(float(ref_A[id]))
                                    corresponding_ref_B.append(float(ref_B[id]))

                            cor_ref_A, p_value_ref_A = kendalltau(corresponding_ref_A, annotated_human_ratings)
                            cor_ref_B, p_value_ref_B = kendalltau(corresponding_ref_B, annotated_human_ratings)
                            cor = (cor_ref_A + cor_ref_B) / 2
                            data_dict[file.split('_')[0]] = f'{cor:.3f}'
                            
                        elif domain == 'tedtalks':
                            metric_scores = list(file_df[metric])
                            human_ratings_df = pd.read_csv(r'human_judgments_seg/all_TED_seg_mqm_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False)
                            human_ratings = list(human_ratings_df[file.split('_')[0]])
                            cor, p_value = kendalltau(metric_scores, human_ratings)
                            data_dict[file.split('_')[0]] = f'{cor:.3f}'
                            
                    else:
                        if domain == 'newstest2021' and 'metricsystem' not in file:

                            ref_A = list(file_df[f'{metric}_ref_A'])
                            ref_B = list(file_df[f'{metric}_ref_B'])
                            human_ratings_df = pd.read_csv(f'human_judgments_seg/all_news_seg_{human_judgment}_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False)
                            human_ratings = list(human_ratings_df[file.split('_')[0]])
                            annotated_human_ratings, corresponding_ref_A, corresponding_ref_B = [], [], []
                            for id, human_rating in enumerate(human_ratings):
                                if human_rating != 'None':
                                    annotated_human_ratings.append(float(human_rating))
                                    corresponding_ref_A.append(float(ref_A[id]))
                                    corresponding_ref_B.append(float(ref_B[id]))

                            cor_ref_A, p_value_ref_A = kendalltau(corresponding_ref_A, annotated_human_ratings)
                            cor_ref_B, p_value_ref_B = kendalltau(corresponding_ref_B, annotated_human_ratings)
                            cor = (cor_ref_A + cor_ref_B) / 2
                            data_dict[file.split('_')[0]] = f'{cor:.3f}'
                        
                if metric == 'COMET-QE-MQM_2021':   
                    if human_judgment == 'mqm':
                        if domain == 'newstest2021':

                            metric_scores = list(file_df[metric])
                            human_ratings_df = pd.read_csv(f'human_judgments_seg/all_news_seg_{human_judgment}_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False) 
                            human_ratings = list(human_ratings_df[file.split('_')[0]])
                            annotated_human_ratings, corresponding_metric_scores = [], []
                            for id, human_rating in enumerate(human_ratings):
                                if human_rating != 'None':
                                    annotated_human_ratings.append(float(human_rating))
                                    corresponding_metric_scores.append(float(metric_scores[id]))
                            cor, p_value = kendalltau(corresponding_metric_scores, annotated_human_ratings)
                            data_dict[file.split('_')[0]] = f'{cor:.3f}'
                            
                        elif domain == 'tedtalks':
                            metric_scores = list(file_df[metric])
                            human_ratings_df = pd.read_csv(r'human_judgments_seg/all_TED_seg_mqm_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False)
                            human_ratings = list(human_ratings_df[file.split('_')[0]])
                            cor, p_value = kendalltau(metric_scores, human_ratings)
                            data_dict[file.split('_')[0]] = f'{cor:.3f}'
                            
                    else:
                        if domain == 'newstest2021' and 'metricsystem' not in file:

                            metric_scores = list(file_df[metric])
                            human_ratings_df = pd.read_csv(f'human_judgments_seg/all_news_seg_{human_judgment}_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False) 
                            human_ratings = list(human_ratings_df[file.split('_')[0]])
                            annotated_human_ratings, corresponding_metric_scores = [], []
                            for id, human_rating in enumerate(human_ratings):
                                if human_rating != 'None':
                                    annotated_human_ratings.append(float(human_rating))
                                    corresponding_metric_scores.append(float(metric_scores[id]))
                            cor, p_value = kendalltau(corresponding_metric_scores, annotated_human_ratings)
                            data_dict[file.split('_')[0]] = f'{cor:.3f}'
                                            
    else:
        path = f'../Data/{domain}/traditional_metrics'
        for file in os.listdir(path):
            if file.endswith('.tsv'):
                
                file_path = f'{path}/{file}'
                file_df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', keep_default_na=False) 
                
                if human_judgment == 'mqm':
                    if domain == 'newstest2021':
                        metric_scores = list(file_df[metric])
                        human_ratings_df = pd.read_csv(f'human_judgments_seg/all_news_seg_{human_judgment}_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False) 
                        human_ratings = list(human_ratings_df[file[:-4]])
                        annotated_human_ratings, corresponding_metric_scores = [], []
                        for id, human_rating in enumerate(human_ratings):
                            if human_rating != 'None':
                                annotated_human_ratings.append(float(human_rating))
                                corresponding_metric_scores.append(float(metric_scores[id]))
                        cor, p_value = kendalltau(corresponding_metric_scores, annotated_human_ratings)
                        data_dict[file[:-4]] = f'{cor:.3f}'
                        
                    elif domain == 'tedtalks':
                        metric_scores = list(file_df[metric])
                        human_ratings_df = pd.read_csv(r'human_judgments_seg/all_TED_seg_mqm_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False) 
                        human_ratings = list(human_ratings_df[file[:-4]])
                        cor, p_value = kendalltau(metric_scores, human_ratings)
                        data_dict[file[:-4]] = f'{cor:.3f}'
                        
                else:
                    if domain == 'newstest2021' and 'metricsystem' not in file:
                        metric_scores = list(file_df[metric])
                        human_ratings_df = pd.read_csv(f'human_judgments_seg/all_news_seg_{human_judgment}_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False) 
                        human_ratings = list(human_ratings_df[file[:-4]])
                        annotated_human_ratings, corresponding_metric_scores = [], []
                        for id, human_rating in enumerate(human_ratings):
                            if human_rating != 'None':
                                annotated_human_ratings.append(float(human_rating))
                                corresponding_metric_scores.append(float(metric_scores[id]))
                        cor, p_value = kendalltau(corresponding_metric_scores, annotated_human_ratings)
                        data_dict[file[:-4]] = f'{cor:.3f}'
                                        
    print(data_dict) 
    all_values = []
    for value in data_dict.values():
        all_values.append(float(value))
    if human_judgment == 'mqm':
        average = sum(all_values) / 14
        print(f'Average: {average:.3f}')  
    else:
        average = sum(all_values) / 9
        print(f'Average: {average:.3f}')  
    
    
if __name__ == '__main__':

    metrics = ['sacre_BLEU', 'TER', 'CHRF2', 'BLEURT-20', 'COMET-MQM_2021', 'COMET-QE-MQM_2021']
    
    print("Segment-level Kendall's tau correlation with MQM scores")
    print('newstest2021:')
    print('==================')
    for metric in metrics:
        print(metric)
        compute_seg_correlation('newstest2021', metric, 'mqm')
        print('------------------')

    print()
    print('tedtalks:')
    print('==================')
    for metric in metrics:
        print(metric)
        compute_seg_correlation('tedtalks', metric, 'mqm')
        print('------------------')   
    
    print()
    print("Segment-level Kendall's tau correlation with raw DA scores")
    print('newstest2021:')
    print('==================')
    for metric in metrics:
        print(metric)
        compute_seg_correlation('newstest2021', metric, 'raw_da')
        print('------------------')
    
    print()
    print("Segment-level Kendall's tau correlation with z-normalized DA scores")
    print('newstest2021:')
    print('==================')
    for metric in metrics:
        print(metric)
        compute_seg_correlation('newstest2021', metric, 'z_da')
        print('------------------')
