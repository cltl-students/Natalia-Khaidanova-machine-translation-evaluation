import pandas as pd
from transformers import MarianMTModel, MarianTokenizer


model_name = 'Helsinki-NLP/opus-mt-en-ru'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

for file in ['baby_k.tsv', 'a_beautiful_mind.tsv']:

    df = pd.read_csv(f'Data/{file}', sep='\t')
    source = list(df['source'])
    
    translated = model.generate(**tokenizer(source, return_tensors="pt", padding=True))

    opus_mt_translations = []
    for sentence in translated:
        opus_mt_translations.append(tokenizer.decode(sentence, skip_special_tokens=True))
        
    df['opus_mt_translation'] = opus_mt_translations
    df.to_csv(f'Data/{file}', sep='\t', index=False)
