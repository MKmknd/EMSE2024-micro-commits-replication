
import subprocess
import sys
import re
from datetime import datetime as dt

def ignore_somecode(text):
    """
    Ignore new pages and CR.
    In git, these are represented as '\r' and '\f'
    If we add '\0' to database, we get error.
    """
    text = re.sub('\r', '', text)
    text = re.sub('\f', '', text)
    text = re.sub('\0', '', text)
    return text


def get_all_hash(repodir):
    hash_list = subprocess.check_output(
            ['git', '-C', '{}'.format(repodir), 'log', '--all', '--pretty=format:%H'],
            universal_newlines=True
            ).splitlines()
    return hash_list


def get_commit_message(repodir, commit_hash):
    commit_msg_list = subprocess.check_output(
            ['git', '-C', '{}'.format(repodir), 'log', '--format=%B',
            '-n', '1', commit_hash],
            universal_newlines=True,
            errors="replace"
            ).splitlines()

    return "\n".join(commit_msg_list)


def git_show_with_context(dirname, commit_hash, context):
    show = subprocess.check_output(
            ['git', '-C', '{}'.format(dirname), 'show',
             '--unified={0}'.format(context), commit_hash],
            ).decode('utf-8', errors='ignore')
    show = ignore_somecode(show)
    return show