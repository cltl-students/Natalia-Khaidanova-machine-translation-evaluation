import pandas as pd
import os
from torchmetrics import SacreBLEUScore, TranslationEditRate, CHRFScore


news_data = pd.read_csv('../Data/all_news_data.tsv', sep='\t')
news_candidates = '../Data/WMT21-data/system-outputs/newstest2021'
news_references_A = list(news_data['news_ref_A'])
news_references_B = list(news_data['news_ref_B'])

all_news_references = []
for A, B in zip(news_references_A, news_references_B):
    all_news_references.append([A, B])

ted_data = pd.read_csv('../Data/all_TED_data.tsv', sep='\t')
ted_candidates = '../Data/WMT21-data/system-outputs/tedtalks'
ted_references = list(ted_data['TED_ref'])

bleu = SacreBLEUScore()
ter = TranslationEditRate()
chrf2 = CHRFScore()


for domain in ['newstest2021', 'tedtalks']:
    for metric in ['sacre_BLEU', 'TER', 'CHRF2']:
        if domain == 'newstest2021':
            
            news_data_dict = {}

            for file_name in os.listdir(news_candidates):
                if file_name[23:-3] not in ['ref-A', 'ref-B', '']:
                    news_data = pd.read_csv('../Data/all_news_data.tsv', sep='\t')
                    candidates = list(news_data[file_name[23:-3]])
                    candidates = [str(x) for x in candidates]
                    
                    if metric == 'sacre_BLEU':
                        sacre_bleu_score = bleu(candidates, all_news_references)
                        news_data_dict[file_name[23:-3]] = sacre_bleu_score.item()
                        
                    if metric == 'TER':
                        ter_score = ter(candidates, all_news_references)
                        news_data_dict[file_name[23:-3]] = ter_score.item()

                    if metric == 'CHRF2':
                        chrf2_score = chrf2(candidates, all_news_references)
                        news_data_dict[file_name[23:-3]] = chrf2_score.item()

            news_data = pd.DataFrame(news_data_dict, index=[0])
            news_data.to_csv(f'../Data/newstest2021/sys/sys_{metric}.tsv', sep='\t', index=False)
            
        if domain == 'tedtalks':
            ted_data_dict = {}
            sacre_references = []
            for reference in ted_references:
                sacre_references.append([reference])

            for file_name in os.listdir(ted_candidates):
                if file_name[19:-3] not in ['ref-A']:
                    ted_data = pd.read_csv('../Data/all_TED_data.tsv', sep='\t')
                    candidates = list(ted_data[file_name[19:-3]])
                  
                    if metric == 'sacre_BLEU':
                        sacre_bleu_score = bleu(candidates, sacre_references)
                        ted_data_dict[file_name[19:-3]] = sacre_bleu_score.item()
                        
                    if metric == 'TER':
                        ter_score = ter(candidates, sacre_references)
                        ted_data_dict[file_name[19:-3]] = ter_score.item()

                    if metric == 'CHRF2':
                        chrf2_score = chrf2(candidates, sacre_references)
                        ted_data_dict[file_name[19:-3]] = chrf2_score.item()

            ted_data = pd.DataFrame(ted_data_dict, index=[0])
            ted_data.to_csv(f'../Data/tedtalks/sys/sys_{metric}.tsv', sep='\t', index=False)
