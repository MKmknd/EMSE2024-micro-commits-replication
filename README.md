
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
bash clone.sh
```

After this process, please apply [cregit](https://github.com/cregit/cregit) to these repositories.
Finally, please commit the finall diff with a commit message 'cregit' (otherwise, you have to update some scripts that ignore the latest commit)
Then, you will get ``token repositories''. 
Please copy them into ``cregit_repository'' (this directory will be made by clone.sh)

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
Second, we computed the number of studied commits and one-line commits that are used in Table 1 in Section 2 (Motivating Example). 

```
cd ./../motivating_example
bash 01_oneline_commits.sh # output the data of Table 1
```

### Data collection
Third, we presented the basic statistics of micro commits and one-line commits, as depicted in Table 2 and Table 3.

```
cd ./../data_collection
python3 01_intersection.py
python3 02_make_table.py
```

### RQs and discussion
fourth, we conducted the experiments of RQs and discussion. 


RQ1

```
cd ./../rq1
bash 01_1_extract_micro_commits.sh 
python3 02_1_extract_changed_tokens.py 
bash 03_1_analyze.sh 
Rscript 03_2_analyze.R 
python3 04_1_make_data.py 
Rscript 05_1_analyze.R 
```

RQ2

```
cd ./../rq2
bash 01_num_single_multi_micro_commits.sh 
python3 02_make_table.py 
python3 03_multi_activity.py 
```

RQ3

```
cd ./../rq3
bash 01_heatmap.sh 
Rscript 01_heatmap.R 
bash 02_statistics.sh 
bash 03_check_value.sh
bash 04_01_extract_num_hunks.sh
Rscript 04_02_make_plot.R
```

Discussion

```
# before executing the following script, 
# you should get the data for nltk
# i.e., in Python
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
python3 01_1_prepare_data.py
python3 01_2_maintenance_commit.py
bash 01_show_data.sh 
python3 02_make_table.py 
mkdir plot
Rscript 03_make_barplot.R 
```