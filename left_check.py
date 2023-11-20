# 判断左递归
def check_left_recursion(productions, nonterminal, visited):
    if nonterminal in visited:
        return True

    visited.add(nonterminal)

    for production in productions:
        rule = production[1].split('|')
        for term in rule:
            if term.strip()[0] == nonterminal:
                if check_left_recursion(productions, nonterminal, visited):
                    return True

    visited.remove(nonterminal)
    return False

# 判断左因子
def check_left_factoring(productions):
    for nonterminal, terms in productions:
        prefixes = {}
        for term in terms.split('|'):
            prefix = term.strip()[0]
            if prefix not in prefixes:
                prefixes[prefix] = []
            prefixes[prefix].append(term)

        for prefix in prefixes:
            if len(prefixes[prefix]) > 1:
                print(f"左公因子 {prefix} 存在于产生式 {prefixes[prefix]}")
                return True

    return False

# grammar 存在左公因子或左递归的文法列表
# return new_grammar 改造后的文法列表
def left_common_factor_or_recursion(grammar):
    parsed_grammar = [(rule[0], rule[1]) for rule in grammar]

    left_recursion_present = False
    left_factoring_present = False

    for nonterminal, terms in parsed_grammar:
        if check_left_recursion(parsed_grammar, nonterminal, set()):
            left_recursion_present = True
            break

        if check_left_factoring(parsed_grammar):
            left_factoring_present = True
            break

    if left_recursion_present or left_factoring_present:
        return True

    return False

# 示例非LL(1)文法列表
# non_ll1_grammar = [
#     ('S', 'a|∧|(T)'),
#     ('T', 'T,S|S'),
#     # Add more grammars here for testing
# ]

# result = left_common_factor_or_recursion(non_ll1_grammar)
# if result:
#     print("存在左公因子或左递归")
# else:
#     print("不存在左公因子或左递归")
