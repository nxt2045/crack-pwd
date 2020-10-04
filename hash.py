import hashlib
import os


def hashing2(plain_list, hash_type):
    # hashing the list
    crypt = None
    if hash_type == "md5":
        crypt = hashlib.md5()
    elif hash_type == "sha1":
        crypt = hashlib.sha1()
    elif hash_type == "sha224":
        crypt = hashlib.sha224()
    elif hash_type == "sha256":
        crypt = hashlib.sha256()
    elif hash_type == "sha384":
        crypt = hashlib.sha384()
    elif hash_type == "sha512":
        crypt = hashlib.sha512()
    else:
        print("Cannot hashing dictionary in this hash type")
        exit()
    hashed_list = []
    for word in plain_list:
        crypt.update(bytes(word, encoding='utf-8'))
        hashed_list.append(crypt.hexdigest())
    return hashed_list


def hashing(plain_list, hash_type):
    plain_list = list(map(str.strip, plain_list))
    hashed_list = []

    # loop through the words in the input list
    for plain_word in plain_list:
        if hash_type == "sha1":
            crypt = hashlib.sha1()
        elif hash_type == "sha256":
            crypt = hashlib.sha256()
        crypt.update(bytes(plain_word, encoding='utf-8'))
        hashed_word = crypt.hexdigest()
        hashed_list.append(hashed_word)
    return hashed_list


def get_hash_type(word):
    hash_type = ""
    if len(word) == 32 and not word.isdigit() and not word.isalpha() and word.isalnum():
        hash_type = "md5"
    elif len(word) == 40 and not word.isdigit() and not word.isalpha() and word.isalnum():
        hash_type = "sha1"
    elif len(word) == 56 and not word.isdigit() and not word.isalpha() and word.isalnum():
        hash_type = "sha224"
    elif len(word) == 64 and not word.isdigit() and not word.isalpha() and word.isalnum():
        hash_type = "sha256"
    elif len(word) == 96 and not word.isdigit() and not word.isalpha() and word.isalnum():
        hash_type = "sha384"
    elif len(word) == 128 and not word.isdigit() and not word.isalpha() and word.isalnum():
        hash_type = "sha512"
    else:
        print("Hash type not support.")
        exit()
    return hash_type


def get_same_sublist(a_list, b_list):
    a_set = set(a_list)
    b_set = set(b_list)
    return list(a_set.intersection(b_set))


if __name__ == '__main__':

    # get plain password list
    # hashed_pwd_path = "Password List/formspring/formspring.txt"
    hashed_pwd_path = "Password List/linkedin/SHA1.txt"
    hashed_pwd_list = []
    if os.path.isfile(hashed_pwd_path):
        # hashed_pwd_list = open(hashed_pwd_path, 'r', encoding='utf-8', errors='ignore').readlines()
        hashed_pwd_list = open(hashed_pwd_path, 'r').readlines()

        hashed_pwd_list = list(map(str.strip, hashed_pwd_list))
        print("finish reading password file")
    else:
        print("password file %s not exit")
        exit()

    # get hash type
    hash_type = get_hash_type(hashed_pwd_list[0])
    print("found hash type", hash_type)

    # read plain dictionary list
    plain_dict_path = "./wordlist/rockyou.txt"
    # plain_dict_list = open(plain_dict_path, 'r', encoding='utf-8', errors='ignore').readlines()
    plain_dict_list = open(plain_dict_path, 'r').readlines()
    plain_dict_list = list(map(str.strip, plain_dict_list))
    print("finish reading dictionary")

    # get hashed dictionary list
    hashed_dict_path = "./wordlist/rockyou-" + hash_type + ".txt"
    hashed_dict_list = []
    if os.path.isfile(hashed_dict_path):
        hashed_dict_list = open(hashed_dict_path, 'r').readlines()
        hashed_dict_list = list(map(str.strip, hashed_dict_list))
    else:
        print("new hashing type, hashing dictionary...")
        hashed_dict_list = hashing(plain_dict_list, hash_type)
        # Creating the output file
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
    with open(cracked_file_path, 'w') as f:
        for i in range(len(hashed_same_list)):
            f.write(
                "%s %s\n" % (hashed_same_list[i], plain_dict_list[hashed_dict_list.index(hashed_same_list[i])]))
    print("finish saving: " + cracked_file_path)
