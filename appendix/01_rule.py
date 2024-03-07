from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
import sqlite3
import sys
import os
import pandas as pd


def check_statement1(token_df, exclude_set):
    # add/remove statement


    return_set = set()
    for org in set(token_df['org']):
        if org in exclude_set:
            continue

        tmp_df = token_df[token_df['org']==org]

        flag = 0
        if tmp_df['token'].iloc[-1]==';' and tmp_df['token_type'].iloc[-1]=='expr_stmt' and tmp_df['token_type'].iloc[0]!='else':
            flag = 1
        elif tmp_df['token'].iloc[0]=='#' and tmp_df['token_type'].iloc[0]=='include' and tmp_df['token_type'].iloc[-1]=='file':
            flag = 1
        elif tmp_df['token'].iloc[0]=='return' and tmp_df['token_type'].iloc[0]=='return' and tmp_df['token_type'].iloc[-1]=='return':
            flag = 1
        elif tmp_df['token_type'].iloc[0]=='name' and tmp_df['token'].iloc[-1]=='@' and tmp_df['token_type'].iloc[-1]=='annotation':
            flag = 1
        elif tmp_df['token'].iloc[0]=='@' and tmp_df['token_type'].iloc[0]=='annotation' and tmp_df['token'].iloc[-1]==')' and tmp_df['token_type'].iloc[-1]=='argument_list':
            flag = 1
        else:
            #print('NG cate: {0}'.format(org))
            continue

        category = 'statement'
        return_set.add(org)
    
    return return_set


def check_identifier1(token_df, exclude_set):
    # add/remove statement

    return_set = set()
    for org in set(token_df['org']):
        if org in exclude_set:
            continue

        tmp_df = token_df[token_df['org']==org]

        tmp_list1 = tmp_df['token_type'].unique()

        if len(set(tmp_list1) - set(['name', 'file']))!=0:
            #print('NG')
            continue

        category = 'identifier'
        return_set.add(org)

    return return_set


def check_constant1(token_df, exclude_set):
    # add/remove statement

    return_set = set()
    for org in set(token_df['org']):

        if org in exclude_set:
            continue

        tmp_df = token_df[token_df['org']==org]

        tmp_list1 = tmp_df['token_type'].unique()

        if len(set(tmp_list1) - set(['literal', 'asm', 'value']))==0:
            pass
        elif len(set(tmp_list1) - set(['literal', 'name']))==0:
            pass
        else:
            continue

        category = 'constant'
        return_set.add(org)

    return return_set


def check_control1(token_df, exclude_set):

    return_set = set()
    for org in set(token_df['org']):

        if org in exclude_set:
            continue

        tmp_df = token_df[token_df['org']==org]

        flag = 0
        if (tmp_df['token']=='goto').any() or ((tmp_df['token']=='ifdef').any() and (tmp_df['token_type']=='directive').any()) or (tmp_df['token']=='if').any() or (tmp_df['token_type']=='break').any() or ((tmp_df['token']=='case').any() and (tmp_df['token_type']=='case').any()) or (tmp_df['token_type']=='default').any():
            flag = 1
        #elif (tmp_df['token'].iloc[-1]==')' and tmp_df['token_type'].iloc[-1]=='block') or (tmp_df['token'].iloc[-1]=='}' and tmp_df['token_type'].iloc[-1]=='block'):
        elif (tmp_df['token'].iloc[0]=='(' and tmp_df['token_type'].iloc[0]=='block' and tmp_df['token'].iloc[-1]==')' and tmp_df['token_type'].iloc[-1]=='block') or (tmp_df['token'].iloc[0]=='{' and tmp_df['token_type'].iloc[0]=='block' and tmp_df['token'].iloc[-1]=='}' and tmp_df['token_type'].iloc[-1]=='block'):
            flag = 1
        elif (tmp_df['token']=='{ }').any():
            flag = 1
        else:
            #print('NG cate: {0}'.format(org))
            continue

        category = 'control flow'
        return_set.add(org)
    
    return return_set


def check_no1(token_df, exclude_set):

    return_set = set()
    for org in set(token_df['org']):
        if org in exclude_set:
            continue

        tmp_df = token_df[token_df['org']==org]

        flag = 0
        if tmp_df['token_type'].iloc[0]=='empty_stmt':
            flag = 1
        else:
            #print('NG cate: {0}'.format(org))
            continue

        category = 'no'
        return_set.add(org)
    
    return return_set


