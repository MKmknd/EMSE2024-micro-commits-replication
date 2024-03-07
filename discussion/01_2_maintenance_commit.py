import os
import sqlite3
from Utils import util
from string import punctuation
from nltk.corpus import stopwords
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


def keyword_check(keyword_set, token_set, out_keyword_dict):

    if len(keyword_set & token_set)>0:
        for key in keyword_set & token_set:
            out_keyword_dict[key] = True
        return True
    return False

def extract_maintenance(data_list):
    corrective_keyword_list = ['fix', 'esolv', 'clos', 'handl', 'issue', 'defect', 'bug', 'problem', 'ticket']
    corrective_keyword_set = set(corrective_keyword_list)

    perfective_keyword_list = ['refactor', 're-factor', 'reimplement', 're-implement', 'design', 'replac', 'modify', 'updat', 'upgrad', 'cleanup', 'clean-up']
    perfective_keyword_set = set(perfective_keyword_list)

    adaptive_keyword_list = ['add', 'new', 'introduc', 'implement', 'implemented', 'extend', 'feature', 'support']
    adaptive_keyword_set = set(adaptive_keyword_list)

    commit_msg_list = []

    data_size = len(data_list)
    for idx, row in enumerate(data_list):
        if (idx%1000)==0:
            print("idx: {0:,}/{1:,}".format(idx, data_size))

        p_name = row[0]
        linecid = row[1]
        tokencid = row[2]
        msg = row[3]

        stemmed_tokens_set = set(preprocess_text(msg))
        out_keyword_dict = {'fix': False, 'esolv': False, 'clos': False, 'handl': False, 'issue': False, 'defect': False, 'bug': False, 'problem': False, 'ticket': False, 'refactor': False, 're-factor': False, 'reimplement': False, 're-implement': False, 'design': False, 'replac': False, 'modify': False, 'updat': False, 'upgrad': False, 'cleanup': False, 'clean-up': False, 'add': False, 'new': False, 'introduc': False, 'implement': False, 'implemented': False, 'extend': False, 'feature': False, 'support': False}
        corrective_flag = keyword_check(corrective_keyword_set, stemmed_tokens_set, out_keyword_dict)
        perfective_flag = keyword_check(perfective_keyword_set, stemmed_tokens_set, out_keyword_dict)
        adaptive_flag = keyword_check(adaptive_keyword_set, stemmed_tokens_set, out_keyword_dict)
        

        record = [p_name, linecid, tokencid, corrective_flag, perfective_flag, adaptive_flag]
        for key in corrective_keyword_list+perfective_keyword_list+adaptive_keyword_list:
            record.append(out_keyword_dict[key])

        commit_msg_list.append(tuple(record))

        if (idx%100000)==0:
            util.dump_pickle('./data/back2.pickle', commit_msg_list)


    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS commit_maintenance;") 
    cur.execute("CREATE TABLE commit_maintenance(project TEXT, linecid TEXT, tokencid TEXT, corrective_flag, perfective_flag, adaptive_flag, fix, esolv, clos, handl, issue, defect, bug, problem, ticket, refactor, re_factor, reimplement, re_implement, design, replac, modify, updat, upgrad, cleanup, clean_up, 'add', new, introduc, implement, implemented, extend, feature, support, PRIMARY KEY (linecid));")
    cur.executemany("INSERT INTO commit_maintenance(project, linecid, tokencid, corrective_flag, perfective_flag, adaptive_flag, fix, esolv, clos, handl, issue, defect, bug, problem, ticket, refactor, re_factor, reimplement, re_implement, design, replac, modify, updat, upgrad, cleanup, clean_up, 'add', new, introduc, implement, implemented, extend, feature, support) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", commit_msg_list)
    conn.commit()
    conn.close()
        


def extract_data():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    command = """
              SELECT project, linecid, tokencid, msg
              FROM commit_msg
              """
    cur.execute(command)
    return_list = []
    for row in cur.fetchall():
        return_list.append(row)
    conn.close()

    return return_list


def main():

    if not os.path.exists('./data'): os.makedirs('./data')
    data_list = extract_data()
    extract_maintenance(data_list)

if __name__=="__main__":
    main()


