import pickle
import sqlite3
import sys
import yaml
import json

def dump_pickle(f_name, data):

    with open(f_name, "wb") as f:
        pickle.dump(data, f)


def load_pickle(f_name):

    with open(f_name, "rb") as f:
        data = pickle.load(f)

    return data

def read_yaml(f_path):
    with open(f_path, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return data

def read_json(f_path):
    with open(f_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

def dump_json(f_path, data, indent=4):
    with open(f_path, 'w') as f:
        json.dump(data, f, indent=indent)

