from math import gcd, factorial
from functools import reduce
from random import choice
from re import match


def lcm(a, b):
    """
    Least common multiple of two numbers

    :param a: First number
    :type a: int
    :param b: Second number
    :type b: int

    :return: Returns least common multiple of two numbers
    :rtype: int
    """
    return a * b // gcd(a, b)


def lcm_n(args):
    """
    Least common multiple of many numbers

    :param args: List of numbers
    :type args: list

    :return: Returns least common multiple of numbers in list
    :rtype: int
    """
    return reduce(lcm, args)


def string2perm(string):
    """
    Convert string from user input to permutation in one-line notation as list

    :param string: Permutation as string
    :type string: string

    :return: Returns permutation in one-line notation as list
    :rtype: list
    """
    string = string.replace('<', '').replace('>', '')
    perm = string.split(' ')
    perm = [int(x) for x in perm if x != ""]

    # check if correct format:
    return -1 if len(perm) != len(set(perm)) or len(perm) != max(perm) else perm


def perm2string(perm):
    """
    Convert permutation in one-line notation as list to string

    :param perm: Permutation as list
    :type perm: list

    :return: Returns permutation in one-line notation as string
    :rtype: string
    """
    string = "<"
    for x in range(len(perm)):
        string += str(perm[x])
        if x != len(perm) - 1: string += " "
    string += ">"

    return string


def string2cycles(string):
    """
    Convert string from user input to permutation in cycle notation as list

    :param string: Permutation as string
    :type string: string

    :return: Returns permutation in cycle notation as list
    :rtype: list
    """
    groups = string.split(')(')

    items = []
    for i in range(0, len(groups)):
        groups[i] = groups[i].replace('(', '').replace(')', '').lstrip().rstrip().split(' ')
        temp = []
        for j in groups[i]:
            temp.append(int(j))
        items.append(temp)

    return items


def cycles2string(cycles):
    """
    Convert permutation in cycle notation as list to string

    :param cycles: Permutation in cycle notation as list
    :type cycles: list

    :return: Returns permutation as string
    :rtype: string
    """
    string = ""
    for cycle in cycles:
        string += "("
        for i in range(len(cycle)):
            string += str(cycle[i])
            if i != len(cycle) - 1: string += " "
        string += ")"

    return string


def perm2cycles(items):
    """
    Convert permutation in one-line notation to permutation in cycle notation

    :param items: Permutation in one-line notation
    :type items: list

    :return: Returns permutation in cycle notation
    :rtype: list
    """
    cycles = []
    used = []

    for x in range(1, max(items) + 1):
        if x in used: continue

        temp = []
        temp.append(x)
        used.append(x)

        i = x

        while True:
            i = items[i - 1]
            if i == x: break
            temp.append(i)
            used.append(i)

        cycles.append(temp)

    return cycles


def cycles2perm(cycles):
    """
    Convert permutation in cycle notation to permutation in one-line notation

    :param cycles: Permutation in cycle notation
    :type cycles: list

    :return: Returns permutation in one-line notation
    :rtype: list
    """
    n = max([item for sublist in cycles for item in sublist])

    perm = [x for x in range(1, n + 1)]
    for i in range(n):
        for j in reversed(cycles):
            try:
                x = j.index(perm[i])
            except ValueError:
                continue
            else:
                if x == len(j) - 1:
                    perm[i] = j[0]
                else:
                    perm[i] = j[x + 1]

    return perm


def perm2cycles_without_fixed(perm):
    """
    Convert permutation in one-line notation to permutation in cycle notation without fixed points

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns permutation in cycle notation without fixed points
    :rtype: list
    """
    cycles = []
    used = []

    for x in range(1, max(perm) + 1):
        if x in used: continue

        temp = []
        temp.append(x)
        used.append(x)

        i = x

        while True:
            i = perm[i - 1]
            if i == x: break
            temp.append(i)
            used.append(i)

        if len(temp) > 1: cycles.append(temp)

    return cycles


