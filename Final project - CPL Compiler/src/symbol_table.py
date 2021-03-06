from collections import namedtuple

from lark.visitors import Visitor

from exceptions import CPLException, CPLCompoundException

__author__ = "Nir Moshe"


Symbol = namedtuple("Symbol", field_names=["name", "type", "line"])


class SymbolAlreadyExistsError(CPLException):
    def __init__(self, first_symbol, redefinition_symbol_name, line):
        CPLException.__init__(
            self,
            line,
            "Symbol %s already defined in line %d!" % (redefinition_symbol_name, first_symbol.line)
        )


class Types:
    INT = "Integer"
    FLOAT = "Floating point"


class SymbolTable(object):
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, type, line):
        if name in self.symbols:
            raise SymbolAlreadyExistsError(self.symbols[name], name, line)

        self.symbols[name] = Symbol(name, type, line)

    def get_symbol(self, name):
        """returns `Symbol` or None if the symbol doesn't exists."""
        return self.symbols.get(name)

    @classmethod
    def build_form_ast(cls, cpl_ast):
        symbol_table = cls()
        builder = SymbolTableBuilder(symbol_table)
        builder.visit(cpl_ast)
        return builder.errors, symbol_table


class SymbolTableBuilder(Visitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self._init_declarations()
        self.errors = []

    def _init_declarations(self):
        self._current_declaration_ids = []
        self._current_declaration_type = None

    def declaration(self, _):
        for token in self._current_declaration_ids:
            try:
                self.symbol_table.add_symbol(
                    name=token.value,
                    type=self._current_declaration_type,
                    line=token.line
                )
            except SymbolAlreadyExistsError as exception:
                self.errors.append(exception)

        self._init_declarations()

    def idlist(self, tree):
        # Collect all the variables definitions.
        for token in tree.children:
            if is_lark_token(token) and token.type == "ID":
                self._current_declaration_ids.append(token)

    def type(self, tree):
        # Extract the variables type (from the declarations statement).
        type_token = tree.children[0]
        if type_token.type == "INT":
            self._current_declaration_type = Types.INT

        else:  # It has to be a float.. otherwise lark would have raise an exception.
            self._current_declaration_type = Types.FLOAT


def is_lark_token(obj):
    try:
        _, _ = obj.type, obj.value
        return True

    except AttributeError:
        return False
