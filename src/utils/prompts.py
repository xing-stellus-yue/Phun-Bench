
# eval 1
def get_char2py_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的汉字，写出它所对应的标准普通话拼音，以json格式输出答案。示例如下：
<content>张</content>
输出：{
    "answer": "zhāng"
}
<content>我</content>
输出：{
    "answer": "wǒ"
}
<content>聂</content>
输出：{
    "answer": "niè"
}

本题目给出的汉字如下：
"""
    return system_prompt


def get_char2py_user_prompt(content):
    template = "<content>{content}</content>"
    user_prompt = template.format(content=content)
    return user_prompt


def get_char2bp_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的汉字，写出它所对应的标准普通话拼音（声调单独用数字表示，1、2、3、4、5分别表示第一声、第二声、第三声、第四声、轻声），以json格式输出答案。示例如下：
<content>张</content>
输出：{
    "base": "zhang",
    "tone": 1
}
<content>我</content>
输出：{
    "base": "wo",
    "tone": 3
}
<content>聂</content>
输出：{
    "base": "nie",
    "tone": 4
}

本题目给出的汉字如下：
"""
    return system_prompt


def get_char2bp_user_prompt(content):
    template = "<content>{content}</content>"
    user_prompt = template.format(content=content)
    return user_prompt


def get_char2chars_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的汉字，写出5个发音和它完全相同的汉字，以json格式输出答案。示例如下：
<content>臣</content>
输出：{
    "answer": ["晨", "辰", "沉", "尘", "陈"]
}
<content>京</content>
输出：{
    "answer": ["茎", "鲸", "荆", "晶", "兢"]
}
<content>义</content>
输出：{
    "answer": ["艺", "抑", "译", "忆", "易"]
}

本题目给出的汉字如下：
"""
    return system_prompt


def get_char2chars_user_prompt(content):
    template = "<content>{content}</content>"
    user_prompt = template.format(content=content)
    return user_prompt


def get_py2chars_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的拼音，写出5个发音和该拼音完全相同的汉字，以json格式输出答案。示例如下：
<pinyin>chén</pinyin>
输出：{
    "answer": ["晨", "辰", "沉", "尘", "陈"]
}
<pinyin>jīng</pinyin>
输出：{
    "answer": ["茎", "鲸", "荆", "晶", "兢"]
}
<pinyin>yì</pinyin>
输出：{
    "answer": ["艺", "抑", "译", "忆", "易"]
}

本题目给出的拼音如下：
"""
    return system_prompt


def get_py2chars_user_prompt(content):
    template = "<pinyin>{content}</pinyin>"
    user_prompt = template.format(content=content)
    return user_prompt


def get_idiom2py_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的成语，写出它所对应的标准普通话拼音（各汉字对应的拼音之间以空格隔开），以json格式输出答案。示例如下：
<content>无与伦比</content>
输出：{
    "answer": "wú yǔ lún bǐ"
}
<content>屡试不爽</content>
输出：{
    "answer": "lǚ shì bù shuǎng"
}
<content>多多益善</content>
输出：{
    "answer": "duō duō yì shàn"
}

本题目给出的成语如下：
"""
    return system_prompt

def get_idiom2py_user_prompt(content):
    template = "<content>{content}</content>"
    user_prompt = template.format(content=content)
    return user_prompt

def get_homo2py_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的一个“短语”，写出它所对应的标准普通话拼音(各汉字对应的拼音之间以空格隔开），以json格式输出答案。示例如下：
<content>吴雨仑笔</content>
输出：{
    "answer": "wú yǔ lún bǐ"
}
<content>履弑布爽</content>
输出：{
    "answer": "lǚ shì bù shuǎng"
}
<content>哆咄易鳝</content>
输出：{
    "answer": "duō duō yì shàn"
}

本题目给出的短语如下：
"""
    return system_prompt

get_homo2py_user_prompt=get_idiom2py_user_prompt

# eval 2


def get_py2idiom_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的拼音，写出它所对应的成语，以json格式输出答案。示例如下：
<pinyin>wú yǔ lún bǐ</pinyin>
输出：{
    "answer": "无与伦比"
}
<pinyin>lǚ shì bù shuǎng</pinyin>
输出：{
    "answer": "屡试不爽"
}
<pinyin>duō duō yì shàn</pinyin>
输出：{
    "answer": "多多益善"
}

