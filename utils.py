from elements_type import *


def create_predicate(p: str) -> Predicate:
    n = len(p)

    def _represent(start: int, losy: list) -> (int, list):

        while start < n and p[start] != ")":
            if p[start + 1] == "(":
                pp = Predicate(p[start])
                new_start, new_list = _represent(start + 2, [])
                pp.set_args(new_list)
                start = new_start
                losy.append(pp)
                continue
            if p[start].isupper():
                e = Constant(p[start])
            else:
                e = Variable(p[start])

            losy.append(e)
            start += 1

        return start + 1, losy

    present = _represent(0, [])[1][0]
    return present


def con_con(con1: Constant, con2: Constant) -> bool:
    return con1 == con2


def con_pred(con: Constant, pred: Predicate, sub_table: dict) -> bool:
    # if false then it's not equal to the constant otherwise
    sub = sub_table.get(pred)  # None or Constant
    if isinstance(sub, Constant):  # it's exist = constant
        return con_con(con, sub)
    sub_table[pred] = con
    return True


def con_var(con: Constant, var: Variable, sub_table: dict) -> bool:
    sub = sub_table.get(var)
    sub2 = sub_table.get(sub)
    if sub2 == var:
        sub_table[sub2] = con
        sub_table[sub] = con
    if isinstance(sub, Constant):
        return con_con(con, sub)
    if isinstance(sub, Predicate):
        return con_pred(con, sub, sub_table)
    if isinstance(sub, Variable):  # if substituted is Variable
        return con_var(con, sub, sub_table)
    sub_table[var] = con
    return True


def pred_pred(pred1: Predicate, pred2: Predicate, sub_table: dict) -> bool:
    sub1 = sub_table.get(pred1)  # either None or Constant
    sub2 = sub_table.get(pred2)  # either None or Constant
    if sub1 and sub2:  # both are Constants
        return con_con(sub1, sub2)
    if not sub1 and not sub2:  # both are None
        return pred1 == pred2
    if not sub1 and sub2:  # sub1 is None and sub2 is Constant
        sub_table[pred1] = sub2
    if sub1 and not sub2:  # sub1 is Constant and sub2 is None
        sub_table[pred2] = sub1
    return True


def var_pred(var: Variable, pred: Predicate, sub_table: dict) -> bool:
    sub1 = sub_table.get(pred)  # returns None or Constant
    sub2 = sub_table.get(var)  # returns None , Variable ,Predicate , Constant
    if sub1 is not None:  # is constant
        if isinstance(sub2, Constant):
            return con_con(sub1, sub2)
        elif isinstance(sub2, Variable):
            return con_var(sub1, sub2, sub_table)
        elif isinstance(sub2, Predicate):
            return con_pred(sub1, sub2, sub_table)
        sub_table[var] = sub1
    else:
        if isinstance(sub2, Constant):
            return con_pred(sub2, pred, sub_table)
        if isinstance(sub2, Variable):
            return var_pred(sub2, pred, sub_table)
        if isinstance(sub2, Predicate):
            return pred_pred(sub2, pred, sub_table)
        sub_table[var] = pred
    return True


def var_var(
    var1: Variable, var2: Variable, sub_table: dict, first_variable: Variable
) -> bool:
    sub1 = sub_table.get(var1)
    sub2 = sub_table.get(var2)
    if var1 == var2 or sub1 == first_variable:
        return True
    is_con1 = isinstance(sub1, Constant)
    is_con2 = isinstance(sub2, Constant)
    is_var1 = isinstance(sub1, Variable)
    is_var2 = isinstance(sub2, Variable)
    is_pred1 = isinstance(sub1, Predicate)
    is_pred2 = isinstance(sub2, Predicate)

    if is_var1:
        if is_con2:
            return con_var(sub2, sub1, sub_table)
        if is_pred2:
            return var_pred(sub1, sub2, sub_table)
        if is_var2:

            return var_var(sub1, sub2, sub_table, first_variable)
        sub_table[var2] = sub1
    elif is_con1:
        if is_con2:
            return con_con(sub1, sub2)
        if is_var2:
            return con_var(sub1, sub2, sub_table)
        if is_pred2:
            return con_pred(sub1, sub2, sub_table)
        sub_table[var2] = sub1
    elif is_pred1:
        if is_con2:
            return con_pred(sub2, sub1, sub_table)
        if is_var2:
            return var_pred(sub2, sub1, sub_table)
        if is_pred2:
            return pred_pred(sub1, sub2, sub_table)
        sub_table[var2] = sub1
    else:  # sub1 is None
        sub_table[var1] = (
            var2  # both are None , we need to add them to substitution set
        )
        if is_con2:  # sub1 is None and sub2 is Constant
            return con_var(sub2, var1, sub_table)
        if is_var2:  # sub1 is none and sub2 is Variable
            return var_var(var1, sub2, sub_table, first_variable)
        if is_pred2:  # sub1 is none and sub2 is Predicate
            return var_pred(var1, sub2, sub_table)

    return True
