class Vn(object):
    def __init__(self, name, expression_list):
        self.name = name
        self.expression_list = expression_list
        self.to_terminal = "Unknown"
        self.first_list = []
        self.follow_list = []
        self.search_table = {}

    def show(self):
        print("non terminal name:", self.name)
        print("to terminal:", self.to_terminal)
        print("expression list:", self.expression_list)
        print("first list:", self.first_list)
        print("follow list:", self.follow_list)
        print("search table:", self.search_table)
        print()

class Language(object):
    def __init__(self):
        self.non_terminal_list = {}
        self.terminal_list = []
        self.now_vn_name = 0
        self.start_node = ""

    def parse_grammar(self,grammar):
        for non_terminal, expressions in grammar:
            expressions_list = expressions.split('|')
            vn = Vn(non_terminal, expressions_list)
            language.add_non_terminal(vn)
            if not self.start_node:
                self.start_node = non_terminal
            for expression in expressions_list:
                if expression == 'ε':
                    self.terminal_list.append('')  # 记录 ε 为空字符
                else:
                    for char in expression:
                        if not char.isupper():
                            self.terminal_list.append(char)

    def to_grammar(self, epsilon='ε'):
        grammar = []
        for vn_name, vn_obj in self.non_terminal_list.items():
            expressions = '|'.join([epsilon if exp == '' else exp for exp in vn_obj.expression_list])
            grammar.append((vn_name, expressions))
        return grammar

    def show(self, tips=""):
        print("--------------------this is language(", tips, ")--------------------")
        print("terminal list:", self.terminal_list)
        print("non terminal list:")
        print()
        for vn in self.non_terminal_list.values():
            vn.show()

    def add_non_terminal(self, vn):
        self.non_terminal_list[vn.name] = vn
        self.now_vn_name = chr(ord(vn.name) + 1)

def find(li, letter):
    try:
        return li.index(letter)
    except:
        return -1


def replace(exp):
    ans_list = []
    for e in language.non_terminal_list[exp[0]].expression_list:
        ans_list.append(exp.replace(exp[0], e, 1))
    return ans_list


def erase():
    order = list(language.non_terminal_list.keys())

    count1 = 0
    while count1 < len(language.non_terminal_list):
        vn = list(language.non_terminal_list.values())[count1]
        changeflag = True
        while changeflag:
            changeflag = False
            count2 = 0
            while count2 < len(vn.expression_list):
                exp = vn.expression_list[count2]
                if exp != "" and exp[0] not in language.terminal_list and find(order, exp[0]) > find(order, vn.name):
                    changeflag = True
                    vn.expression_list.pop(count2)
                    count2 -= 1
                    vn.expression_list.extend(replace(exp))
                count2 += 1
        count1 += 1

    language.show("after modify")

    count5 = 0
    while count5 < len(language.non_terminal_list):
        vn = list(language.non_terminal_list.values())[count5]
        count6_start = 0
        count6_end = 1
        vn.expression_list.sort() 
        while count6_start < len(vn.expression_list):
            express = vn.expression_list[count6_start]
            if express == "":
                count6_start += 1
                count6_end += 1
                continue

            if count6_end == len(vn.expression_list):
                if count6_end - count6_start == 1:
                    count6_start = count6_end
                else:
                    modified_list = []
                    for e in vn.expression_list[count6_start:count6_end]:
                        if len(e) == 1:
                            modified_list.append("")
                        else:
                            modified_list.append(e[1:])
                    new_vn = Vn(str(language.now_vn_name), modified_list)
                    vn.expression_list = vn.expression_list[0:count6_start] + [
                        express[0] + str(language.now_vn_name)]
                    language.add_non_terminal(new_vn)
                    count6_start += 1
                    count6_end = count6_start
                continue

            express_ = vn.expression_list[count6_end]
            if express[0] != express_[0]:
                if count6_end - count6_start == 1:
                    count6_start = count6_end
                else:
                    modified_list = []
                    for e in vn.expression_list[count6_start:count6_end]:
                        if len(e) == 1:
                            modified_list.append("")
                        else:
                            modified_list.append(e[1:])
                    new_vn = Vn(str(language.now_vn_name), modified_list)
                    vn.expression_list = vn.expression_list[0:count6_start] + [
                        express[0] + str(language.now_vn_name)] + vn.expression_list[count6_end:]
                    language.add_non_terminal(new_vn)
                    count6_start += 1
                    count6_end = count6_start
            count6_end += 1
        count5 += 1

    language.show("after extract")

    count4 = 0
    while count4 < len(language.non_terminal_list):
        vn = list(language.non_terminal_list.values())[count4]
        count3 = 0
        while count3 < len(vn.expression_list):
            expre = vn.expression_list[count3]
            if expre != "" and expre[0] not in language.terminal_list and expre[0] == vn.name:
                new_vn = Vn(str(language.now_vn_name), [expre[1:] + str(language.now_vn_name), ""])
                vn.expression_list.pop(count3)
                count3 -= 1
                for k in range(len(vn.expression_list)):
                    vn.expression_list[k] += str(language.now_vn_name)
                language.add_non_terminal(new_vn)
            count3 += 1
        count4 += 1


def delete():
    new_non_terminal_list = {language.start_node: language.non_terminal_list[language.start_node]}
    count1 = 0
    while count1 < len(new_non_terminal_list):
        vn = list(new_non_terminal_list.values())[count1]
        for exp in vn.expression_list:
            for letter in exp:
                if letter not in language.terminal_list:
                    new_non_terminal_list[letter] = language.non_terminal_list[letter]
        count1 += 1
    language.non_terminal_list = new_non_terminal_list
    language.show("after delete")

# grammar = [('A', 'Bb|c'), ('B', 'Aa')] # 这里对空串的处理好像还有点问题
# grammar = [('S', 'Ab|Ba'), ('A', 'Sa|Bc'), ('B','d')]
# grammar = [('S', 'a|∧|(T)'), ('T', 'T,S|S')]
# language = Language()
# language.parse_grammar(grammar)
# print(language.terminal_list)
# # language.start_node = "S"
# language.show("original")
# erase()
# language.show()
# delete()
language = Language()

def reform(grammar):
    language.parse_grammar(grammar)
    language.show("original")
    erase()
    language.show("after erase")
    delete()
    new_grammar = language.reverse_grammar()
    print(new_grammar)
    return(new_grammar)

# reform(grammar)