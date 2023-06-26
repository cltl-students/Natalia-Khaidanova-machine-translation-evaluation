import pandas as pd
import os


# GET SOURCE, REFERENCE(S), MACHINE-TRANSLATION OUTPUTS PER DOMAIN
def read_file(file_path):
    """
    Read the data.
    
    :param string file_path: path to the file
    :return: list of strings (sentences)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [line.strip() for line in f.readlines()]
    return data
  
  
news_source = r'WMT21-data/sources/newstest2021.en-ru.src.en'
news_reference_A = r'WMT21-data/references/newstest2021.en-ru.ref.ref-A.ru'
news_reference_B = r'WMT21-data/references/newstest2021.en-ru.ref.ref-B.ru'
news_candidates = r'WMT21-data/system-outputs/newstest2021'

ted_source = r'WMT21-data/sources/tedtalks.en-ru.src.en'
ted_reference = r'WMT21-data/references/tedtalks.en-ru.ref.ref-A.ru'
ted_candidates = r'WMT21-data/system-outputs/tedtalks'


news_source = read_file(news_source)
news_reference_A = read_file(news_reference_A)
news_reference_B = read_file(news_reference_B)

ted_source = read_file(ted_source)
ted_reference = read_file(ted_reference)


news_data_dict = {'news_source':news_source,
                  'news_ref_A':news_reference_A,
                  'news_ref_B':news_reference_B}

ted_data_dict = {'TED_source':ted_source,
                 'TED_ref':ted_reference}

                   
for news_file_name in os.listdir(news_candidates):
    for ted_file_name in os.listdir(ted_candidates):
      
        news_file_path = os.path.join(news_candidates, news_file_name)
        ted_file_path = os.path.join(ted_candidates, ted_file_name)
        
        news_candidate = read_file(news_file_path)
        ted_candidate = read_file(ted_file_path)
        
        if news_file_name[23:-3] not in ['ref-A','ref-B']:
            news_data_dict[news_file_name[23:-3]] = news_candidate
        if ted_file_name[19:-3] != 'ref-A':
            ted_data_dict[ted_file_name[19:-3]] = ted_candidate


news_df = pd.DataFrame(news_data_dict)
news_df.to_csv('all_news_data.tsv', sep='\t', index=False) 

ted_df = pd.DataFrame(ted_data_dict)
ted_df.to_csv('all_TED_data.tsv', sep='\t', index=False)


# GET HUMAN JUDGMENTS PER TYPE AND DOMAIN
newstest2021_file_path_1 = r'WMT21-data/evaluation/newstest2021/en-ru.mqm.seg.score'
newstest2021_file_path_2 = r'WMT21-data/evaluation/newstest2021/en-ru.wmt-raw.seg.score'
newstest2021_file_path_3 = r'WMT21-data/evaluation/newstest2021/en-ru.wmt-z.seg.score'

newstest2021_file_path_4 = r'WMT21-data/evaluation/newstest2021/en-ru.mqm.sys.score'
newstest2021_file_path_5 = r'WMT21-data/evaluation/newstest2021/en-ru.wmt-raw.sys.score'
newstest2021_file_path_6 = r'WMT21-data/evaluation/newstest2021/en-ru.wmt-z.sys.score'

tedtalks_file_path_1 = r'WMT21-data/evaluation/tedtalks/en-ru.mqm.seg.score'

tedtalks_file_path_2 = r'WMT21-data/evaluation/tedtalks/en-ru.mqm.sys.score'


def get_scores(file_path, systems, scores):
    """
    Put human judgment scores for each system in a dict.
    
    :param systems: list of machine-translation systems
    :param scores: list of human judgment scores
    :return: two dicts: for newstest2021 and for tedtalks
    """
    news_data_dict, ted_data_dict = {}, {}

    for system, score in zip(systems, scores):
        
        if 'news' in file_path:
            if system not in ['refA','refB']:
                if system not in news_data_dict:
                    news_data_dict[system] = []
                news_data_dict[system].append(score)

        if 'tedtalks' in file_path:
            if system != 'refA':
                if system not in ted_data_dict:
                    ted_data_dict[system] = []
                ted_data_dict[system].append(score)
            
    return news_data_dict, ted_data_dict


def save_scores(file_path, correlation, score_type):
    """
    Save all scores per system in a .tsv file. 
    
    :param string file_path: path to the validation file
    :param string correlation: if segment-level, correlation == 'seg'; if system-level, correlation == 'sys'
    :param string score_type: type of human judgment scores ('mqm', 'raw_da', or 'z_da')
    :return: None
    """

    if correlation == 'seg':

        labels = ['system','score']
        data = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', keep_default_na=False, names=labels) 
        
        systems = list(data['system'])
        scores = list(data['score'])
        
        news_data_dict, ted_data_dict = get_scores(file_path, systems, scores)
        
        if 'news' in file_path:
            news_df = pd.DataFrame(news_data_dict)
            news_df.to_csv(f'../eval/human_judgments_seg/all_news_seg_{score_type}_scores.tsv', sep='\t', index=False) 
            
        if 'tedtalks' in file_path:
            ted_df = pd.DataFrame(ted_data_dict)
            ted_df.to_csv('../eval/human_judgments_seg/all_TED_seg_mqm_scores.tsv', sep='\t', index=False) 

    if correlation == 'sys':

        labels = ['system','score']
        data = pd.read_csv(file_path, sep='\t', on_bad_lines='skip', keep_default_na=False, names=labels) 

        systems = list(data['system'])
        scores = list(data['score'])
        
        news_data_dict, ted_data_dict = get_scores(file_path, systems, scores)
        
        if 'news' in file_path:
            news_df = pd.DataFrame(news_data_dict)
            news_df.to_csv(f'../eval/human_judgments_sys/all_news_sys_{score_type}_scores.tsv', sep='\t', index=False) 
        if 'tedtalks'in file_path:
            ted_df = pd.DataFrame(ted_data_dict)
            ted_df.to_csv('../eval/human_judgments_sys/all_TED_sys_mqm_scores.tsv', sep='\t', index=False) 
            
            
if __name__ == '__main__':
    save_scores(newstest2021_file_path_1, 'seg', 'mqm')
    save_scores(newstest2021_file_path_2, 'seg', 'raw_da')
    save_scores(newstest2021_file_path_3, 'seg', 'z_da')
    
    save_scores(newstest2021_file_path_4, 'sys', 'mqm')
    save_scores(newstest2021_file_path_5, 'sys', 'raw_da')
    save_scores(newstest2021_file_path_6, 'sys', 'z_da')
    
    save_scores(tedtalks_file_path_1, 'seg', 'mqm')
    save_scores(tedtalks_file_path_2, 'sys', 'mqm')
