
## Abstract

This is a replication package of the paper titled "An Empirical Study of Token-based Micro Commits" submitted to the EMSE in 2023.

## Dependency
Please go to python_packages/Utils and add this module to your Python environment, such as:

```
pip3 install -e .
```

This module has all common functions. 

## Data
The list of studied projects:
- Camel
- Hadoop
- Linux
- Zephyr

We investigated their repositories. 

Also, we put the list of studied micro commits (./micro_commits.csv)

## How to use

### Prepare the studied dataset
First, we have to prepare the studied dataset. 
So, we 
1. clone the repositories
2. apply cregit to these repositories
3. convert them into databases

```
cd ./prepare_dataset
bash clone.sh # 1 
```

After this process, please apply [cregit](https://github.com/cregit/cregit) to these repositories.
Finally, please commit the finall diff with a commit message 'cregit' (otherwise, you have to update some scripts that ignore the latest commit)
Then, you will get ``token repositories''. 
Please copy them into ``cregit_repository''

```
git config --global --add safe.directory '*'
python3 01_hash_pair.py # make hash pairs between original and token repositories
python3 02_cregit2org_table.py # add a table: commit_hash_pairs
python3 03_classify_diff_blocks.py # extract chunks from token repositories
python3 04_num_tokens_table.py # add a table: commit_token_sizes
python3 05_classify_diff_blocks.py # extract chunks from original repositories
python3 06_num_lines_table.py # add a table: commit_line_sizes
bash 07_do-dbs.sh # create all.db
```

So, you have the following directories:
- prepare_dataset/db # This directory has all databases
- prepare_dataset/repository # This directory has all studied repositories
- prepare_dataset/cregit_repository # This directory has all studied token repositories



### Motivating Example
Second, we computed the number of One-line commits and showed Table 1 in Section 2 (Motivating Example). 


```
cd ./../motivating_example
bash 01_oneline_commits.sh # output the data of Table 1
```


### RQs

Third, we conducted the experiments of RQ. 


RQ1

```
cd ./../rq1
bash 01_heatmap.sh # prepare the Figures 2, 3, and 4 data, and show the proportion of commits add-or-remove at most one token, three tokens, and five tokens (./data/maxtokenadded.csv)
Rscript 01_heatmap.R # create Figures 2, 3, and 4
bash 02_statistics.sh # show the statistics in the text in RQ1
python3 03_make_table.py # prepare Table 2 ('./tables/onetoken_commit_prop.csv')
```

RQ2

```
cd ./../rq2
bash 01_1_extract_micro_commits.sh # prepare a new database data
python3 02_1_extract_changed_tokens.py # make a new database
bash 03_1_analyze.sh # prepare a data to make the figures
Rscript 03_2_analyze.R # Figure 6
python3 04_1_make_data.py # Table 3
Rscript 05_1_analyze.R # Figure 5
```

RQ3

```
cd ./../rq3
# before executing the following script, 
# you should get the data for nltk
# i.e., in Python
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
python3 01_1_prepare_data.py
python3 01_2_maintenance_commit.py
bash 01_show_data.sh # show the data of Figure 7
python3 02_make_table.py # prepare the data of Figure 7
mkdir plot
Rscript 03_make_barplot.R # make Figure 7
bash 04_num_single_multi_micro_commits.sh # Table 6
python3 05_make_table.py # Table 7
python3 06_multi_activity.py # Table 8 and 9
```
