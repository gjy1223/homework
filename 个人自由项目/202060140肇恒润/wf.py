import os
from os import listdir
import argparse


def get_arg():  # 读取命令行参数，如果没附加参数的话取默认值
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", '--count_letter', action="store_true")  # 第0步，字母频率
    group.add_argument("-f", '--find_word', action="store_true")  # 第一步，第二步，单词频率
    # group.add_argument("-p", '--phrase', type=int)  # 第三步，短语（未完成）

    parser.add_argument("-d", '--find_word_in_dir', action="store_true")  # 在目录里找文件
    parser.add_argument("-s", '--sub_dir', action="store_true")  # 在目录及子目录里找文件
    parser.add_argument("-n", '--disp_num', default=5, type=int)  # 显示的个数，默认5个，值为-1时全部显示
    parser.add_argument("-x", '--stop_words', type=str)  # 停词
    parser.add_argument('path')  # 路径（文件名）
    opt = parser.parse_args()
    return opt


def read_text(file_name):  # 读取指定的文本文件
    text = open(file_name, 'r', encoding='utf-8')  # 打开txt
    strs = text.read()  # 文本读入字符串，全变成小写
    text.close()  # 关text
    strs = strs.lower()  # 全变成小写
    return strs  # 作为一个字符串返回


def is_number(s):  # 判断是不是数字
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def is_txt_file(filename):  # 判断是不是文本文件
    return any(filename.endswith(extension) for extension in [".txt"])


