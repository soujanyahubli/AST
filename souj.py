import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

def create_rule(rule_string):
    def parse_expression(expr):
        tokens = re.split(r'(\sAND\s|\sOR\s)', expr)
        if len(tokens) == 3:
            operator = tokens[1].strip()
            return Node(
                node_type="operator",
                value=operator,
                left=parse_expression(tokens[0].strip()),
                right=parse_expression(tokens[2].strip())
            )
        return Node(node_type="operand", value=expr.strip())
    
    return parse_expression(rule_string)

def combine_rules(rule_list):
    combined_ast = None
    for rule in rule_list:
        rule_ast = create_rule(rule)
        if combined_ast is None:
            combined_ast = rule_ast
        else:
            combined_ast = Node(
                node_type="operator",
                value="AND",
                left=combined_ast,
                right=rule_ast
            )
    return combined_ast

def evaluate_rule(ast, data):
    def eval_condition(condition, data):
        attribute, operator, value = re.split(r'([><=]+)', condition)
        attribute = attribute.strip()
        value = value.strip().replace("'", "")
        
        if attribute not in data:
            raise ValueError(f"Missing attribute: {attribute}")
        
        if operator == ">":
            return data[attribute] > int(value)
        elif operator == "<":
            return data[attribute] < int(value)
        elif operator == "=":
            return data[attribute] == value
        else:
            raise ValueError(f"Invalid operator: {operator}")
    
    if ast.node_type == "operand":
        return eval_condition(ast.value, data)
    elif ast.node_type == "operator":
        left_eval = evaluate_rule(ast.left, data)
        right_eval = evaluate_rule(ast.right, data)
        if ast.value == "AND":
            return left_eval and right_eval
        elif ast.value == "OR":
            return left_eval or right_eval
        else:
            raise ValueError(f"Invalid operator in AST: {ast.value}")

def main():
    rule1 = "age > 30 AND department = 'Sales'"
    rule2 = "salary > 50000 OR experience > 5"
    
    ast_rule1 = create_rule(rule1)
    ast_rule2 = create_rule(rule2)
    
    combined_ast = combine_rules([rule1, rule2])
    
    data = {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }
    
    result = evaluate_rule(combined_ast, data)
    print(f"Evaluation result: {result}")

if __name__ == "__main__":
    main()
