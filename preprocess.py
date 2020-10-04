dict_path_latin1 = "./wordlist/rockyou.txt"
dict_path_utf8 = "./wordlist/rockyou-utf8.txt"

f = open(dict_path_latin1, 'r', encoding="latin-1")
content = f.read()
f.close()
f = open(dict_path_utf8, 'w', encoding="utf-8")
f.write(content)
f.close()

plain_dict_path = "./wordlist/rockyou.txt"
plain_dict_list = open(plain_dict_path, 'r', errors='ignore').readlines()
plain_dict_list = list(map(str.strip, plain_dict_list))

