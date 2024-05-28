#/usr/bin/python3

import os
import argparse

def load_hidx(hidx_file):
    len_hash_dict = dict()
    hash_file_dict = dict()

    with open(hidx_file, "r") as f:
        lines = f.readlines()

    init = True
    delim = False
    for line in lines:
        ls = line.strip()
        if init:
            init = False
            continue # skip first line (metadata)

        if len(ls) == 0:
            continue

        if "=====" in ls:
            delim = True
            continue

        tokens = ls.split("\t")

        if not delim: # before delimiter: len to hash list
            func_len = int(tokens[0])
            hash_list = set(tokens[1:])
            len_hash_dict[func_len] = hash_list

        else: # after delimiter: hash to file and line
            hash_val = tokens[0]
            file_name = tokens[1]
            line_num = tokens[2]
            hash_file_dict[hash_val] = [file_name, line_num]

    return hidx_file, len_hash_dict, hash_file_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target",
        type=str,
        required=True,
        help="Target program to find vulnerable clones"
    )

    parser.add_argument(
        "-d",
        "--database",
        type=str,
        required=True,
        help="Path to the directory storing vulnerablility hidx"
    )

    args = parser.parse_args()

    if not os.path.exists(args.target):
        print(f"[-] {args.target} does not exist")
        exit(1)

    if not args.target.endswith(".hidx"):
        print(f"[-] {args.target} does not appear to be a hidx file")
        exit(1)

    if not os.path.exists(args.database):
        print(f"[-] {args.database} does not exist")
        exit(1)

    target, target_len_hash_dict, target_hash_file_dict = load_hidx(args.target)

    vdb_list = list()
    vdb_len_hash_dict_list = list()
    vdb_hash_file_dict_list = list()

    for hidx_file in os.listdir(args.database):
        file_ = os.path.join(args.database, hidx_file)

        vdb, vdb_len_hash_dict, vdb_hash_file_dict = load_hidx(file_)
        vdb_list.append(vdb)
        vdb_len_hash_dict_list.append(vdb_len_hash_dict)
        vdb_hash_file_dict_list.append(vdb_hash_file_dict)

    collision_set = set()

    for vdb_idx, vdb in enumerate(vdb_list):
        print(f"Target {target} vs VDB {vdb}")
        for func_len in target_len_hash_dict:
            if func_len not in vdb_len_hash_dict_list[vdb_idx]:
                continue

            target_hash_list = target_len_hash_dict[func_len]
            vdb_hash_list = vdb_len_hash_dict_list[vdb_idx][func_len]

            collision = target_hash_list.intersection(vdb_hash_list)

            if len(collision) == 0:
                continue

            collision_set.update(collision)

        for hash_ in collision_set:
            print(hash_)
            file_info = target_hash_file_dict[hash_]
            vuln_info = vdb_hash_file_dict_list[vdb_idx][hash_]
            print(f"[+] {file_info[1]}-th function in {file_info[0]}"
                  f"is a clone of vulnerability at {vuln_info[0]}")

