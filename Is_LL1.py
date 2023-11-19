import re

# 求非终结符在vn的位置，即索引
def index(x):
    for n in range(len(vn)):
        if x == vn[n]:
            return n
    return None

# 判断是不是终结符
def judge_terminal(x):
    if x in vn:
        return False
    else:
        return True


# 求所有非终结符的first集
def first_all_not_terminal():
    global  f
    f = []
    for i in range(len(vn)):
        f = f + [set()]

    for num in range(len(grammar)):
        for s in vn:
            first_single_not_terminal(s)
    print('非终结符的FIRST集依次为：')
    print(f)

# 求单个非终结符的first集
def first_single_not_terminal(x):

    index_start = index(x)  # 非终结符x在vn的位置
    for i in a:
        if i[0] == x: # x为非终结符
            # 右边第一个为终结符
            for j in range(1, len(i)):
                if judge_terminal(i[j]):
                    # 直接添加此终结符
                    f[index_start].add(i[j])
                    break
                # 当右边第一个为非终结符时
                else:
                    # 当此first集没有空串时，直接添加此first集给开始符x
                    index_next = index(i[j])
                    if index_next is not None and 'ε' not in f[index_next]:
                        f[index_start].update(f[index_next])
                        break
                    # 如果此first集含有空串时
                    else:
                        if j == len(i) - 1:
                            break
                        # 添加去掉空串的first集
                        if index_next is not None:
                            f[index_start].update(f[index_next] - {'ε'})

                        index_next_next = index(i[j+1])  # 后面的符号的位置
                        # 添加后面的符号的first集
                        if index_next_next is not None:
                            f[index_start].update(f[index_next_next])


# 求所有文法的First集
def first_all_string():
    global f1
    f1 = []
    for i in range(len(grammar)):
        f1 = f1 + [set()]

    for num in range(len(vn)):
        for i in range(len(grammar)):
            first_single_string(i)

    print('文法的FIRST集依次为：')
    print(f1)

# 求单个文法的first集
def first_single_string(num): # num表示文法的位置
    string = a[num] # 单独的一串文法
    for i in range(1,len(string)):
        # 如果遇到终结符，将终结符添加进去，并且跳出循环
        if judge_terminal(string[i]):
            f1[num].add(string[i])
            break
        # 是非终结符，则添加去掉空串的first集
        else:
            index_next = index(string[i]) # 记录此非终结符在vn的位置
            # 如果没有空串
            if 'ε' not in f[index_next]:
                for e in f[index_next]:
                    f1[num].add(e)
                break
            # 如果有空串
            else:
                for e in f[index_next]:
                    if e != 'ε':
                        f1[num].add(e)
                if i == len(string) -1 :
                    break
                index_next_next = index(string[i+1])
                for e in f[index_next_next]:
                    f1[num].add(e)


# 求所有非终结符的follow集
def follow_all():
    global follow
    follow = []
    for i in range(len(vn)):
        follow = follow + [set()]
        follow[0].add("#") 

    for num in range(len(grammar)):
        for s in vn: # s为非终结符
            follow_single(s)
    print('非终结符的follow集依次为：')
    print(follow)

# 求单个非终结符的follow集
def follow_single(s):
    index_vn = index(s) # 表示当前非终结符在vn的位置
    for i in a:
        index_vn_start = index(i[0]) # 表示当前非终结符所在的文法的开始符在vn的位置
        for j in range(1,len(i)):
            if s == i[j]: # j表示非终结符s在文法a中的位置
                # 如果非终结符在文法的末尾，此时非终结符的follow集为文法开始符的follow集
                if j == len(i) - 1:
                    for e in follow[index_vn_start]:
                        if e != 'ε': # follow集不能有空串
                            follow[index_vn].add(e)
                    break
                # 如果非终结符不在文法的末尾
                else:
                    # 如果后面跟着的是终结符
                    if judge_terminal(i[j+1]):
                        follow[index_vn].add(i[j+1])
                        break 
                    # 如果后面跟着的是非终结符
                    else:
                        index_vn_next = index(i[j+1]) # 此非终结符后面跟着的非终结符在vn的位置
                        # 如果后面的非终结符的frist集不包含空串，直接添加它的first集
                        if 'ε' not in f[index_vn_next]:
                            for e in f[index_vn_next]:
                                follow[index_vn].add(e)
                        # 如果后面的非终结符的frist集包含空串
                        else:
                            # 加上去掉first集中的空串
                            for e in f[index_vn_next]:
                                if e != 'ε':
                                    follow[index_vn].add(e)
                            # 加上此文法开始符的follow集
                            for e in follow[index_vn_start]:
                                if e != 'ε':
                                    follow[index_vn].add(e)


# 求所有文法的select集
def select_all():
    global select
    select = []
    for i in range(len(grammar)):
        select = select + [set()]
        select_singe(i) # 注意i为整数

    print('文法的select集依次为：')
    print(select)

# 求单个文法的select集
def select_singe(i):
    str = a[i] # 存储对应的文法
    # 当文法的first集不包含空串
    if 'ε' not in f1[i]:
        for e in f1[i]:
            select[i].add(e)
    # 当文法的first集包含空串
    else:
        # 加上去掉空串的此文法的first集
        for e in f1[i]:
            if e != 'ε':
                select[i].add(e)
        index_start = index(str[0]) # 找出此文法的开始符在vn的位置
        for e in follow[index_start]:
            select[i].add(e)

# 判断是否为LL1文法
def judge_LL1():
    flag = 0
    for i in range(len(grammar)):
        for j in range(i + 1, len(grammar)): 
            if grammar[i][0] == grammar[j][0]:
                intersection = select[i] & select[j]
                if intersection:  # 判断是否有交集
                    print("不是LL(1)文法")
                    flag += 1
                    return False

    if flag == 0:
        print("是LL(1)文法")
        return True

# 主函数部分
def Is_LL1(g):
    global grammar, vn, vt, a
    grammar=[]
    vn = []
    vt=[]
    # a是列表，用来存储上下文无关文法
    a = []

    for symbol, production in g:
            # 使用正则表达式分隔字符串
            productions = re.split(r'\|', production)
            # 将分隔后的产生式添加到新的文法中
            for p in productions:
                grammar.append((symbol, p.strip()))

    # 非终结符
    for item in grammar:
        if item[0] not in vn:
            vn.append(item[0])

    # 终结符
    for i in [item[1] for item in grammar]:
        for j in i:
            if not j.isupper() and j not in vt and j != 'ε':
                vt.append(j)

    for one,two in grammar:
        a.append([one] + [char for char in two])

    print("非终结符",vn)
    print("终结符",vt)

    first_all_not_terminal()
    first_all_string()
    follow_all()
    select_all()
    return judge_LL1()

# 测试：
# 不是LL1
g = [('S', 'a|∧|(T)'), ('T', 'T,S|S')]  
# 是LL1
# g = [('E', 'TD'), ('D', '+E|ε'),('T','FS'),('S','T|ε'),('F','PM'),('M','*M|ε'),('P','(E)|a|b|^')]

print(Is_LL1(g))
