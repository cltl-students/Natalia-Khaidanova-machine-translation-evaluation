import pandas as pd
import os 


domains = ['newstest2021','tedtalks']
metrics = ['BLEURT-20','COMET-MQM_2021','COMET-QE-MQM_2021']

for domain in domains:
    for metric in metrics:
    
        data_dict = {}
        metric_path = f'../Data/{domain}/sys/sys_{metric}.tsv'

        if os.path.exists(metric_path):
            continue

        for file_name in os.listdir(f'../Data/{domain}/{metric}'):
            if file_name.endswith('.tsv'):

                df = pd.read_csv(f'../Data/{domain}/{metric}/{file_name}', sep='\t') 

                if metric in ['BLEURT-20','COMET-MQM_2021'] and domain == 'newstest2021':
                    ref_A = list(df[f'{metric}_ref_A'])
                    ref_B = list(df[f'{metric}_ref_B'])
                    system_score = (sum(ref_A) + sum(ref_B)) / (len(ref_A) + len(ref_B))
                    if metric == 'BLEURT-20':
                        data_dict[file_name[:-14]] = system_score
                    if metric == 'COMET-MQM_2021':
                        data_dict[file_name[:-19]] = system_score

                if metric in ['BLEURT-20','COMET-MQM_2021'] and domain == 'tedtalks':
                    segment_scores = list(df[metric])
                    system_score = sum(segment_scores) / len(segment_scores)
                    if metric == 'BLEURT-20':
                        data_dict[file_name[:-14]] = system_score
                    if metric == 'COMET-MQM_2021':
                        data_dict[file_name[:-19]] = system_score

                if metric == 'COMET-QE-MQM_2021':
                    segment_scores = list(df['COMET-QE-MQM_2021'])
                    system_score = sum(segment_scores) / len(segment_scores)
                    data_dict[file_name[:-22]] = system_score

        metric_data = pd.DataFrame(data_dict, index=[0])
        metric_data.to_csv(f'../Data/{domain}/sys/sys_{metric}.tsv', sep='\t', index=False)
