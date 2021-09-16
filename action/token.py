import jieba
from hotjb.response import respond

def tokenizer(env):
    '''
    '''

    r = jieba.cut('测试文本用于测试。',use_paddle=True)

    return respond([r])