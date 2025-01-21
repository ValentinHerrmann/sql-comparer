import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Where, Comparison, Function, Parenthesis
from sqlparse.tokens import Keyword, DML, Name, Wildcard

import Helper as He

        
#####################################
#####################################

def _identifier(identifier, alias_map, baseDict: dict):
        if isinstance(identifier, Identifier):
            if identifier.get_real_name() and identifier.get_parent_name() and identifier.get_parent_name().lower() in alias_map.keys():
                return f"{alias_map[identifier.get_parent_name().lower()].lower()}.{identifier.get_real_name().lower()}"
            elif identifier.get_real_name():
                tables = He.findTableForColumn(baseDict, identifier.get_real_name(), alias_map.keys())
                if len(tables) == 1:
                    alias_map[tables[0].lower()] = tables[0]
                    return f"{tables[0].lower()}.{identifier.get_real_name().lower()}"
                else:
                    return f"{identifier.get_real_name().lower()}"
        return str(identifier)

        
#####################################
#####################################


def _select(select, alias_map, baseDict: dict, insideFunction=False):
    select_tokens = []
    for token in select.tokens:
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                select_tokens.append(f"{_identifier(identifier, alias_map, baseDict).lower()} as {identifier.get_real_name().lower()}")
        elif isinstance(token, Identifier):
            if insideFunction:
                select_tokens.append(_identifier(token, alias_map, baseDict).lower())
            else:
                select_tokens.append(f"{_identifier(token, alias_map,  baseDict).lower()} as {token.get_real_name().lower()}")
        elif isinstance(token, Function):
            #select_tokens.append(f"{token.get_name().lower()}({_identifier(token.get_parameters(), alias_map, baseDict).lower()})")
            for par in token.tokens:
                if isinstance(par, Identifier):
                    select_tokens.append(par.get_name().lower()+"(")
                if isinstance(par, Parenthesis):
                    select_tokens[-1] += _select(par, alias_map, baseDict, True)+") as funcResult" 
        elif token.ttype is Wildcard:
            select_tokens.append("*")
        else:
            continue
    select_tokens.sort()
    return ",".join(select_tokens)


#####################################
#####################################


def _from(from_, alias_map, baseDict: dict):
    from_tokens = []
    if hasattr(from_, 'tokens'):
        for token in from_.tokens:
            if isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    alias_map[identifier.get_real_name().lower()] = identifier.get_alias() or identifier.get_real_name()
                    from_tokens.append(f"{identifier.get_real_name().lower()} {alias_map[identifier.get_real_name().lower()].lower()}")
            elif isinstance(token, Identifier):
                alias_map[token.get_real_name().lower()] = token.get_alias() or token.get_real_name()
                from_tokens.append(f"{token.get_real_name().lower()} {alias_map[token.get_real_name().lower()].lower()}")
            elif token.ttype is not None and token.ttype is Name:
                alias_map[token.value.lower()] = token.value.lower()
                from_tokens.append(f"{token.value.lower()} {alias_map[token.value.lower()].lower()}")
            else:
                continue
    from_tokens.sort()
    return ",".join(from_tokens)


#####################################
#####################################


def _groupby(groupby_, alias_map, baseDict: dict):
    groupby_tokens = []
    if(isinstance(groupby_, Identifier)):
        groupby_tokens.append(_identifier(groupby_, alias_map, baseDict).lower())
    elif isinstance(groupby_, IdentifierList):
        for identifier in groupby_.get_identifiers():
            groupby_tokens.append(_identifier(identifier, alias_map, baseDict).lower())
    groupby_tokens.sort()
    return ",".join(groupby_tokens)

def _condition(token, alias_map, baseDict: dict):
    left, operator, right = [t for t in token.tokens if not t.is_whitespace]

    flipAllowed = True
    leftLiteral = False
    rightLiteral = False

    if is_value(right):
        flipAllowed = False
        rightLiteral = True

    if is_value(left):
        left, right = right, left
        if operator.value == ">":
            operator.value = "<"
        elif operator.value == "<":
            operator.value = ">"
        leftLiteral = rightLiteral
        rightLiteral = True
        flipAllowed = False

    left = _identifier(left, alias_map, baseDict)
    right = _identifier(right, alias_map, baseDict)

    if flipAllowed and left.lower() >= right.lower():
        left, right = right, left
        if operator.value == ">":
            operator = "<"
        elif operator.value == "<":
            operator = ">"

    return f"{left if leftLiteral else left.lower()} {operator} {right if rightLiteral else right.lower()}"

def is_value(token):
    return token.ttype in (sqlparse.tokens.Token.Literal.Number.Integer,
                            sqlparse.tokens.Token.Literal.Number.Float,
                            sqlparse.tokens.Token.Literal.String.Single,
                            sqlparse.tokens.Token.Literal.String.Symbol)



#####################################
#####################################


