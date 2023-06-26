<h1>Machine-Translation Evaluation: Comparing Traditional and Neural Machine-Translation Evaluation Metrics for English→Russian</h1>

Machine translation (MT) has become increasingly popular in recent years due to advances in technology and growing globalization. As the quality of MT continues to improve, more and more companies are turning to this method over human translation to save time and money. However, the increasing reliance on MT has also highlighted the need for automatic evaluation algorithms that can accurately measure its quality. Developing such algorithms is essential in ensuring that MT can effectively meet the needs of businesses and individuals in the global marketplace, as well as in comparing different MT algorithms against each other and tracking their improvements over time. MT evalaution metrics are an indispensable component of these automatic evaluation algorithms. 

This repository is part of the thesis project for the Master's Degree in "Linguistics: Text Mining" at the Vrije Universiteit Amsterdam (2022-2023). The project focuses on replicating and reproducing selected research conducted at the WMT21 Metrics Shared Task. The replication involves evaluating the traditional (SacreBLEU, TER, and CHRF2) and best-performing reference-based (BLEURT-20, COMET-MQM_2021) and reference-free (COMET-QE-MQM_2021) neural metrics. The evaluation is conducted across two domains: news articles and TED talks translated from English into Russian. By examining the performance of these metrics, we aim to understand their effectiveness and suitability in different translation contexts. Furthermore, the thesis project goes beyond the initial evaluation and explores the applicability of reference-free neural metrics, with a particular focus on COMET-QE-MQM_2021, for professional human translators. This extended evaluation is performed on a distinct domain, namely scientific articles. The articles are translated in the same direction as the primary data. 

