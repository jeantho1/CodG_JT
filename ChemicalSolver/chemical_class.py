import re
import random


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

    def is_equilibrate(self):
        result = False  # Variable que retourne la fonction
        number_of_checked_atoms = 0
        dictionnary_left_side_values = {}  # On donne en clé l'atome et en value la qty
        dictionnary_right_side_values = {}  # On donne en clé l'atome et en value la qty

        #  2 boucles pour le coté gauche
        for m_l in self.left_eq.list_mol:
            # print(m_l)  # Affiche la molécule
            # print(m_l.qty)  # Coef stoechio de la molécule

            for at in m_l.atoms:
                # print(at.symbol)  # Affiche l'atome
                # print(at.qty)  # Nombres d'atomes dans la molécule
                dictionnary_left_side_values[at.symbol] = \
                    m_l.qty * at.qty + dictionnary_left_side_values.setdefault(at.symbol, 0)
        # print(dictionnary_left_side_values)

        #  2 boucles pour le coté droit
        for m_r in self.right_eq.list_mol:
            # print(m_r)  # Affiche la molécule
            # print(m_r.qty)  # Coef stoechio de la molécule

            for at_r in m_r.atoms:
                # print(at_r.symbol)  # Affiche l'atome
                # print(at_r.qty)  # Nombres d'atomes dans la molécule
                dictionnary_right_side_values[at_r.symbol] = \
                    m_r.qty * at_r.qty + dictionnary_right_side_values.setdefault(at_r.symbol, 0)
        # print(dictionnary_right_side_values)

        if dictionnary_right_side_values == dictionnary_left_side_values:
            print("T'es un bon prof Man !! <3 ")
            result = True

        return result

    def solve(self):
        # TODO JeanTho quand tu auras fait simplify tu pourras utiliser self.generate_factors
        for i, f in enumerate(self.generate_factors_best_try()):
            self.apply_factors(f)
            # print(str(self))
            if self.is_equilibrate():
                break
        print("{} solutions have been tried".format(i + 1))
        return str(self)

    def generate_factors_best_try(self):
        nb_mol = len(self.left_eq.list_mol) + len(self.right_eq.list_mol)
        # nombres premiers
        steps = [2, 3, 5, 7, 11, 13, 17]    # , 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        f = (1,) * nb_mol
        yield f

        random.seed()
        for step in steps:
            print("--- step {} ---".format(step))
            nb_possible_solutions = step ** nb_mol
            tried = set()
            for _ in range(nb_possible_solutions-1):
                while f in tried:
                    # print(len(f), len(tried), nb_possible_solutions, step, nb_mol)
                    f = tuple(random.randint(1, step) for i in range(nb_mol))
                tried.add(f)
                yield f
        yield (0,) * nb_mol

    def generate_factors(self):
        nb_mol = len(self.left_eq.list_mol) + len(self.right_eq.list_mol)
        steps = [5, 10]
        f = [1] * nb_mol
        yield f

        random.seed()
        for step in steps:
            print("--- step {} ---".format(step))
            nb_possible_solutions = step ** nb_mol
            for _ in range(nb_possible_solutions):
                # after exploring the maximum number of solutions (not necessarily ALL the possible solutions!)
                # we try a wider range
                for i in range(nb_mol):
                    f[i] = random.randint(0, step)
                yield f

    def apply_factors(self, f):
        if f == (2,1,1,2):
            print("ahah")
        all_mols = self.left_eq.list_mol[:]
        all_mols.extend(self.right_eq.list_mol)
        assert len(f) == len(all_mols)
        for i, m in enumerate(all_mols):
            m.qty = f[i]

    def __str__(self):
        return "{} -> {}".format(str(self.left_eq), str(self.right_eq))


class EquationSide(object):
    def __init__(self, half_seq_str):
        self.half_seq = half_seq_str
        self.list_mol = []      # list of molecules contained in the half equation

    def parse(self):
        list_mol = self.half_seq.split("+")
        for i in range(len(list_mol)):
            self.list_mol.append(Molecule(list_mol[i]))
            self.list_mol[i].parse()

    def __str__(self):
        list_mol_str = [str(m) for m in self.list_mol]
        return " + ".join(list_mol_str)


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
        self.qty = int(match.group('qty')) if match.group('qty') else 1
        self.mol = match.group('mol')

        # extract atoms
        atoms_str = re.findall("(?P<atoms>[A-Z][a-z]*[0-9]*)", self.mol)
        self.atoms = [Atom(a) for a in atoms_str]
        for a in self.atoms:
            a.parse()

    def __str__(self):
        list_atom_str = [str(a) for a in self.atoms]
        qty_str = str(self.qty) if self.qty > 1 else ""
        return qty_str + "".join(list_atom_str)


class Atom(object):
    def __init__(self, atom_str):
        self.atom_str = atom_str
        self.qty = None         # number of atoms
        self.symbol = None      # string representing the atom letter

    def parse(self):
        match = re.fullmatch('(?P<symbol>[A-Za-z]+)(?P<qty>[0-9]*)', self.atom_str)
        self.qty = int(match.group('qty')) if match.group('qty') else 1
        self.symbol = match.group('symbol')

    def __str__(self):
        qty_str = str(self.qty) if self.qty > 1 else ""
        return "{}{}".format(self.symbol, qty_str)