本题目给出的拼音如下：
"""
    return system_prompt


def get_py2idiom_user_prompt(py):
    template = "<pinyin>{py}</pinyin>"
    user_prompt = template.format(py=py)
    return user_prompt


def get_sim_py2idiom_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的拼音，猜出和它在读音上最相近的四字成语，以json格式输出答案。示例如下：
<pinyin>shú yǔ pén bǐ</pinyin>
输出：{
    "answer": "无与伦比"
}
<pinyin>lǜ shī bǔ shuāng</pinyin>
输出：{
    "answer": "屡试不爽"
}
<pinyin>duō pō yì bàn</pinyin>
输出：{
    "answer": "多多益善"
}

本题目给出的拼音如下：
"""
    return system_prompt


def get_sim_py2idiom_user_prompt(py):
    template = "<pinyin>{py}</pinyin>"
    user_prompt = template.format(py=py)
    return user_prompt


def get_phrase2py_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的句子以及从句子中提取出来的短语，写出短语在句子中的语境下所对应的标准普通话拼音(各汉字对应的拼音之间以空格隔开），以json格式输出答案。示例如下：
<sentence>大户人家的小王犯了两项家规，父亲决定对小王数罪并罚，也就是家法结合律。</sentence>
<content>家法结合律</content>
输出：{
    "answer": "jiā fǎ jié hé lǜ"
}
<sentence>有人踩了笛卡尔一脚，笛卡尔：没事儿，因为我是恕学家。</sentence>
<content>恕学家</content>
输出：{
    "answer": "shù xué jiā"
}
<sentence>食材越多，越容易作出更多的菜，或许这就是多多益膳。</sentence>
<content>多多益膳</content>
输出：{
    "answer": "duō duō yì shàn"
}

本题目给出的句子和短语如下：
"""
    return system_prompt


def get_phrase2py_user_prompt(sentence, content):
    template = "<sentence>{sentence}</sentence>\n<content>{content}</content>"
    user_prompt = template.format(sentence=sentence, content=content)
    return user_prompt

# eval 2


def get_py2phrase_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的拼音，写出它所对应的最常用的短语（包括词语、成语），以json格式输出答案。示例如下：
<pinyin>jiā fǎ jié hé lǜ</pinyin>
输出：{
    "answer": "加法结合律"
}
<pinyin>shù xué jiā</pinyin>
输出：{
    "answer": "数学家"
}
<pinyin>duō duō yì shàn</pinyin>
输出：{
    "answer": "多多益善"
}

本题目给出的拼音如下：
"""
    return system_prompt


def get_py2phrase_user_prompt(py):
    template = "<pinyin>{py}</pinyin>"
    user_prompt = template.format(py=py)
    return user_prompt


def get_sim_pert2idiom_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请根据下面给出的一个“短语”，猜出和它在读音上最相近的四字成语（不要考虑语义），以json格式输出答案。示例如下：
<content>孰语盆笔</content>
输出：{
    "answer": "无与伦比"
}
<content>律师捕霜</content>
输出：{
    "answer": "屡试不爽"
}
<content>王杨捕劳</content>
输出：{
    "answer": "亡羊补牢"
}

本题目给出的短语如下：
"""
    return system_prompt


def get_sim_pert2idiom_user_prompt(w):
    template = "<content>{w}</content>"
    user_prompt = template.format(w=w)
    return user_prompt


def get_sim_word4word_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请从四个选项中，选出在读音上和给出的词语最接近的一项（不要考虑语义），以json格式输出答案。示例如下：
<content>技法</content>
<choices>
A. 家法
B. 依法
C. 办法
D. 立法
</choices>
输出：{
    "answer": "D"
}
<content>增添</content>
<choices>
A. 今天
B. 春天
C. 昨天
D. 成天
</choices>
输出：{
    "answer": "B"
}
<content>渐渐</content>
<choices>
A. 健全
B. 建议
C. 间接
D. 见面
</choices>
输出：{
    "answer": "D"
}

本题目给出的词语和选项如下：
"""
    return system_prompt


def get_sim_word4word_user_prompt(w, choices):
    A, B, C, D = choices
    template = """<content>{w}</content>
<choices>
A. {A}
B. {B}
C. {C}
D. {D}
</choices>
"""
    user_prompt = template.format(w=w, A=A, B=B, C=C, D=D)
    return user_prompt


def get_sim_py4py_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请从四个拼音选项中，选出和给出的拼音读音最接近的一项，以json格式输出答案。示例如下：
<content>jì fǎ</content>
<choices>
A. jiā fǎ
B. yī fǎ
C. bàn fǎ
D. lì fǎ
</choices>
输出：{
    "answer": "D"
}
<content>zēng tiān</content>
<choices>
A. jīn tiān
B. chūn tiān
C. zuó tiān
D. chéng tiān
</choices>
输出：{
    "answer": "B"
}
<content>jiàn jiàn</content>
<choices>
A. jiàn quán
B. jiàn yì
C. jiàn jiē
D. jiàn miàn
</choices>
输出：{
    "answer": "D"
}

本题目给出的拼音和选项如下：
"""
    return system_prompt


def get_sim_py4py_user_prompt(py, choices):
    A, B, C, D = choices
    template = """<content>{py}</content>
<choices>
A. {A}
B. {B}
C. {C}
D. {D}
</choices>
"""
    user_prompt = template.format(py=py, A=A, B=B, C=C, D=D)
    return user_prompt


def get_pun_sys_prompt():
    system_prompt = """你是一位精通汉语的大师。请从下面给出的包含谐音梗的句子中，抽取出关键的谐音部分，并写出它所对应的常用语（包括词语、成语），以json格式输出答案。示例如下：
<sentence>红色的圆形印章，简单来说，就是，朱圆章。</sentence>
输出：{
    "pun word": "朱圆章",
    "alternative word": "朱元璋"
}
<sentence>龙下凡，我接他，他说需要用雨水才能接他，于是我盛雨接龙。</sentence>
输出：{
    "pun word": "盛雨接龙",
    "alternative word": "成语接龙"
}
<sentence>据理力争的女律师被评为当代据理夫人。</sentence>
输出：{
    "pun word": "据理夫人",
    "alternative word": "居里夫人"
}

本题目给出的句子如下：
"""
    return system_prompt


def get_pun_user_prompt(content):
    template = "<sentence>{content}</sentence>"
    user_prompt = template.format(content=content)
    return user_prompt


def get_rhyming1_sys_prompt():
    system_prompt = """你是一位使用汉语的作词人，需要根据既有的参考短句，创作出一句和它押韵的短句（且韵脚字不雷同）。注意，如果两个汉字的韵母出现在下面的同一组中，我们认为它们相互押韵（不要求声调相同）。

<groups>
第一组：a、ia、ua（如“他”“家”“瓜”）；
第二组：o、uo（如“波”“诺”）;
第三组：e（如“鹅”）；
第四组：ie、üe（如“接”“月”）；
第五组：er（如“而”）；
第六组：i、ü（如“知”“及”“鱼”）；
第七组：u（如“姑”）；
第八组：ai、uai（如“来”“乖”）；
第九组：ei、uei（如“雷”“鬼”）；
第十组：ao、iao（如“老”“交”）；
第十一组：ou、iou（如“楼”“有”）；
第十二组：an、uan、ian、üan（如“安”“关”“先”“远”）；
第十三组：en、uen（如“恩”“文”）；
第十四组：in、ün（如“音”“云”）；
第十五组：ang、uang、iang（如“昂”“光”“想”）；
第十六组：ing（如“英”）；
第十七组：eng、ueng（如"成"“风”“翁”）；
第十八组：ong、iong（如“龙”“雄”）。
</groups>

请以json格式输出答案。示例如下：
<reference>一瞬间想起了那时候的自己</reference>
输出：{
"answer": "孤独的我在梦里寻觅"
}
<reference>我有了你生命才有希望</reference>
输出：{
"answer": "多希望有一个让我依靠的肩膀"
}
<reference>付出所有的青春不留遗憾</reference>
输出：{
"answer": "用慈爱做花环，人与人不冷淡"
}
请根据下面的参考短句生成押韵的短句：
"""
    return system_prompt


def get_rhyming1_user_prompt(content):
    template = "<reference>{content}</reference>"
    user_prompt = template.format(content=content)
    return user_prompt


def get_rhyming2_sys_prompt():
    system_prompt = """你是一位使用汉语的作词人，需要根据既有的参考短句，创作出一句和它双押的短句，要求它最后两个字和参考短句的最后两个字分别押韵（且韵脚字不雷同）。注意，如果两个汉字的韵母出现在下面的同一组中，我们认为它们相互押韵（不要求声调相同）。

<groups>
第一组：a、ia、ua（如“他”“家”“瓜”）；
第二组：o、uo（如“波”“诺”）;
第三组：e（如“鹅”）；
第四组：ie、üe（如“接”“月”）；
第五组：er（如“而”）；
第六组：i、ü（如“知”“及”“鱼”）；
第七组：u（如“姑”）；
第八组：ai、uai（如“来”“乖”）；
第九组：ei、uei（如“雷”“鬼”）；
第十组：ao、iao（如“老”“交”）；
第十一组：ou、iou（如“楼”“有”）；
第十二组：an、uan、ian、üan（如“安”“关”“先”“远”）；
第十三组：en、uen（如“恩”“文”）；
第十四组：in、ün（如“音”“云”）；
第十五组：ang、uang、iang（如“昂”“光”“想”）；
第十六组：ing（如“英”）；
第十七组：eng、ueng（如"成"“风”“翁”）；
第十八组：ong、iong（如“龙”“雄”）。
</groups>

请以json格式输出答案。示例如下：
<reference>一瞬间想起了那时候的自己</reference>
输出：{
"answer": "在塞纳河边的回忆你和谁在一起"
}
<reference>我有了你生命才有希望</reference>
输出：{
"answer": "破碎的心失去依傍"
}
<reference>付出所有的青春不留遗憾</reference>
输出：{
"answer": "你知道的我有半夜敲文字的习惯"
}
请根据下面的参考短句生成双押的短句：
"""
    return system_prompt


def get_rhyming2_user_prompt(content):
    template = "<reference>{content}</reference>"
    user_prompt = template.format(content=content)
    return user_prompt

    
def get_audio_sim_word4word_script(w,choices):
    A, B, C, D = choices
    template = """你是一位精通汉语的大师。请从四个选项中，选出在读音上和给出的词语最接近的一项（不要考虑语义），以json格式输出答案。本题给出的词语是：{w}。四个选项分别是：A. {A}；B. {B}；C. {C}；D. {D}。"""
    script = template.format(w=w, A=A, B=B, C=C, D=D)
    return script
    

def get_audio_sim_pert2idiom_script(w):
    template = """你是一位精通汉语的大师。请根据下面给出的一个“短语”，猜出和它在读音上最相近的四字成语，以json格式输出答案。本题给出的短语是：{w}。
"""
    script=template.format(w=w)
    return script

def get_audio_homo2idiom_script(w):
    template = """你是一位精通汉语的大师。请听写出下面我读出的四字成语，以json格式输出答案。本题给出的成语是：{w}。
"""
    script=template.format(w=w)
    return script

# ...existing code...

PROMPT_MAP = {
    "char2py": {
        "sys": get_char2py_sys_prompt,
        "user": get_char2py_user_prompt,
    },
    "char2bp": {
        "sys": get_char2bp_sys_prompt,
        "user": get_char2bp_user_prompt,
    },
    "char2chars": {
        "sys": get_char2chars_sys_prompt,
        "user": get_char2chars_user_prompt,
    },
    "py2chars": {
        "sys": get_py2chars_sys_prompt,
        "user": get_py2chars_user_prompt,
    },
    "idiom2py": {
        "sys": get_idiom2py_sys_prompt,
        "user": get_idiom2py_user_prompt,
    },
    "homo2py": {
        "sys": get_homo2py_sys_prompt,
        "user": get_homo2py_user_prompt,
    },
    "py2idiom": {
        "sys": get_py2idiom_sys_prompt,
        "user": get_py2idiom_user_prompt,
    },
    "sim_py2idiom": {
        "sys": get_sim_py2idiom_sys_prompt,
        "user": get_sim_py2idiom_user_prompt,
    },
    "phrase2py": {
        "sys": get_phrase2py_sys_prompt,
        "user": get_phrase2py_user_prompt,
    },
    "py2phrase": {
        "sys": get_py2phrase_sys_prompt,
        "user": get_py2phrase_user_prompt,
    },
    "sim_pert2idiom": {
        "sys": get_sim_pert2idiom_sys_prompt,
        "user": get_sim_pert2idiom_user_prompt,
    },
    "sim_word4word": {
        "sys": get_sim_word4word_sys_prompt,
        "user": get_sim_word4word_user_prompt,
    },
    "sim_py4py": {
        "sys": get_sim_py4py_sys_prompt,
        "user": get_sim_py4py_user_prompt,
    },
    "pun": {
        "sys": get_pun_sys_prompt,
        "user": get_pun_user_prompt,
    },
    "rhyming1": {
        "sys": get_rhyming1_sys_prompt,
        "user": get_rhyming1_user_prompt,
    },
    "rhyming2": {
        "sys": get_rhyming2_sys_prompt,
        "user": get_rhyming2_user_prompt,
    },
    "audio_sim_pert2idiom": {
        "script": get_audio_sim_pert2idiom_script,
    },
    "audio_homo2idiom": {
        "script": get_audio_homo2idiom_script,
    },
    "audio_sim_word4word": {
        "script": get_audio_sim_word4word_script,
    },
}

# Usage example:
# sys_prompt = PROMPT_MAP["char2py"]["sys"]()
# user_prompt = PROMPT_MAP["char2py"]["user"]("好")

if __name__ == "__main__":
    print(get_char2py_user_prompt("好"))