def check_declaration1(token_df, exclude_set):
    # add/remove statement

    return_set = set()
    for org in set(token_df['org']):

        if org in exclude_set:
            continue

        tmp_df = token_df[token_df['org']==org]

        flag = 0
        if tmp_df['token_type'].iloc[0]=='define' or tmp_df['token_type'].iloc[0]=='specifier':
            flag = 1
        # elif (tmp_df['token_type'].iloc[0]=='name' and tmp_df['token'].iloc[0]=='int') or (tmp_df['token_type'].iloc[0]=='name' and tmp_df['token'].iloc[0]=='u32') or (tmp_df['token_type'].iloc[0]=='name' and tmp_df['token'].iloc[0]=='unsigned'):
        elif ((tmp_df['token_type']=='name') & (tmp_df['token']=='int')).any() or ((tmp_df['token_type']=='name') & (tmp_df['token']=='u32')).any() or ((tmp_df['token_type']=='name') & (tmp_df['token']=='unsigned')).any() or ((tmp_df['token_type']=='name') & (tmp_df['token']=='long')).any() or ((tmp_df['token_type']=='name') & (tmp_df['token']=='__init')).any() or ((tmp_df['token_type']=='name') & (tmp_df['token']=='__initdata')).any() or ((tmp_df['token_type']=='name') & (tmp_df['token']=='__iomem')).any() or ((tmp_df['token_type']=='name') & (tmp_df['token']=='__user')).any() or ((tmp_df['token_type']=='name') & (tmp_df['token']=='uninitialized_var')).any() or ((tmp_df['token_type']=='name') & (tmp_df['token']=='__maybe_unused')).any():  
            flag = 1
        elif (tmp_df['token_type'].iloc[0]=='init' and tmp_df['token'].iloc[0]=='='):
            flag = 1
        else:
            #print('NG cate: {0}'.format(org))
            continue

        category = 'declaration'
        return_set.add(org)
    
    return return_set
        


def check_expression1(token_df, exclude_set):
    # add/remove statement

    return_set = set()
    for org in set(token_df['org']):
        if org in exclude_set:
            continue

        tmp_df = token_df[token_df['org']==org]

        flag = 0
        if ((tmp_df['token_type']=='argument_list') & (tmp_df['token']==',')).any() or ((tmp_df['token_type']=='argument_list') & (tmp_df['token']=='(')).any() or ((tmp_df['token_type']=='argument_list') & (tmp_df['token']==')')).any() or ((tmp_df['token_type']=='argument_list') & (tmp_df['token']=='()')).any() or ((tmp_df['token_type']=='block') & (tmp_df['token']==', }')).any():  
            flag = 1
        elif ((tmp_df['token_type']=='operator') & (tmp_df['token']=='+')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='-')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='*')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='/')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='&')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='&&')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='==')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='!=')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='.')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='|')).any() or (((tmp_df['token_type']=='operator') & (tmp_df['token']=='(')).any() and ((tmp_df['token_type']=='operator') & (tmp_df['token']==')')).any()) or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='=')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='!')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='++')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='--')).any() or ((tmp_df['token_type']=='operator') & (tmp_df['token']=='->')).any():  
            flag = 1
        elif ((tmp_df['token_type']=='block') & (tmp_df['token']==',')).any():  
            flag = 1
        elif len(set(tmp_df['token_type'].unique()) - set(['name', 'value'])) == 0 and len(tmp_df['token_type'].unique())==2:
            flag=1
        elif len(set(tmp_df['token_type'].unique()) - set(['value'])) == 0 and len(tmp_df['token_type'].unique())==1:
            flag=1
        elif len(set(tmp_df['token_type'].unique())-set(['argument']))==0 & (tmp_df['token_type'].iloc[0]=='NULL' or tmp_df['token_type'].iloc[-1]=='NULL'):  
            flag = 1
        else:
            pass

        if tmp_df.shape[0]>1:
            if (tmp_df['operation'].iloc[0]=='-') & (tmp_df['operation'].iloc[1]=='+') & (((tmp_df['token_type'].iloc[0]=='literal') & (tmp_df['token_type'].iloc[1]=='name')) or (tmp_df['token_type'].iloc[0]=='name') & (tmp_df['token_type'].iloc[1]=='literal')):  
                flag = 1

        if flag==0:
            #print('NG cate: {0}'.format(org))
            continue

        category = 'expression'
        return_set.add(org)
    
    return return_set