Creator: [Natalia Khaidanova](https://github.com/NataliaKhaidanova)

Supervisor: Sophie Arnoult 

<h2>Content</h2>

<h2>\Data</h2>

The [data](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data) folder contains:

<h3>Files:</h3>

- [all_TED_data.tsv](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/Data/all_TED_data.tsv) stores all source sentences, reference translations, and MTs presented at the WMT21 Metrics Task for the TED talks domain.  

- [all_news_data.tsv](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/Data/all_news_data.tsv) stores all source sentences, reference translations, and MTs presented at the WMT21 Metrics Task for the news domain.

- [create_data_files.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/Data/create_data_files.py) creates [all_TED_data.tsv](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/Data/all_TED_data.tsv) and [all_news_data.tsv](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/Data/all_news_data.tsv) files, converts the WMT21 Metrics Task human judgments per type (MQM, raw DA, and z-normalized DA) and domain (news and TED talks) into .tsv files. The files are stored in [human_judgments_seg](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/eval/human_judgments_seg) (segment-level human judgments) and [human_judgments_sys](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/eval/human_judgments_sys) (system-level human judgments). 

<h3>Subfolders:</h3>

- [WMT21-data](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/WMT21-data) stores source sentences ([sources](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/WMT21-data/sources)), reference translations ([references](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/WMT21-data/references)), MTs ([system-outputs](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/WMT21-data/system-outputs)), and human judgment scores ([evaluation](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/WMT21-data/evaluation)) for each domain (news and TED talks). 

- [newstest2021](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021) contains segment-level scores for each implemented neural metric ([BLEURT-20](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/BLEURT-20), [COMET-MQM_2021](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/COMET-MQM_2021), and [COMET-QE-MQM_2021](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/COMET-QE-MQM_2021)) and all utilized traditional metrics ([traditional metrics](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/traditional_metrics)), as well as [system-level scores](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/sys) for each of these metrics. Domain: news. 

- [tedtalks](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks) contains segment-level scores for each implemented neural metric ([BLEURT-20](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/BLEURT-20), [COMET-MQM_2021](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/COMET-MQM_2021), and [COMET-QE-MQM_2021](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/COMET-QE-MQM_2021)) and all utilized traditional metrics ([traditional metrics](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/traditional_metrics)), as well as [system-level scores](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/sys) for each of these metrics. Domain: TED talks. 

<h2>\eval</h2>

The [eval](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/eval) folder contains: 

<h3>Files:</h3>

- [get_nr_annotations.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/eval/get_nr_annotations.py) checks the number of annotated segments in the WMT21 Metrics Task data per type of human judgment (MQM, raw DA, or z-normalized DA). 

- [seg_eval.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/eval/seg_eval.py) runs a segment-level evaluation of the implemented neural (BLEURT-20, COMET-MQM_2021, and COMET-QE-MQM_2021) and traditional (SacreBLEU, TER, and CHRF2) metrics. 

- [sys_eval.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/eval/sys_eval.py) runs a system-level evaluation of the implemented neural (BLEURT-20, COMET-MQM_2021, and COMET-QE-MQM_2021) and traditional (SacreBLEU, TER, and CHRF2) metrics. 

<h3>Subfolders:</h3>

- [human_judgments_seg](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/eval/human_judgments_seg) stores segment-level human judgment scores of each type (MQM, raw DA, or z-normalized DA) in separate .tsv files. The scores are presented for both news and TED talks.
  
- [human_judgments_sys](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/eval/human_judgments_sys) stores system-level human judgment scores of each type (MQM, raw DA, or z-normalized DA) in separate .tsv files. The scores are presented for both news and TED talks.

<h2>\metrics</h2>

The [metrics](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/metrics) folder contains: 

<h3>Files:</h3>

- [BLEURT-20.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/metrics/BLEURT-20.py) computes segment-level scores for the reference-based neural metric BLEURT-20 on the WMT21 Metrics Task data and calculates the metric's runtime per MT system. The resulting segment-level scores and metric's runtime are stored in [BLEURT-20 (newstest2021)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/BLEURT-20) and [BLEURT-20 (tedtalks)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/BLEURT-20). 

- [COMET-MQM_2021.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/metrics/COMET-MQM_2021.py) computes segment-level scores for the reference-based neural metric COMET-MQM_2021 on the WMT21 Metrics Task data and calculates the metric's runtime per MT system. The resulting segment-level scores and metric's runtime are stored in [COMET-MQM_2021 (newstest2021)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/COMET-MQM_2021) and [COMET-MQM_2021 (tedtalks)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/COMET-MQM_2021). 
  
- [COMET-QE-MQM_2021.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/metrics/COMET-QE-MQM_2021.py) computes segment-level scores for the reference-free neural metric COMET-QE-MQM_2021 on the WMT21 Metrics Task data and calculates the metric's runtime per MT system. The resulting segment-level scores and metric's runtime are stored in [COMET-QE-MQM_2021 (newstest2021)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/COMET-QE-MQM_2021) and [COMET-QE-MQM_2021 (tedtalks)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/COMET-QE-MQM_2021).

- [get_sys_scores.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/metrics/get_sys_scores.py) computes system-level scores for the neural metrics (BLEURT-20, COMET-MQM_2021, and COMET-QE-MQM_2021) on the WMT21 Metrics Task data. The system-level scores are obtained by averaging the metrics' segment-level scores. The resulting system-level scores are stored in [sys (newstest2021)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/sys) and [sys (tedtalks)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/sys). 

- [traditional_metrics_seg.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/metrics/traditional_metrics_seg.py) computes segment-level scores for the traditional metrics (SacreBLEU, TER, and CHRF2) on the WMT21 Metrics Task data. The resulting segment-level scores are stored in [traditional_metrics (newstest2021)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/traditional_metrics) and [traditional_metrics (tedtalks)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/traditional_metrics).

- [traditional_metrics_sys.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/metrics/traditional_metrics_sys.py) computes system-level scores for the traditional metrics (SacreBLEU, TER, and CHRF2) on the WMT21 Metrics Task data. The resulting system-level scores are stored in [sys (newstest2021)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/sys) and [sys (tedtalks)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/sys). 

- [traditional_metrics_runtime.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/metrics/traditional_metrics_runtime.py) calculates the traditional metrics' (SacreBLEU, TER, and CHRF2) runtimes for segment-level evaluation. The runtimes are determined for all MT systems per domain (news and TED talks). The metrics' runtimes are stored in [traditional_metrics (newstest2021)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/newstest2021/traditional_metrics) and [traditional_metrics (tedtalks)](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/Data/tedtalks/traditional_metrics).

<h2>\reference-free_eval</h2>

The [reference-free_eval](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/reference-free_eval) folder contains: 

<h3>Files:</h3>

- [COMET-QE-MQM_2021.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/COMET-QE-MQM_2021.py) computes segment- and system-level scores of the reference-free neural metric COMET-QE-MQM_2021 on the additional data comprising two scientific articles ([Baby K](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/Data/baby_k.tsv) and [A Beautiful Mind](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/Data/a_beautiful_mind.tsv)). The metric evaluates both human and machine translations. Note that the source sentences and their human translations were added to the files manually. 

- [add_opus_mt_translations.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/add_opus_mt_translations.py) adds MTs produced by the opus-mt-en-ru MT system to the data comprising two scientific articles ([Baby K](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/Data/baby_k.tsv) and [A Beautiful Mind](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/Data/a_beautiful_mind.tsv)).

- [get_mean_length.py](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/get_mean_length.py) counts the mean character length of the source sentences and their human translations in the [Baby K](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/Data/baby_k.tsv) and [A Beautiful Mind](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/Data/a_beautiful_mind.tsv) articles. 

<h3>Subfolders:</h3>

- [Data](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/tree/main/reference-free_eval/Data) contains two scientific articles ([Baby K](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/Data/baby_k.tsv) and [A Beautiful Mind](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/reference-free_eval/Data/a_beautiful_mind.tsv)), each comprising English source sentences, their corresponding Russian human translations and MTs produced by the opus-mt-en-ru MT system. The files were created with the aim of evaluating the applicability of reference-free neural metrics, specifically COMET-QE-MQM_2021, for professional human translators. The subfolder also stores the segment- and system-level scores produced by COMET-QE-MQM_2021 for both human and machine translations.

<h2>requirements.txt</h2>

The [requirements.txt](https://github.com/NataliaKhaidanova/MT_evaluation_metrics/blob/main/requirements.txt) file contains information about the packages and models required to run and evaluate the implemented traditional (SacreBLEU, TER, and CHRF2) and neural (BLEURT-20, COMET-MQM_2021, and COMET-QE-MQM_2021) metrics. It also lists additional packages needed to run all the .py files in the repository. 

<h2>Natalia_Khaidanova_2778662_Thesis.pdf</h2>

The [Natalia_Khaidanova_2778662_Thesis.pdf](https://github.com/NataliaKhaidanova/machine-translation-evaluation/blob/main/Natalia_Khaidanova_2778662_Thesis.pdf) file contains the thesis report outlining the results of the research. 

<h2>References</h2>

- Markus Freitag, Ricardo Rei, Nitika Mathur, Chi-kiu Lo, Craig Stewart, George Foster, Alon Lavie, and Ondřej Bojar. 2021. [Results of the WMT21 Metrics Shared Task: Evaluating Metrics with Expert-based Human Evaluations on TED and News Domain](https://aclanthology.org/2021.wmt-1.73v3.pdf ). *In Proceedings of the Sixth Conference on Machine Translation*, pages 733–774, Online. Association for Computational Linguistics. 