def letter_frequence(file_name, disp_num):  # 第0步，输出文本文件中26个字母出现频率并由高到低排列并显示百分比
    strs = read_text(file_name)  # 读文件
    letters = ['a', 'b', 'c', 'd', 'e',  # 字母表
               'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
    letter_frequency = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0,  # 统计字母个数的字典
                        'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0,
                        'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0,
                        'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0,
                        'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
    total_letters_num = 0  # 字符串中总的字母个数

    for letter in strs:  # 在字符串中for循环读字母
        if letter not in letters and letter != ' ':  # 如果不是字母，也不是空格的字符，就全变成空格
            strs = strs.replace(letter, ' ')
        if letter in letters:  # 如果是字母，总字母数+1，对应的字母词典中的数+1
            total_letters_num += 1
            letter_frequency[letter] += 1
    for item in letter_frequency:  # 算百分比
        letter_frequency[item] = letter_frequency[item] / total_letters_num
        letter_frequency[item] = round(letter_frequency[item] * 100, 2)
    result = sorted(letter_frequency.items(), key=lambda k: k[1], reverse=True)  # sorted排序
    # sorted排序函数用法：
    # 按照value值降序排列：
    # sorted(dict.items(), key=lambda k: k[1], reverse=True)
    # 按照value值升序排序：
    # sorted(dict.items(), key=lambda k: k[1], reverse=False)
    # 或者sorted(dict.items(), key=lambda k: k[1])
    # 按照key值降序排列：
    # sorted(dict.items(), key=lambda k: k[0], reverse=True)
    # 按照key值升序排列：
    # sorted(dict.items(), key=lambda k: k[0])
    # 或者sorted(dict.items(), key=lambda k: k[0], reverse=False)

    if disp_num == -1:  # 显示的个数，值为-1就全显示
        for item in result:
            print('{}:{}%'.format(item[0], item[1]))
    else:
        if disp_num > len(result):  # 如果disp_num比单词个数还多，则全显示了好了
            disp_num = len(result)
        for i in range(disp_num):  # 显示前N个
            print('{}:{}%'.format(result[i][0], result[i][1]))


def word_frequence(file_name, disp_num, stop_words):  # 第一步，输出单个文件中前N个最常出现的单词
    strs = read_text(file_name)  # 读文件
    letters = ['a', 'b', 'c', 'd', 'e',  # 字母表
               'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
    word_frequency = {}

    for letter in strs:  # 如果不是字母，也不是空格的字符，也不是数字，就全变成空格
        if letter not in letters and letter != ' ' and not is_number(letter):
            strs = strs.replace(letter, ' ')
    words = strs.split()  # 用空格分词

    for word in words:
        if is_number(word[0]):  # 剔除掉123good这种东西
            words.remove(word)
        elif word in stop_words:  # 剔除掉停词表里的词
            words.remove(word)
        else:
            count = word_frequency.get(word, 0)
            word_frequency[word] = count + 1

    result = sorted(word_frequency.items(), key=lambda k: k[1], reverse=True)  # sorted排序

    if disp_num == -1:  # 显示的个数，值为-1就全显示
        for item in result:
            print('{}:{}'.format(item[0], item[1]))
    else:
        if disp_num > len(result):  # 如果disp_num比单词个数还多，则全显示了好了
            disp_num = len(result)
        for i in range(disp_num):
            print('{}:{}'.format(result[i][0], result[i][1]))


def read_stop_words(stop_words_path):  # 读停词表里的词，生成一个列表
    strs = read_text(stop_words_path)
    stop_words = strs.split()  # 用空格分词
    return stop_words


# def phrase_frequence(file_name, phrase_num):  # 第三步: 常用的短语,未完成
#     strs = read_text(file_name)  # 读文件
#     letters = ['a', 'b', 'c', 'd', 'e',  # 字母表
#                'f', 'g', 'h', 'i', 'j',
#                'k', 'l', 'm', 'n', 'o',
#                'p', 'q', 'r', 's', 't',
#                'u', 'v', 'w', 'x', 'y', 'z']
#     phrase_frequency = {}
#
#     for letter in strs:  # 如果不是字母，也不是空格的字符，也不是数字，就全变成|
#         if letter not in letters and letter != ' ' and not is_number(letter):
#             strs = strs.replace(letter, '|')
#     phrases = strs.split('|')  # 用|分词
#
#     for phrase in phrases:
#         if ' ' not in phrase or len(phrase) < 3:  # 剔除掉123good这种东西
#             phrases.remove(phrase)
#         else:
#             count = phrase_frequency.get(phrase, 0)
#             phrase_frequency[phrase] = count + 1
#
#     result = sorted(phrase_frequency.items(), key=lambda k: k[1], reverse=True)  # sorted排序
#
#     if phrase_num == -1:  # 显示的个数，值为-1就全显示
#         for item in result:
#             print('{}:{}'.format(item[0], item[1]))
#     else:
#         if phrase_num > len(result):  # 如果disp_num比单词个数还多，则全显示了好了
#             phrase_num = len(result)
#         for i in range(phrase_num):
#             print('{}:{}'.format(result[i][0], result[i][1]))


def main():
    opt = get_arg()
    path = opt.path
    disp_num = opt.disp_num

    if opt.stop_words:  # 有停词表就读停词表
        stop_words = read_stop_words(opt.stop_words)
    else:
        stop_words = ''

    if opt.count_letter:  # 第0步：输出某个英文文本文件中 26 字母出现的频率
        letter_frequence(path, disp_num)
    if opt.find_word:  # 第一步：输出单个文件中的前 N 个最常出现的英语单词
        word_frequence(path, disp_num, stop_words)
    if opt.find_word_in_dir and not opt.sub_dir:  # 功能2：指定文件目录，对目录下每一个文件执行操作。
        text_list = listdir(path)
        for item in text_list:
            if is_txt_file(item):
                print('|||||||||||||||||{}|||||||||||||||||'.format(item))
                word_frequence('{}{}'.format(path, item), disp_num, stop_words)
    if opt.sub_dir:  # 递归遍历目录下的所有子目录
        os.chdir(path)
        for dirpath, dirs, files in os.walk('.'):  # 递归遍历当前目录和所有子目录的文件和目录
            for name in files:  # files保存的是所有的文件名
                if is_txt_file(name):
                    print('|||||||||||||||||{}|||||||||||||||||'.format(name))
                    filename = os.path.join(dirpath, name)  # 加上路径，dirpath是遍历时文件对应的路径
                    word_frequence(filename, disp_num, stop_words)
    # if opt.phrase:  # 第三步: 我们想看看常用的短语是什么， 怎么办呢？
    #     phrase_num = opt.phrase
    #     phrase_frequence(path, phrase_num)


if __name__ == "__main__":
    main()
