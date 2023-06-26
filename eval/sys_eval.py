import csv
import os
from scipy.stats import pearsonr


def get_systems_and_scores(file_path):
    """
    Help function. 
    Store all systems and their corresponding system-level scores in two separate lists.
    
    :param sting file_path: path to the file with metric system-level scores
    :return: two lists (list of systems and list of their corresponding system-level scores)
    """
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        systems = next(reader)  
        for row in reader:
            scores = [float(x) for x in row]
        
        return systems, scores
    
    
def compute_sys_correlation(domain, human_judgment):
    """
    Compute system-level Pearson's r and Spearman's p for 
    SacreBLEU, TER, CHRF2, BLEURT-20, COMET-MQM_2021, COMET-QE-MQM_2021.
    Get the correlation for both newstest2021 and tedtalks datasets. 
    
    :param sting domain: domain to compute the correlation for ('newstest2021' or 'tedtalks')
    :param sting human_judgment: human judgment type ('mqm', 'raw_da', 'z_da') 
    :return: None
    """
    if domain == 'newstest2021':
        ratings = f'human_judgments_sys/all_news_sys_{human_judgment}_scores.tsv'
    if domain == 'tedtalks':
        ratings = f'human_judgments_sys/all_TED_sys_mqm_scores.tsv'
    
    unstructured_hj_systems, unstructured_hj_scores = get_systems_and_scores(ratings)
    
    for file_name in os.listdir(f'../Data/{domain}/sys'):
        if file_name.endswith('.tsv'):

            unstructured_metric_systems, unstructured_metric_scores = get_systems_and_scores(f'../Data/{domain}/sys/{file_name}')

            structured_hj_scores, structured_metric_scores = [], []

            for hj_system, hj_score in zip(unstructured_hj_systems, unstructured_hj_scores):
                for metric_system, metric_score in zip(unstructured_metric_systems, unstructured_metric_scores):
                    if hj_system == metric_system:
                        structured_hj_scores.append(hj_score)
                        structured_metric_scores.append(metric_score)

            r, p_value = pearsonr(structured_metric_scores, structured_hj_scores)

            print(f"{file_name[4:-4]}: Pearson's r {r:.3f}")

    
if __name__ == '__main__':
    print('System-level correlation with MQM scores:')
    print('newstest2021:')
    print('==================')
    compute_sys_correlation('newstest2021', 'mqm')
    print('------------------')
    
    print()
    print('tedtalks:')
    print('==================')
    compute_sys_correlation('tedtalks', 'mqm')
    print('------------------')
    
    print()
    print('System-level correlation with raw DA scores:')
    print('newstest2021:')
    print('==================')
    compute_sys_correlation('newstest2021', 'raw_da')
    print('------------------')
    
    print()
    print('System-level correlation with z-normalized DA scores:')
    print('newstest2021:')
    print('==================')
    compute_sys_correlation('newstest2021', 'z_da')
    print('------------------')
