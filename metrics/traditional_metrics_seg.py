import pandas as pd
import os
from torchmetrics import SacreBLEUScore, TranslationEditRate, CHRFScore


news_data = pd.read_csv(r'../Data/all_news_data.tsv', sep='\t') 
news_candidates = '../Data/WMT21-data/system-outputs/newstest2021'
news_references_A = list(news_data['news_ref_A'])
news_references_B = list(news_data['news_ref_B'])

all_news_references = []
for A, B in zip(news_references_A, news_references_B):
    all_news_references.append([A, B])
    
ted_data = pd.read_csv(r'../Data/all_TED_data.tsv', sep='\t') 
ted_candidates = '../Data/WMT21-data/system-outputs/tedtalks'
ted_references = list(ted_data['TED_ref'])

sacre_bleu = SacreBLEUScore()
ter = TranslationEditRate()
chrf2 = CHRFScore()


news_scores, ted_scores = [], []

for file_name in os.listdir(news_candidates):
    if file_name[23:-3] not in ['ref-A','ref-B','']:

        data_dict = {}
        sacre_bleu_scores, ter_scores, chrf2_scores = [], [], []
        candidates = list(news_data[file_name[23:-3]])

        for references, candidate in zip(all_news_references, candidates):
            try:
                # SacreBLEU
                sacre_bleu_score = sacre_bleu([candidate], [references])
                sacre_bleu_score = sacre_bleu_score.item()
                sacre_bleu_scores.append(f'{sacre_bleu_score:.2f}')
                # TER
                ter_score = ter([candidate], [references])
                ter_score = ter_score.item()
                ter_scores.append(f'{ter_score:.2f}')
                # CHRF2
                chrf2_score = chrf2([candidate], [references])
                chrf2_score = chrf2_score.item()
                chrf2_scores.append(f'{chrf2_score:.2f}')

            except Exception:
                sacre_bleu_scores.append('0.00')
                ter_scores.append('0.00')
                chrf2_scores.append('0.00')

        data_dict['sacre_BLEU'] = sacre_bleu_scores
        data_dict['TER'] = ter_scores
        data_dict['CHRF2'] = chrf2_scores
        news_scores.append(data_dict)

        news_data = pd.DataFrame(data_dict)
        news_data.to_csv(f'../Data/newstest2021/traditional_metrics/{file_name[23:-3]}.tsv', sep='\t', index=False) 
    
for file_name in os.listdir(ted_candidates):
    if file_name[19:-3] != 'ref-A':

        data_dict = {}
        sacre_bleu_scores, ter_scores, chrf2_scores = [], [], []
        candidates = list(ted_data[file_name[19:-3]])

        for reference, candidate in zip(ted_references, candidates):
            sacre_bleu_score = sacre_bleu([candidate], [[reference]])
            sacre_bleu_score = sacre_bleu_score.item()
            sacre_bleu_scores.append(f'{sacre_bleu_score:.2f}')

            ter_score = ter([candidate], [[reference]])
            ter_score = ter_score.item()
            ter_scores.append(f'{ter_score:.2f}')

            chrf2_score = chrf2([candidate], [[reference]])
            chrf2_score = chrf2_score.item()
            chrf2_scores.append(f'{chrf2_score:.2f}')

        data_dict['sacre_BLEU'] = sacre_bleu_scores
        data_dict['TER'] = ter_scores
        data_dict['CHRF2'] = chrf2_scores
        ted_scores.append(data_dict)

        ted_data = pd.DataFrame(data_dict)
        ted_data.to_csv(f'../Data/tedtalks/traditional_metrics/{file_name[19:-3]}.tsv', sep='\t', index=False) 
