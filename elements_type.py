from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass()
class Predicate:
    name: str
    args = []

    def set_args(self, args):
        self.args = args

    def get_args(self) -> List[Constant, Variable, Predicate]:
        return self.args

    def get_arg(self, index) -> [Constant, Variable, Predicate]:
        return self.args[index]

    def set_arg_at(self, index, arg):
        self.args[index] = arg

    def __str__(self):
        return f"{self.name}{self.args}"

    def length(self):
        return len(self.args)

    def __hash__(self):
        return hash(self.name + "p")

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.args)


@dataclass()
class Variable:
    var: str

    def get_var(self):
        return self.var

    def __hash__(self):
        return hash(self.var + "v")

    def __repr__(self):
        return self.var


@dataclass()
class Constant:
    const: str

    def get_const(self):
        return self.const

    def __hash__(self):
        return hash(self.const)

    def __repr__(self):
        return self.const