def evaluation(statement_set, declaration_set, constant_set, control_set, expression_set, identifier_set, no_set):

    print('Evaluation start')
    # Display the count of each set
    print("Count of Statement Set:", len(statement_set))
    print("Count of Declaration Set:", len(declaration_set))
    print("Count of Constant Set:", len(constant_set))
    print("Count of Control Flow Set:", len(control_set))
    print("Count of Expression Set:", len(expression_set))
    print("Count of Identifier Set:", len(identifier_set))
    print("Count of No Set:", len(no_set))

    total_count = len(statement_set) + len(declaration_set) + len(constant_set) + len(control_set) + len(expression_set) + len(identifier_set) + len(no_set)
    print("Total Count:", total_count)
    print("Total Count in set:", len(statement_set | declaration_set | constant_set | control_set | expression_set | identifier_set | no_set))

    all_sets = []
    for set_name, set_data in [('statement', statement_set), ('declaration', declaration_set),
                            ('constant', constant_set), ('control flow', control_set),
                            ('expression', expression_set), ('identifier', identifier_set),
                            ('no', no_set)]:
        for item in set_data:
            all_sets.append([set_name, item])

    df_all_sets = pd.DataFrame(all_sets, columns=['category', 'org'])
    df_all_sets.to_csv('./data/02_check.csv', index=False)

    conn = sqlite3.connect('./db/manual_labels.db')
    labels_df = pd.read_sql_query('SELECT category, org FROM manual_labels', conn)
    conn.close()

    cnt = 0
    failed_hash_list = []
    for org in labels_df['org']:
        tmp = df_all_sets[df_all_sets['org']==org]
        if tmp.shape[0]==0:
            if labels_df[labels_df['org']==org]['category'].iloc[0][:4]=="mult":
                cnt += 1
            else:
                failed_hash_list.append((org,"multi"))
        else:
            if tmp['category'].iloc[0]==labels_df[labels_df['org']==org]['category'].iloc[0]:
                cnt += 1
            else:
                failed_hash_list.append((org, tmp['category'].iloc[0]))
    
    print("\nfailed hash list")
    print(failed_hash_list)
    print("")
        
    total_samples = labels_df.shape[0]
    proportion = cnt / total_samples
    print(f"Proportion of cnt: {proportion:.2f} (fraction)")
    print(f"Proportion of cnt: {proportion * 100:.2f}% (percentage)")
    print("{0}/{1}".format(cnt, total_samples))


    # output csv file
    TABLE = []
    row = []
    cnt = 0
    tmp_set = set()
    #for category in df_all_sets['category'].unique():
    for category in ['declaration', 'constant', 'identifier', 'control flow', 'statement', 'expression', 'no']:
        target = set(labels_df[labels_df['category']==category]['org'])
        predict = set(df_all_sets[df_all_sets['category']==category]['org'])
        print("{0}: {1}/{2}".format(category, len(target & predict), len(target)))
        tmp_set = tmp_set | target
        cnt += len(target & predict)

        proportion = len(target & predict) / len(target)
        tmp = f"{proportion * 100:.1f}" + " ({0}/{1})".format(len(target & predict), len(target))
        row.append(tmp)
    
    predict = set(labels_df['org']) - set(df_all_sets['org'])
    target = set(labels_df['org']) - tmp_set
    print("multi: {0}/{1}".format(len(target & predict), len(target)))
    cnt += len(target & predict)

    proportion = len(target & predict) / len(target)
    tmp = f"{proportion * 100:.1f}" + " ({0}/{1})".format(len(target & predict), len(target))
    row.append(tmp)

    proportion = cnt / total_samples
    tmp = f"{proportion * 100:.1f}" + " ({0}/{1})".format(cnt, total_samples)
    row.append(tmp)
    TABLE.append(row)

    df = pd.DataFrame(TABLE, columns=['declaration', 'constant', 'identifier', 'control flow', 'statement', 'expression', 'no', 'multi', 'total'])
    df.to_csv('./data/acc.csv', index=False)
    

if __name__=="__main__":
    conn = sqlite3.connect('./db/manual_labels.db')
    query = "SELECT * FROM tokens"
    token_df = pd.read_sql_query(query, conn)
    conn.close()

    print('identifier start')
    identifier_set = check_identifier1(token_df, set())
    print('identifier done')
    print('constant start')
    constant_set = check_constant1(token_df, identifier_set)
    print('constant done')
    print('statement start')
    statement_set = check_statement1(token_df, identifier_set | constant_set)
    print('statement done')
    print('declaration start')
    declaration_set = check_declaration1(token_df, identifier_set | constant_set | statement_set)
    print('declaration done')
    print('control flow start')
    control_set = check_control1(token_df, identifier_set | constant_set | statement_set | declaration_set)
    print('control flow done')
    print('expression start')
    expression_set = check_expression1(token_df, identifier_set | constant_set | statement_set | declaration_set | control_set)
    print('expression done')
    print('no start')
    no_set = check_no1(token_df, identifier_set | constant_set | statement_set | declaration_set | control_set | expression_set)
    print('no done')


    evaluation(statement_set, declaration_set, constant_set, control_set, expression_set, identifier_set, no_set)
