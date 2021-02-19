from mdsd.item_support import const_visitor
from mdsd.item_support import accept


@const_visitor
class print_visitor:
    def __init__(self, f, indent):
        self.f = f
        self.indent = indent

    def visit_scalar(self, struct, attr, meta):
        self.f.write(" " * self.indent + f"{attr}={getattr(struct, attr)}\n")

    def visit_scalar_struct(self, struct, attr, meta):
        printto(getattr(struct, attr), self.f, self.indent + 2)

    def visit_array(self, struct, attr, meta):
        self.f.write(" " * self.indent + f"{attr}={str(getattr(struct, attr))}\n")

    def visit_string(self, struct, attr, rawattr, meta):
        val = getattr(struct, attr).replace(r'"', r"\"")
        self.f.write(" " * self.indent + f'{attr}="{val}"\n')

    def visit_array_struct(self, struct, attr, meta):
        v = print_visitor(self.f, self.indent + 2)
        for s in getattr(struct, attr):
            printto(s, self.f, self.indent + 2)


def printto(s, f, indent=0):
    v = print_visitor(f, indent + 2)
    f.write(" " * indent + f"{s.__class__.__name__}\n")
    accept(s, v)