def smart_input(string):
    """
    Convert string from user input to permutation in one-line notation as list.
    Function will accept both: one-line and cycle notation. There is also a way to multiply permutations by '#' sign

    :param string: Permutation as string
    :type string: string

    :return: Returns permutation in one-line notation as list
    :rtype: list
    """
    strings = string.split('#')
    cycles = []
    for string in strings:
        string = string.rstrip().lstrip()
        if len(string) == 0:
            return -1
        if match('^<(\s)*(([1-9]|1[0-5])?\s)*([1-9]|1[0-5])?(\s)*>$', string):
            perm = string2perm(string)
            if perm == -1: return -1
            cycle = perm2cycles(perm)
            cycles += cycle
        elif match('^(\((\s)*(([1-9]|1[0-5])?\s)*([1-9]|1[0-5])?(\s)*\)(\s)*)+$', string):
            cycle = string2cycles(string)
            cycles += cycle
        else:
            return -1

    return cycles2perm(cycles)


def random_perm(n):
    """
    Randomize permuatation in specified Sn

    :param n: Max number in permutation
    :type n: int

    :return: Returns permutation in one-line notation as list
    :rtype: list
    """
    perm = []
    random_from = [i for i in range(1, n + 1)]
    while len(random_from) > 0:
        i = choice(random_from)
        random_from.remove(i)
        perm.append(i)

    return perm


def all_inversions(perm):
    """
    Generate all inversions of permutation

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns list with all inversions
    :rtype: list
    """
    inversions = []
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions.append([perm[i], perm[j]])

    return inversions


def all_inversions_count(perm):
    """
    Counts all inversions of permutation

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns number of all inversions
    :rtype: number
    """
    return len(all_inversions(perm))


def inversion_vector(perm):
    """
    Generate inversion vector of permutation

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns inversion vector of permutation
    :rtype: list
    """
    invers = all_inversions(perm)
    vector = [0] * len(perm)

    for i in range(len(perm)):
        for j in invers:
            if j[0] == perm[i]:
                vector[i] += 1
    return vector


def perm_cpd(perm):
    """
    Counts cycles of even length

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns number of cycles of even length
    :rtype: list
    """
    cycles = perm2cycles(perm)
    cpd = 0
    for x in cycles:
        if len(x) % 2 == 0:
            cpd += 1
    return cpd


def perm_cpnd(perm):
    """
    Counts cycles of odd length

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns number of cycles of odd length
    :rtype: list
    """
    cycles = perm2cycles(perm)
    cpnd = 0
    for x in cycles:
        if len(x) % 2 != 0:
            cpnd += 1
    return cpnd


def perm_type(perm):
    """
    Type of permutation

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns type of permutation
    :rtype: list
    """
    perm_type = []
    cycles = perm2cycles(perm)
    for i in range(1, len(perm) + 1):
        counter = 0
        for j in cycles:
            if len(j) == i: counter += 1
        if counter != 0:
            perm_type.append([f"{i}^{counter}"])

    return perm_type


def perm_order(perm):
    """
    Order of permutation

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns order of permutation
    :rtype: int
    """
    cycles = perm2cycles(perm)
    return lcm_n([len(x) for x in cycles])


def perm_inverse(perm):
    """
    Inverse permutation (raised to the power of -1)

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns inverse permutation
    :rtype: list
    """
    inversed = []
    for i in range(1, len(perm) + 1):
        inversed.append(perm.index(i) + 1)

    return inversed


def move(cycle):
    """
    Push last element of cycle to first position

    :param cycle: One cycle of permutation in cycles notation
    :type cycle: list

    :return: Returns moved cycle
    :rtype: list
    """
    cycle.insert(0, cycle[-1])
    cycle.pop(-1)
    return (cycle)


def canonical_cycle_notation(perm):
    """
    Convert permutation in one-line notation to permutation in canonical cycle notation

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns permutation in canonical cycle notation
    :rtype: list
    """
    cycles = perm2cycles(perm)
    ccn = []
    for x in cycles:
        while x[0] != max(x):
            x = move(x)
        ccn.append(x)
    ccn.sort()
    return ccn


def perm_sign(perm):
    """
    Sign of permutation

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns sign of permutation
    :rtype: int
    """
    return (-1) ** all_inversions_count(perm)


def perm_number(perm):
    """
    Number of permutation in list in lexicographic order

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns number of permutation
    :rtype: int
    """
    vector = inversion_vector(perm)
    vector.reverse()
    number = 0
    i = 0

    for x in vector:
        number += x * factorial(i)
        i += 1

    return number


