import pandas as pd 


for file in ['baby_k.tsv', 'a_beautiful_mind.tsv']:

    data = f'Data/{file}'
    df = pd.read_csv(data, sep='\t') 

    sources = list(df['source'])
    human_translations = list(df['human_translation'])

    source_total_length = 0
    human_translation_total_length = 0
    num_segments = len(sources)

    for source, human_translation in zip(sources, human_translations):
        source_total_length += len(source)
        human_translation_total_length += len(human_translation)

    source_mean_length = source_total_length / num_segments
    human_translation_mean_length = human_translation_total_length / num_segments
    
    print(f'Mean source character length in {file}: {int(source_mean_length)}')
    print(f'Mean human translation character length in {file}: {int(human_translation_mean_length)}')
    print()
