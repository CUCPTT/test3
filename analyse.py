import re
import tkinter as tk
from tkinter import ttk
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
    print("select:")
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


# 构造预测分析表
def forecast_analysis_table():
    # 行表示非终结符，列表示终结符
    global f_a_table
    # 创建空的二维列表
    vt.append('#')
    f_a_table = [['' for i in range(len(vt))] for j in range(len(vn))]
    for i in range(len(vn)):
        for j in range(len(vt)):
            for n in range(len(a)):
                if vn[i] == a[n][0]:
                    if vt[j] in select[n]:
                        f_a_table[i][j] = str_list(a[n][1:])
    print(vn)
    print(vt)
    print("此文法的预测分析表为：")
    print(f_a_table)

# 将列表中的元素变成字符串
def str_list(x):
    b = [str(j) for j in x]
    str2 = ''.join(b)
    return str2

# 分析过程
def analyse(g, string):
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


    first_all_not_terminal()
    first_all_string()
    follow_all()
    select_all()
    forecast_analysis_table()
    root = tk.Tk()
    root.title("对"+string+"的分析过程")
    
    # 创建标题标签
    title_label = tk.Label(root, text="对"+string+"的分析过程", font=("Arial", 12))
    title_label.pack(pady=10)
    
    # 创建表格
    table = ttk.Treeview(root,height=20)
    table["columns"] = ("Steps", "AnalyzeStack", "RemainingInputString","ProductionOrMatch")
    # 显示表格并设置垂直滚动条
    vsb = ttk.Scrollbar(root, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    table.pack(expand=True, fill="both", pady=200) # 设置表格的初始高度
    # 设置表格的位置和大小
    table.place( width=500, height=800)
    # 设置列宽
    table.column("#0", width=0, stretch=tk.NO)
    table.column("Steps", width=100)
    table.column("AnalyzeStack", width=100)
    table.column("RemainingInputString", width=100)
    table.column("ProductionOrMatch", width=150)
    
    # 设置列标题
    table.heading("#0", text="", anchor=tk.W)
    table.heading("Steps", text="步骤")
    table.heading("AnalyzeStack", text="分析栈")
    table.heading("RemainingInputString", text="剩余输入串")
    table.heading("ProductionOrMatch", text="推导所用产生式或匹配")
    stack = '#'+a[0][0]
    string = string + '#'
    cnt = 0
    flag = 1
    while string != '#' or stack != '#':
        if stack[-1] in vn:
            for i in range(len(vn)):
                for j in range(len(vt)):
                    if stack[-1] == vn[i] and string[0] == vt[j]:
                        if f_a_table[i][j] != '':
                            cnt = cnt + 1
                            table.insert("", tk.END, text=str(cnt), values=(str(cnt), stack, string,stack[-1]+' -> '+f_a_table[i][j]))
                            stack = stack[0:-1]
                            if f_a_table[i][j] != 'ε':
                                stack = stack + f_a_table[i][j][-1::-1]
                        else:
                            cnt = cnt + 1
                            table.insert("", tk.END, text=str(cnt), values=(str(cnt), stack, string,'拒绝'))
                            flag = 0
                            stack = '#'
                            string = '#'
        else:
            if stack[-1] == string[0]:
                cnt = cnt + 1
                table.insert("", tk.END, text=str(cnt), values=(str(cnt), stack, string,'"'+stack[-1]+'"'+'匹配'))
                stack = stack[0:-1]
                string = string[1:]
            else:
                cnt = cnt + 1
                table.insert("", tk.END, text=str(cnt), values=(str(cnt), stack, string,'拒绝'))
                flag = 0
                stack = '#'
                string = '#'

    if flag:
        cnt = cnt +1
        table.insert("", tk.END, text=str(cnt), values=(str(cnt), '#', '#','接受'))

    # 显示表格
    table.pack()
    
    # 运行主循环
    root.mainloop()


# 测试没有出现问题
# g = [('E', 'TD'), ('D', '+E|ε'),('T','FS'),('S','T|ε'),('F','PM'),('M','*M|ε'),('P','(E)|a|b|^')]

# string = "(a+b)*b+a"

# analyse(g,string)
