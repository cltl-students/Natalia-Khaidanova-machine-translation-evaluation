import pandas as pd
import os 


def get_nr_annotations(domain, human_judgment):
    """
    Get number of annotated segments per domain and human judgment type.
    
    :param sting domain: 'newstest2021' or 'tedtalks'
    :param sting human_judgment: human judgment type ('mqm', 'raw_da', 'z_da') 
    :return: None
    """
    path = f'../Data/{domain}/traditional_metrics'
    for file in os.listdir(path):
        if file.endswith('.tsv'):
            if human_judgment == 'mqm':
                if domain == 'newstest2021':

                    human_ratings_df = pd.read_csv(f'human_judgments_seg/all_news_seg_{human_judgment}_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False)
                    human_ratings = list(human_ratings_df[file[:-4]])
                    annoated_human_ratings = []
                    for human_rating in human_ratings:
                        if human_rating != 'None':
                            annoated_human_ratings.append(float(human_rating))
                    print(f'{file[:-4]}: {len(annoated_human_ratings)}')
                    
                elif domain == 'tedtalks':  

                    human_ratings_df = pd.read_csv(f'human_judgments_seg/all_TED_seg_mqm_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False)
                    human_ratings = list(human_ratings_df[file[:-4]])
                    annoated_human_ratings = []
                    for human_rating in human_ratings:
                        if human_rating != 'None':
                            annoated_human_ratings.append(float(human_rating))
                    print(f'{file[:-4]}: {len(annoated_human_ratings)}')
                    
            else:
                if domain == 'newstest2021' and 'metricsystem' not in file:

                    human_ratings_df = pd.read_csv(f'human_judgments_seg/all_news_seg_{human_judgment}_scores.tsv', sep='\t', on_bad_lines='skip', keep_default_na=False)
                    human_ratings = list(human_ratings_df[file[:-4]])
                    annoated_human_ratings = []
                    for human_rating in human_ratings:
                        if human_rating != 'None':
                            annoated_human_ratings.append(float(human_rating))
                    print(f'{file[:-4]}: {len(annoated_human_ratings)}')
   

if __name__ == '__main__':
    print('Number of MQM annotated segments for newstest2021:')
    get_nr_annotations('newstest2021', 'mqm')
    print('------------------')
    print()
    print('Number of MQM annotated segments for tedtalks:')
    get_nr_annotations('tedtalks', 'mqm')
    print('------------------')
    print()
    print('Number of raw DA annotated segments for newstest2021:')
    get_nr_annotations('newstest2021', 'raw_da')
    print('------------------')
    print()
    print('Number of z-normalized DA annotated segments for newstest2021:')
    get_nr_annotations('newstest2021', 'z_da')