def next_in_lex(perm):
    """
    Generate permutation with one number higher in list in lexicographic order

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns next permutation in list in lexicographic order
    :rtype: list
    """
    sorted = perm.copy()
    sorted.sort()
    sorted.reverse()
    if sorted == perm: return -1

    # szukanie pary rosnącej od prawej
    perm_r = perm.copy()
    perm_r.reverse()
    for x in range(len(perm) - 1):
        if perm_r[x] > perm_r[x + 1]: break
    # jesli znaleziony na koncu to zmiana dwoch elementow
    if x == 0:
        result = perm[0:-2]
        result.append(perm[-1])
        result.append(perm[-2])
        return result

    # szukanie liczby większej po prawej stronie
    temp = []
    for i in range(x + 1):
        temp.append([perm_r[i], i])
    temp.sort()

    for i in temp:
        if i[0] > perm_r[x + 1]: break
    perm_r[i[1]] = perm_r[x + 1]
    perm_r[x + 1] = i[0]

    # odwrocenie koncowki
    result = perm_r[x + 1:]
    result.reverse()
    result.extend(perm_r[:x + 1])
    return result


def perm_list(n, filename):
    """
    Generate full list of permutation in lexicographic order in Sn and save it to file

    :param n: max number in permutation in one-line notation
    :type n: int
    :param filename: path to file, where the result will be saved
    :type filename: string

    :return: Returns next permutation in list in lexicographic order
    :rtype: list
    """
    perm = [x for x in range(1, n + 1)]
    with open(filename, "wt", encoding="UTF-8") as file:
        file.write(f"Wszystkie permutacje w porządku leksykograficznym należące do S{n}\n")
        for i in range(factorial(n)):
            file.write(f"[{i}]\t\t{perm2string(perm)}\n")
            perm = next_in_lex(perm)
            if perm == -1: break


def perm_from_number(number, n):
    """
    Generate permutation with given number

    :param number: Number of permutation in list in lexicographic order
    :type number: int
    :param n: max number in permutation in one-line notation
    :type n: int

    :return: Returns permutation with given number
    :rtype: list
    """
    perm = [0] * n
    vector = [0] * n
    for i in range(n):
        vector[i] = number // factorial(n - i - 1)
        number = number % factorial(n - i - 1)
    numbers = [i for i in range(1, n + 1)]
    for i in range(n):
        perm[i] = numbers[vector[i]]
        numbers.pop(vector[i])

    return perm


def is_derangement(perm):
    """
    Check if permutation is derangement

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns True if permutation is derangement
    :rtype: bool
    """
    cycles = perm2cycles(perm)
    return not any([True for x in cycles if len(x) == 1])


def is_involution(perm):
    """
    Check if permutation is involution

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns True if permutation is involution
    :rtype: bool
    """
    cycles = perm2cycles(perm)
    return not any([True for x in cycles if len(x) > 2])


def is_transposition(perm):
    """
    Check if permutation is transposition

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns True if permutation is transposition
    :rtype: bool
    """
    cycles = perm2cycles_without_fixed(perm)
    return False if len(cycles) == 0 else (len(cycles) == 1 and len(cycles[0]) == 2)


def is_onecyclic(perm):
    """
    Check if permutation is onecyclic

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns True if permutation is onecyclic
    :rtype: bool
    """
    cycles = perm2cycles(perm)
    return len(cycles) == 1


def is_even(perm):
    """
    Check if permutation is even

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns True if permutation is even
    :rtype: bool
    """
    cycles = perm2cycles_without_fixed(perm)
    return len(cycles) % 2 == 0


def is_odd(perm):
    """
    Check if permutation is odd

    :param perm: Permutation in one-line notation
    :type perm: list

    :return: Returns True if permutation is odd
    :rtype: bool
    """
    cycles = perm2cycles_without_fixed(perm)
    return len(cycles) % 2 != 0


def perm_power(perm, power):
    """
    Raises a permutation to a power

    :param perm: Permutation in one-line notation
    :type perm: list
    :param power: Power to which the permutation will be raised
    :type power: int

    :return: Returns permutation raised to power
    :rtype: list
    """
    cycles = perm2cycles(perm)
    order = perm_order(perm)
    power2 = abs(power)
    power2 = power2 % order
    if power2 == 0:
        perm = [i for i in range(1, len(perm) + 1)]
    elif power2 == 1:
        pass
    else:
        cycles *= power2
        perm = cycles2perm(cycles)

    if power < 0:
        perm = perm_inverse(perm)

    return perm
