import pandas as pd
import os
from torchmetrics import SacreBLEUScore, TranslationEditRate, CHRFScore
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

sacre_bleu = SacreBLEUScore()
ter = TranslationEditRate()
chrf2 = CHRFScore()


def get_traditional_metrics_runtime(data, candidates, all_references, metric):
    """
    Get metric's scores for all candidates and systems in the system-outputs folder,
    get the time needed to produce these scores. N.B.! The scores won't be saved. 

    :param pandas.core.frame.DataFrame data: pandas dataframe of either all_news_data.tsv or all_TED_data.tsv
    :param str candidates: path to the folder with system outputs
    :param list all_references: list (of lists) of reference translations
    :param str metric: metric's name (sacre_BLEU, TER, or CHRF2)
    :return: None
    """
    start_time = time.time()
    all_scores = []
    count = 0

    for file_name in os.listdir(candidates):
        # get the scores for the newstest2021 data
        if 'newstest2021' in candidates and file_name[23:-3] not in ['ref-A','ref-B','']:

            count += 1
            data_dict, scores = {}, []
            file_candidates = list(data[file_name[23:-3]])

            for references, candidate in zip(all_references, file_candidates):
                
                if metric == 'sacre_BLEU':
                    try:
                        sacre_bleu_score = sacre_bleu([candidate], [references])
                        sacre_bleu_score = sacre_bleu_score.item()
                        scores.append(f'{sacre_bleu_score:.2f}')
                    except Exception:
                        scores.append('0.00')

                if metric == 'TER':
                    try:
                        ter_score = ter([candidate], [references])
                        ter_score = ter_score.item()
                        scores.append(f'{ter_score:.2f}')
                    except Exception:
                        scores.append('0.00')

                if metric == 'CHRF2':
                    try:
                        chrf2_score = chrf2([candidate], [references])
                        chrf2_score = chrf2_score.item()
                        scores.append(f'{chrf2_score:.2f}')
                    except Exception:
                        scores.append('0.00')

            data_dict[metric] = scores
            all_scores.append(data_dict)

            if count == 3:
                print('three files are processed')
            if count == 7:
                print('half of the files is processed')
            if count == 11:
                print('almost done')

        # get the scores for the tedtalks data
        if 'tedtalks' in candidates and file_name[19:-3] not in ['ref-A','']:

            count += 1
            data_dict, scores = {}, []
            file_candidates = list(data[file_name[19:-3]])

            for reference, candidate in zip(all_references, file_candidates):

                if metric == 'sacre_BLEU':
                    sacre_bleu_score = sacre_bleu([candidate], [[reference]])
                    sacre_bleu_score = sacre_bleu_score.item()
                    scores.append(f'{sacre_bleu_score:.2f}')

                if metric == 'TER':
                    ter_score = ter([candidate], [[reference]])
                    ter_score = ter_score.item()
                    scores.append(f'{ter_score:.2f}')

                if metric == 'CHRF2':
                    chrf2_score = chrf2([candidate], [[reference]])
                    chrf2_score = chrf2_score.item()
                    scores.append(f'{chrf2_score:.2f}')

            data_dict[metric] = scores
            all_scores.append(data_dict)

            if count == 3:
                print('three files are processed')
            if count == 7:
                print('half of the files is processed')
            if count == 11:
                print('almost done')

    end_time = time.time()
    total_time = end_time - start_time
    print('Time taken', f'for {metric}:', f'{total_time:.2f}', 'seconds')


if __name__ == '__main__':
    print('newstest2021 data:')
    print('==================')
    get_traditional_metrics_runtime(news_data, news_candidates, all_news_references, 'sacre_BLEU')
    print('------------------')
    get_traditional_metrics_runtime(news_data, news_candidates, all_news_references, 'TER')
    print('------------------')
    get_traditional_metrics_runtime(news_data, news_candidates, all_news_references, 'CHRF2')
    print('------------------')
    print('tedtalks data:')
    print('==================')
    get_traditional_metrics_runtime(ted_data, ted_candidates, ted_references, 'sacre_BLEU')
    print('------------------')
    get_traditional_metrics_runtime(ted_data, ted_candidates, ted_references, 'TER')
    print('------------------')
    get_traditional_metrics_runtime(ted_data, ted_candidates, ted_references, 'CHRF2')
    print('------------------')
