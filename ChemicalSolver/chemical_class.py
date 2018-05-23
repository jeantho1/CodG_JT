import re


class Equation(object):
    def __init__(self, seq_str):
        # check input
        assert re.fullmatch('[A-Za-z0-9+ ]+->[A-Za-z0-9+ ]+', seq_str), "Invalid equation: {}".format(seq_str)

        self.seq = seq_str
        self.left_eq = None     # object EquationSide representing the left part
        self.right_eq = None    # object EquationSide representing the right part

    def parse_seq(self):
        parse = self.seq.replace(" ", "").split("->", 1)
        left_eq_str = parse[0]
        right_eq_str = parse[1]
        self.left_eq = EquationSide(left_eq_str)
        self.right_eq = EquationSide(right_eq_str)

        self.left_eq.parse()
        self.right_eq.parse()

    def solve(self):
        pass
        return None

    def is_equilibrate(self):
        pass
        return False


class EquationSide(object):
    def __init__(self, half_seq_str):
        self.half_seq = half_seq_str
        self.list_mol = []      # list of molecules contained in the half equation

    def parse(self):
        list_mol = self.half_seq.split("+")
        for i in range(len(list_mol)):
            self.list_mol.append(Molecule(list_mol[i]))
            self.list_mol[i].parse()


class Molecule(object):
    def __init__(self, molecule_str):
        self.mol_str = molecule_str
        self.qty = None         # stoechiometric number
        self.mol = None         # string representing the molecule
        self.atoms = None       # list of atoms in the molecule

    def parse(self):
        # extract quantity
        match = re.fullmatch('(?P<qty>[0-9]*)(?P<mol>[A-Za-z0-9]+)', self.mol_str)
        assert match, "Invalid molecule: {}".format(self.mol_str)
        self.qty = int(match.group('qty'))
        self.mol = match.group('mol')

        # extract atoms
        atoms_str = re.findall("(?P<atoms>[A-Za-z]+[0-9]*)", self.mol)
        self.atoms = [Atom(a) for a in atoms_str]
        for a in self.atoms:
            a.parse()


class Atom(object):
    def __init__(self, atom_str):
        self.atom_str = atom_str
        self.qty = None         # number of atoms
        self.symbol = None      # string representing the atom letter

    def parse(self):
        match = re.fullmatch('(?P<symbol>[A-Za-z]+)(?P<qty>[0-9]*)', self.atom_str)
        self.qty = int(match.group('qty'))
        self.symbol = match.group('symbol')
