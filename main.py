"""
this project is intended to be used only with single characters as either {Variable,Predicate,Constant}
and it does not work with multi character strings that represents a single Constant example constant = "Ali"
it will consider "Ali" as A:constant , l : Variable ,i:Variable .
also it must be valid brackets when providing functions and predicates like s(),s() not s( or s)
"""

from libx import create_predicate, unify


def test(p1, p2):
    px1 = create_predicate(p1)
    px2 = create_predicate(p2)
    print(unify(px1, px2))


# --------------------success cases--------------------------
test("s()", "s()")
test("a(vmf(mt(s)B))", "a(msf(Bmt))")
test("a(Bcdf(m))", "a(mRWX)")

test("a(Bc(m))", "a(Bc(X))")
test("z(vmnxt)", "z(mnxtJ)")
test("z(vmnxt)", "z(mnxtv)")
test("z(vmnxt)", "z(mnxtf(XU))")
test("z(vmnxt)", "z(mnxts())")
test("z(K)", "z(f(XU))")
test("z(vmnx)", "z(mnxt)")
test("z(vmnx)", "z(mvxT)")
# test("z", "z")
# test("f(t(x)j(x))", "f(j(x)K)")
# --------------------failure cases---------------------------


test("b(CdE(f))", "b(gCh(i))")
test("m(XY)", "m(ghW)")
test("f(A(b(c)))", "f(B(d(E)))")
test("r(aB(XYZ))", "r(bc(DPQ))")
test("n(", "n)")