def _paranthesis(parenthesis, alias_map, baseDict: dict):
    toks = []

    bracketsRequired = True
    closeBracketsAfterNext = False

    and_count = sum(1 for token in parenthesis.tokens if token.ttype is Keyword and token.value == "AND")  # Zähle "AND"-Tokens
    or_count = sum(1 for token in parenthesis.tokens if token.ttype is Keyword and token.value == "OR")  # Zähle "AND"-Tokens


    if(and_count==1 and or_count == 0):
        val = _2element_par(parenthesis, alias_map, baseDict, "AND")
        return val
    elif(and_count==0 and or_count == 1):
        val = _2element_par(parenthesis, alias_map, baseDict, "OR")
        return val




    for token in parenthesis.tokens:
        if isinstance(token, Comparison):
            toks.append(_condition(token, alias_map, baseDict))
        elif isinstance(token, Parenthesis):
            toks.append(_paranthesis(token, alias_map, baseDict))

        elif token.ttype is Keyword: #AND,OR
            if token.value == "AND":
                pass
            elif token.value == "OR":
                pass
            elif token.value == "NOT":
                pass

        elif token.value == '(':
            toks.append(token.value)
        else:
            continue
    x = parenthesis.flatten()
    return " ".join(toks)


def _2element_par(parenthesis, alias_map, baseDict: dict, keyword):
    toks = []

    for token in parenthesis.tokens:
        if isinstance(token, Comparison):
            toks.append(_condition(token, alias_map, baseDict))
        elif isinstance(token, Parenthesis):
            toks.append(_paranthesis(token, alias_map, baseDict))
    toks = toks.sort()
    fill = (" "+keyword+" ")
    return fill.join(toks)


def count_keywordValues_tokens(tokens, values):
    return len([token for token in tokens if token.ttype is Keyword and token.value.upper() in values])


def _where(where, alias_map, baseDict: dict, query: str):
    conditions = []
    current_condition = []

    and_count = count_keywordValues_tokens(where.tokens, ['AND'])
    or_count = count_keywordValues_tokens(where.tokens, ['OR'])


    # No AND / OR
    if and_count + or_count == 0:
        return _where_simpleCondition(where, alias_map, baseDict)
    # only ANDs / only ORs
    elif and_count == 0 or or_count == 0:
        return _where_sameStrengthKeywords(where, alias_map, baseDict, " AND " if and_count > 0 else " OR ")






    for token in where.tokens:
        if token.is_whitespace or (token.ttype is Keyword and token.value.upper() == "WHERE"):
            continue

        if token.ttype is Keyword and token.value.upper() in ('AND', 'OR'):
            if current_condition:
                conditions.append(''.join(str(t) for t in current_condition).strip())
                current_condition = []
            conditions.append(token.value.upper())
        else:
            current_condition.append(token)

    if current_condition:
        conditions.append(''.join(str(t) for t in current_condition).strip())

    sorted_conditions = []
    current_group = []
    last_connector = ""

    if "OR" not in conditions:
        for condition in conditions:
            if condition == 'AND':
                pass
            else:
                current_group.append(condition)

        if current_group:
            sorted_conditions.extend(sorted(current_group))

        return " AND ".join(sorted_conditions)
    else:
        return " ".join(conditions)

        where_index = query.upper().find('WHERE')
        
        normalized_query = query[:where_index + 5] + ' ' + ' '.join(sorted_conditions)



def _where_simpleCondition(where, alias_map, baseDict: dict):
    cond = []
    for tok in where.tokens:
        if isinstance(tok, Comparison):
            cond.append(_condition(tok, alias_map, baseDict))
        elif isinstance(tok, Parenthesis):
            for _tok in tok.tokens:
                if isinstance(_tok, Comparison):
                    cond.append(_condition(_tok, alias_map, baseDict))
                elif isinstance(_tok, Parenthesis):
                    tok = _tok
    return "".join(cond)

def _where_sameStrengthKeywords(where, alias_map, baseDict: dict, keyword: str):
    cond = []
    for tok in where.tokens:
        if isinstance(tok, Comparison):
            cond.append(_condition(tok, alias_map, baseDict))
        elif isinstance(tok, Parenthesis):
            for _tok in tok.tokens:
                if isinstance(_tok, Comparison):
                    cond.append(_condition(_tok, alias_map, baseDict))
                elif isinstance(_tok, Parenthesis):
                    tok = _tok
    cond.sort()
    return keyword.join(cond)







def _where_xx(where, alias_map, baseDict: dict):
    where_tokens = []
    for token in where.tokens:

        if isinstance(token, Comparison):
            left, operator, right = [t for t in token.tokens if not t.is_whitespace]
            left = _identifier(left, alias_map, baseDict)
            right = _identifier(right, alias_map, baseDict)
            if left.lower() >= right.lower():
                left, right = right, left
                if operator.value == ">":
                    operator = "<"
                elif operator.value == "<":
                    operator = ">"

            where_tokens.append(f"{left.lower()} {operator} {right.lower()}")
        elif token.ttype is Keyword:
            where_tokens.append(token.value.upper())
        elif token.is_whitespace or (token.ttype is Keyword and token.value.upper() == "WHERE"):
            continue
        else:
            where_tokens.append(str(token))
    return " ".join(where_tokens)