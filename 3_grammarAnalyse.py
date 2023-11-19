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

def check_left_factoring(productions):
    # 检查左公因子的逻辑
    # 实现左公因子检查的算法
    pass

def left_common_factor_or_recursion(grammar):
    parsed_grammar = [(rule[0], rule[1]) for rule in grammar]

    left_recursion_present = False
    left_factoring_present = False

    for nonterminal, terms in parsed_grammar:
        if check_left_recursion(parsed_grammar, nonterminal, set()):
            left_recursion_present = True
            break

        if check_left_factoring(terms):
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
