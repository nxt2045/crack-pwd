#!/usr/bin/env python
# Cracking Hashed Password
# By Xiaotong Niu
# 2020-10-04

import os


def hashing(plain_list, hash_type, encoding):
    """
    :param plain_list:
    :param hash_type: type to hashing plain_list
    :param encoding: plain_list's encoding
    :return: hashed_list
    """
    # hashing the list
    import hashlib
    plain_list = list(map(str.strip, plain_list))
    hashed_list = []
    for plain_word in plain_list:
        crypt = hashlib.new(hash_type)
        crypt.update(bytes(plain_word, encoding=encoding))
        hashed_word = crypt.hexdigest()
        hashed_list.append(hashed_word)
    return hashed_list


def get_hash_type(word):
    """
    get hash type based on word length
    """
    hash_type = ""
    if word.isdigit() or word.isalpha() or not word.isalnum():
        print("Hash type not support.")
        exit()
    elif len(word) == 32:
        hash_type = "md5"
    elif len(word) == 40:
        hash_type = "sha1"
    elif len(word) == 56:
        hash_type = "sha224"
    elif len(word) == 64:
        hash_type = "sha256"
    elif len(word) == 96:
        hash_type = "sha384"
    elif len(word) == 128:
        hash_type = "sha512"
    else:
        print("Hash type not support.")
        exit()
    return hash_type


def get_same_sublist(a_list, b_list):
    a_set = set(a_list)
    b_set = set(b_list)
    return list(a_set.intersection(b_set))


def crack_by_dict(hashed_pwd_path):
    """
    :param hashed_pwd_path: password file path to crack
    """
    # read plain password list
    if not os.path.isfile(hashed_pwd_path):
        print("password file %s not exit")
        exit()
    hashed_pwd_list = open(hashed_pwd_path, 'r').readlines()
    hashed_pwd_list = list(map(str.strip, hashed_pwd_list))
    print("finish reading password file")

    # get hash type
    hash_type = get_hash_type(hashed_pwd_list[0])
    print("found hash type: ", hash_type)

    # read plain dictionary list
    plain_dict_path = "./wordlist/rockyou.txt"
    plain_dict_list = open(plain_dict_path, 'r', encoding="ISO-8859-1").readlines()
    plain_dict_list = list(map(str.strip, plain_dict_list))
    print("finish reading dictionary")

    # get hashed dictionary list
    hashed_dict_path = "./wordlist/rockyou-" + hash_type + ".txt"
    if os.path.isfile(hashed_dict_path):
        hashed_dict_list = open(hashed_dict_path, 'r').readlines()
        hashed_dict_list = list(map(str.strip, hashed_dict_list))
    else:
        print("new hash type, hashing dictionary...")
        hashed_dict_list = hashing(plain_dict_list, hash_type, encoding="ISO-8859-1")
        # save hashed dictionary
        print("saving new hashed dictionary...")
        with open(hashed_dict_path, 'w') as f:
            for word in hashed_dict_list:
                f.write("%s\n" % word)
    print("finish hashing dictionary")

    # crack password
    hashed_same_list = get_same_sublist(hashed_pwd_list, hashed_dict_list)
    print("finish crack password: %d / %d" % (len(hashed_same_list), len(hashed_pwd_list)))

    # save crack result
    print("saving results ...")
    cracked_file_path = os.path.dirname(hashed_pwd_path) + "/cracked.txt"
    with open(cracked_file_path, 'w', encoding="ISO-8859-1") as f:
        for i in range(len(hashed_same_list)):
            line = hashed_same_list[i] + " " + plain_dict_list[hashed_dict_list.index(hashed_same_list[i])]
            f.write(line + "\n")
            print(line)
    print("finish saving: " + cracked_file_path)


def crack_yahoo(input_path):
    write_list = []
    output_path = os.path.dirname(input_path) + "/cracked.txt"
    with open(input_path, 'r', encoding="ISO-8859-1") as f_read:
        for position, line in enumerate(f_read):
            if position < 3073 - 1:
                continue
            elif 3073 - 1 <= position < 456564:
                new_line = line.strip('\n') + " " + line.strip('\n').split(':')[-1]
                write_list.append(new_line)
            else:
                break
    print("finish crack password")
    print("saving results ...")
    with open(output_path, 'w', encoding="ISO-8859-1") as f_write:
        i = 0
        for line in write_list:
            f_write.write(line + '\n')
    print("finish saving: " + output_path)


if __name__ == '__main__':
    file_path = ""
    choice = input("please choose linkedin/formspring/yahoo/other to crack: ")
    if choice == "yahoo":
        file_path = "Password List/yahoo/password.file"
        crack_yahoo(file_path)
    elif choice == "linkedin":
        file_path = "Password List/linkedin/SHA1.txt"
        crack_by_dict(file_path)
    elif choice == "formspring":
        file_path = "Password List/formspring/formspring.txt"
        crack_by_dict(file_path)
    elif choice == "other":
        file_path = input("please input file path to crack: ")
        crack_by_dict(file_path)
    else:
        print("sorry, can not understand your input")
