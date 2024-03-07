import sys
import re
import os
import sqlite3
import subprocess
from Utils import git_reader
from Utils import util
from string import punctuation
from nltk.corpus import stopwords
from nltk.corpus import wordnet
#from nltk.tokenize import word_tokenize
from nltk import word_tokenize
from nltk.stem import PorterStemmer

db_path = './../prepare_dataset/db/all.db'

def remove_punctuation(word_tokens):
    return [word for word in word_tokens if not word in punctuation]

def preprocess_text(text):
    """
    Preprocess a text. Concretely, this function applies the following processing:
    - tokenization
    - filtering out stop words
    - Using one term representing all synonymous
    - Stemming analysis

    All of them are implemented based on the NLTK toolkit

    Arguments:
    text [string] -- a text that we want to proprocess

    Returns:
    return token text [a list of stemmed words] -- proprocessed input text into one string separated by " "
    """
    stop_words = set(stopwords.words("english"))
    ps = PorterStemmer()

    text = text.lower()
    word_tokens = word_tokenize(text) # tokenization
    word_tokens = remove_punctuation(word_tokens) # remove punctuation
    filtered_word_tokens = [word for word in word_tokens if not word in stop_words] # filtering out stop words
    stemmed_word_tokens = [ps.stem(word) for word in filtered_word_tokens]

    return stemmed_word_tokens


def extract_dfc(data_list):
    # DONE: error, bug, fix, incorrect, fault, defect, flaw, type
    # issue -> issu
    # mistake -> mistak, mistaken, mistakenli
    # temp: default (fault), prefix (fix), debug (bug)
    #re_str = re.compile(".*(defect|flaw).*")
    #re_str = re.compile(".*(error|bug|fix|issue|mistake|incorrect|fault|defect|flaw|type).*")
    #re_str = re.compile(".*(error|bug|fix|issue|issu|mistake|mistak|incorrect|fault|defect|flaw|type).*")
    dfc_keyword_set = set(["error","bug","fix","issue","issu","mistake","mistak","incorrect","fault","defect","flaw","type"])
    dfc_keyword_list = ["error","bug","fix","issue","issu","mistake","mistak","incorrect","fault","defect","flaw","type"]
    commit_msg_list = []

    data_size = len(data_list)
    for idx, row in enumerate(data_list):
        if (idx%1000)==0:
            print("idx: {0:,}/{1:,}".format(idx, data_size))

        p_name = row[0]
        linecid = row[1]
        tokencid = row[2]

        repo_dir = "./repository/{0}".format(p_name)

        try:
            msg = git_reader.get_commit_message(repo_dir, linecid)
        except subprocess.CalledProcessError:
            print(row)
            sys.exit()

        stemmed_tokens_set = set(preprocess_text(msg))
        dfc_flag = False
        #for dfc_keyword in dfc_keyword_list:
        #    if not dfc_keyword in stemmed_tokens_set:
        #        continue
        #    dfc_flag = True
        #    break
        if len(dfc_keyword_set & stemmed_tokens_set)>0:
            dfc_flag = True
        
        out_keyword_dict = {"error": False, "bug": False, "fix": False, "issue": False, "issu": False, "mistake": False, "mistak": False, "incorrect": False, "fault": False, "defect": False, "flaw": False, "type": False}
        for key in dfc_keyword_set & stemmed_tokens_set:
            out_keyword_dict[key] = True

        record = [p_name, linecid, tokencid, msg, dfc_flag]
        for key in dfc_keyword_list:
            record.append(out_keyword_dict[key])

        commit_msg_list.append(tuple(record))

        if (idx%100000)==0:
            util.dump_pickle('./data/back.pickle', commit_msg_list)


    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS commit_msg;") 
    cur.execute("CREATE TABLE commit_msg(project TEXT, linecid TEXT, tokencid TEXT, msg, dfc_flag, error, bug, fix, issue, issu, mistake, mistak, incorrect, fault, defect, flaw, type, PRIMARY KEY (linecid));")
    cur.executemany('INSERT INTO commit_msg(project, linecid, tokencid, msg, dfc_flag, error, bug, fix, issue, issu, mistake, mistak, incorrect, fault, defect, flaw, type) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', commit_msg_list)
    conn.commit()
    conn.close()
        


def extract_commits():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    command = """
              SELECT project, linecid, tokencid
              FROM token_commit_summary
              """
    cur.execute(command)
    return_list = []
    for row in cur.fetchall():
        return_list.append(row)
    conn.close()

    return return_list


def main():

    if not os.path.exists('./data'): os.makedirs('./data')
    data_list = extract_commits()
    extract_dfc(data_list)

if __name__=="__main__":
    main()


