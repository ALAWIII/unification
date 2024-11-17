from elements_type import *
from utils import *


def get_sub_table(p1: Predicate, p2: Predicate) -> [dict, bool]:
    sub_table = {}

    def _get_sub_table(p1: Predicate, p2: Predicate) -> bool:
        if p1 != p2 or p1.length() != p2.length():
            return False
        n = p1.length()
        for i in range(n):
            ele1 = p1.get_arg(i)  # only one of them : {Constant,Variable , Predicate}
            ele2 = p2.get_arg(i)
            is_con1 = isinstance(ele1, Constant)
            is_con2 = isinstance(ele2, Constant)
            is_var1 = isinstance(ele1, Variable)
            is_var2 = isinstance(ele2, Variable)
            is_pred1 = isinstance(ele1, Predicate)
            is_pred2 = isinstance(ele2, Predicate)
            if is_con1:
                if is_con2:
                    if not con_con(ele1, ele2):
                        return False
                elif is_var2:
                    if not con_var(ele1, ele2, sub_table):
                        return False
                else:  # is_pred2
                    if not con_pred(ele1, ele2, sub_table):
                        return False
            elif is_pred1:
                if is_con2:
                    if not con_pred(ele2, ele1, sub_table):
                        return False
                elif is_var2:
                    if not var_pred(ele2, ele1, sub_table):
                        return False
                else:  # is_pred2
                    if not pred_pred(ele1, ele2, sub_table):
                        return False
                    if not _get_sub_table(ele1, ele2):
                        return False
            else:  # is_var1

                if is_con2:
                    if not con_var(ele2, ele1, sub_table):
                        return False
                elif is_pred2:

                    if not var_pred(ele1, ele2, sub_table):
                        return False
                else:  # both are variables
                    if not var_var(ele1, ele2, sub_table, ele1):
                        return False
        return True

    result = _get_sub_table(p1, p2)  # either true or false

    return sub_table, result


def unify_element(element: [Variable, Predicate], sub_table: dict, i=0):
    if i == len(sub_table):
        return element
    sub = sub_table.get(element)  # only one of them : {Constant,Variable,Predicate}
    if sub is None:
        return element
    if isinstance(sub, Variable):
        value = unify_element(sub, sub_table, i + 1)
        sub_table[element] = value
        return value
    if isinstance(sub, Predicate):
        sub_pred = sub_table.get(sub)  # either is None or constant
        if sub_pred is not None:
            return sub_pred
    return sub  # if it was already a constant


def unify(p1: Predicate, p2: Predicate):
    sub_table, result = get_sub_table(p1, p2)

    if len(sub_table) >= 0 and not result:
        return False

    def _unify(p: Predicate):
        for index, element in enumerate(p):
            if isinstance(element, Variable):
                unify_element(element, sub_table, 0)
                p.set_arg_at(index, sub_table[element])
            elif isinstance(element, Predicate):
                if element in sub_table:
                    unify_element(element, sub_table, 0)
                    p.set_arg_at(index, sub_table[element])
                _unify(element)

    _unify(p1)
    # print(sub_table)
    return p1
