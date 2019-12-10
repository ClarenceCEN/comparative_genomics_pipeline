import pandas as pd
import sys


def CAZY_counts(file_prefix):

    data = pd.read_table(file_prefix+".tab", sep="\t", header=None)

    a = data[0]
    c_with_num = a.replace('.hmm','',regex=True)
    d_without_num = a.replace('[0-9]*_*[0-9]*.hmm','',regex=True)
    b1 = c_with_num.value_counts()
    b1_No = b1.shape[0]
    b2 = d_without_num.value_counts()
    b2_No = b2.shape[0]
    g1 = pd.Series([file_prefix]*b1_No)
    g2 = pd.Series([file_prefix]*b2_No)
    g1.index = b1.index
    g2.index = b2.index
    e1 = [g1, b1]
    e2 = [g2, b2]
    f1 = pd.concat(e1, axis=1)
    f2 = pd.concat(e2, axis=1)
    #print(f1[0])
    #print(f1.index.str.contains('GH',regex=False))
    f1['category'] = 'GH'
    GT_cate = f1.index.str.contains('GT',regex=False)
    AA_cate = f1.index.str.contains('AA',regex=False)
    CBM_cate = f1.index.str.contains('CBM',regex=False)
    CE_cate = f1.index.str.contains('CE',regex=False)
    #f1[f1.index.str.contains('GH',regex=False)]['category'] = 'GT'
    f1.loc[GT_cate,'category'] = 'GT'
    f1.loc[AA_cate,'category'] = 'AA'
    f1.loc[CBM_cate,'category'] = 'CBM'
    f1.loc[CE_cate,'category'] = 'CE'
    print(f1)
    #print(b2)
    print(file_prefix+" done!")
    f1.to_csv(file_prefix+"_family.csv", sep=',',header = None)
    f2.to_csv(file_prefix+"_category.csv", sep=',',header = None)

CAZY_counts(sys.argv[1])