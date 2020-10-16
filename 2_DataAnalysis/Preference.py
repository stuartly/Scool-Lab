import csv
import sys
import pandas as pd
from os.path import basename
import math
from datetime import datetime
input_file = sys.argv[1]
output_file = sys.argv[2]

def fa(file):
    tmp_lst = []
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
    author_num=df['AU']
    i=0
    co_paper=0
    co_paper_over3=0
    while i<len(author_num):
        author_str=author_num[i]
        author_lis=author_str.split('; ')
        author_lis_length=len(author_lis)
        if author_lis_length>1:
            co_paper=co_paper+1
        if author_lis_length>2:
            co_paper_over3=co_paper_over3+1
        i=i+1
    familiarity=math.sqrt(co_paper_over3/co_paper)
    return familiarity

def ad(file):
    tmp_lst = []
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
    year=df['PY']
    this_year=datetime.now().year
    last_year=this_year-1
    the_year_before_last=last_year-1
    the_year_before_last2year=the_year_before_last-1
    the_year_before_last3year = the_year_before_last2year - 1
    last_3_year_lis=[str(this_year),str(last_year),str(the_year_before_last),str(the_year_before_last2year),str(the_year_before_last3year)]
    year_to_papernum_lis=[]
    for j in last_3_year_lis:
        yearly_paper=0
        i=0
        while i<len(year):
            if year[i]==j:
                yearly_paper=yearly_paper+1
            i=i+1
        year_to_papernum_lis.append(yearly_paper)
    i=0
    yearly_speed_accumulated=0
    while i<len(year_to_papernum_lis)-1:
        yearly_speed=(year_to_papernum_lis[i+1]-year_to_papernum_lis[i])/year_to_papernum_lis[i]
        yearly_speed_accumulated=yearly_speed_accumulated+yearly_speed
        i=i+1
    advancing=yearly_speed_accumulated/len(year_to_papernum_lis)
    return advancing

def si(file):
    # 先读取每篇论文的摘要
    tmp_lst = []
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
    a = df['AB']
    b = a[0]
    total = 0

    i = 1
    while i < (len(a) - 1):
        b = str(b + a[i])
        c = str(a[i + 1])
        # 整合文档数据
        doc_complete1 = [b]
        doc_complete2 = [c]

        # 数据清洗和预处理
        from nltk.corpus import stopwords
        from nltk.stem.wordnet import WordNetLemmatizer
        import string
        import nltk

        nltk.download('wordnet')
        stop = set(stopwords.words('english'))
        exclude = set(string.punctuation)
        lemma = WordNetLemmatizer()

        def clean(doc):
            stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
            punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
            normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
            return normalized

        doc_clean1 = [clean(doc).split() for doc in doc_complete1]
        doc_clean2 = [clean(doc).split() for doc in doc_complete2]

        # 准备Document-Term矩阵
        import gensim
        from gensim import corpora

        import gensim
        from gensim import corpora

        # 创建语料的词语词典，每个单独的词语都会被赋予一个索引
        dictionary1 = corpora.Dictionary(doc_clean1)
        dictionary2 = corpora.Dictionary(doc_clean2)

        # 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
        doc_term_matrix1 = [dictionary1.doc2bow(doc) for doc in doc_clean1]
        doc_term_matrix2 = [dictionary2.doc2bow(doc) for doc in doc_clean2]

        # 构建LDA模型
        # 使用 gensim 来创建 LDA 模型对象
        Lda = gensim.models.ldamodel.LdaModel

        # 在 DT 矩阵上运行和训练 LDA 模型
        ldamodel1 = Lda(doc_term_matrix1, num_topics=3, id2word=dictionary1, passes=50)
        ldamodel2 = Lda(doc_term_matrix2, num_topics=3, id2word=dictionary2, passes=50)

        # 输出结果
        m = str(ldamodel1.print_topics(num_topics=3, num_words=3))
        n = str(ldamodel2.print_topics(num_topics=3, num_words=3))

        import re
        pattern1 = re.compile(r'\'(.*?)\'')
        pattern2 = re.compile(r'\'(.*?)\'')
        result1 = str(pattern1.findall(m))
        result2 = str(pattern2.findall(n))

        pattern = re.compile(r'"(\w+)"')
        mo_result1 = pattern.findall(result1)
        h = ' '.join(mo_result1)
        mo_result2 = pattern.findall(result2)
        k = ' '.join(mo_result2)

        import math
        import time

        # 对要进行比较的str1和str2进行计算，并返回相似度
        def simicos(str1, str2):
            # 分词
            cut_str1 = str1.split(' ')
            cut_str2 = str2.split(' ')
            # 列出所有词
            all_words = set(cut_str1 + cut_str2)
            # 计算词频
            freq_str1 = [cut_str1.count(x) for x in all_words]
            freq_str2 = [cut_str2.count(x) for x in all_words]
            # 计算相似度
            sum_all = sum(map(lambda z, y: z * y, freq_str1, freq_str2))
            sqrt_str1 = math.sqrt(sum(x ** 2 for x in freq_str1))
            sqrt_str2 = math.sqrt(sum(x ** 2 for x in freq_str2))
            return sum_all / (sqrt_str1 * sqrt_str2)

        case1 = result1
        case2 = result2
        start = time.time()
        similarity = simicos(h, k)
        total = total + similarity
        print(*"相似度: %.3f" % similarity)
        i = i + 1

    aver_sim = total / (len(a) - 1)
    return aver_sim

def th(file):
    tmp_lst = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
    year = df['PY']
    year_lis_str = []
    for i in year:
        year_lis_str.append(i)
    year_lis_str = list(set(year_lis_str))
    year_lis_int = list(map(int, year_lis_str))
    year_lis_int_sorted = sorted(year_lis_int, reverse=False)
    year_lis_str_sorted = []
    for i in year_lis_int_sorted:
        year_lis_str_sorted.append(str(i))
    coauthor_num_lis = []
    for i in year_lis_str_sorted:
        groupby_df = df.groupby(['PY'])['AU'].get_group(i)
        author_yearly = []
        for row in groupby_df:
            author_yearly.append(row)
        author_yearly_unsorted = []
        for k in author_yearly:
            author_list_yearly = k.split('; ')
            author_yearly_unsorted = author_yearly_unsorted + author_list_yearly
        author_yearly_sorted = list(set(author_yearly_unsorted))
        coauthor_num_lis.append(len(author_yearly_sorted) - 1)
    num = 0
    coauthor_v_accu = 0
    while num < len(coauthor_num_lis) - 1:
        coauthor_v = (coauthor_num_lis[num + 1] - coauthor_num_lis[num]) / coauthor_num_lis[num]
        coauthor_v_accu = coauthor_v_accu + coauthor_v
        num = num + 1
    thriving = coauthor_v_accu / len(coauthor_num_lis) - 1
    return thriving

def main():
    author = basename(input_file).strip('.csv')
    familiarity=fa(input_file)
    advancing=ad(input_file)
    similarity=si(input_file)
    thriving=th(input_file)
    with open(output_file,'a',newline='')as csv_out_file:
        filewriter=csv.writer(csv_out_file)
        filewriter.writerow([author,familiarity,advancing,similarity,thriving])

if __name__=="__main__":
    main()
