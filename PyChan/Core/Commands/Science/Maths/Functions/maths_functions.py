def dec_to_another(to_param, number: int):
    """
    Convert number to decimal number systems

    :param to_param: Target number system

    :param number: Number to change
    :type number: int

    :return: Returns a number converted to the decimal system
    :rtype: int
    """
    digits = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
              13: 'D', 14: 'E', 15: 'F'}
    number_copy = number
    converted_number = ''
    while number_copy > 0:
        rest = number_copy % to_param
        converted_number = digits[rest] + converted_number
        number_copy = number_copy // to_param
    return converted_number


def float_to_bin(num, length):
    """
    Convert float number to binary systems

    :param num: Number to change
    :type num: float

    :param length: The maximum length of the number in binary system
    :type length: int

    :return: Returns a number converted to the binary system
    :rtype: string
    """
    temp_2 = ''
    temp = float(num)
    for x in range(length):
        temp = temp * 2
        if temp < 1:
            temp_2 += "0"
        else:
            temp_2 += "1"
            temp -= 1
    return temp_2


def dec_float_to_another(to_param, number: float):
    """
    Convert float number to another number system

    :param to_param: Target number system
    :type to_param: int

    :param number: Number to change
    :type number: int

    :return: Solution step by step in json format
    :rtype: dict

    """
    digits = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
              13: 'D', 14: 'E', 15: 'F'}

    integer = int(number)
    fraction = number - integer
    numbers_dict = {'integer': [], 'fraction': [], 'converted': {}}

    if integer != 0:
        converted_integer = ''
        while integer > 0:
            rest = integer % to_param
            converted_integer = digits[rest] + converted_integer
            integer = integer // to_param
            numbers_dict['integer'].append({integer: digits[rest]})
        numbers_dict['converted']['integer'] = converted_integer
    else:
        numbers_dict['converted']['integer'] = 0
    if fraction != 0:
        converted_fraction = ''
        counter = 0
        while fraction != 0 and counter < 16:
            fraction = fraction * to_param
            integ = int(fraction)
            converted_fraction = converted_fraction + digits[integ]
            numbers_dict['fraction'].append({fraction: digits[integ]})
            fraction = fraction - integ
            counter = counter + 1
        numbers_dict['converted']['fraction'] = converted_fraction
    else:
        numbers_dict['converted']['fraction'] = '0'

    numbers_dict['converted']['number'] = f"{numbers_dict['converted']['integer']}.{numbers_dict['converted']['fraction']}"

    return numbers_dict


def another_float_to_dec(from_param, number):
    """
    Convert float number to decimal number system

    :param from_param: Base number system
    :type from_param: int

    :param number: Number to change

    :return: Solution step by step in json format
    :rtype: dict
    """
    digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
              'D': 13, 'E': 14, 'F': 15}

    dec = 0
    numbers_dict = {'integer': {}, 'fraction': {}, 'dec': 0}

    integer = ''
    fraction = ''

    if '.' in number:
        integer = number.split('.')[0]
        fraction = number.split('.')[1]
    else:
        integer = number

    for i, char in enumerate(reversed(integer)):
        dec = dec + (from_param ** i * digits[char])
        numbers_dict['integer'][i] = digits[char]

    for i, char in enumerate(fraction, start=1):
        dec = dec + (from_param ** (-i) * digits[char])
        numbers_dict['fraction'][-i] = digits[char]

    numbers_dict['dec'] = dec

    return numbers_dict


def ieee754_32(liczba):
    """
   Convert float number to ieee754 32 bit system

   :param liczba: Base number system
   :type liczba: float

   :return: List with sign, exponent and mantissa
   :rtype: list
   """
    sign = '0'
    if liczba[0] == '-':
        liczba = liczba[1:]
        sign = '1'
    number = liczba.split('.')
    bin_number = [dec_to_another(2, int(number[0]))]
    bin_number.append(float_to_bin('0.'+number[1], 27))
    exponent = dec_to_another(2, 127 + len(bin_number[0]) - 1)
    return [sign, exponent, (bin_number[0][1:] + bin_number[1])[:23], (sign+exponent+bin_number[0][1:] + bin_number[1])[:32]]


def ieee754_64(liczba):
    """
   Convert float number to ieee754 64 bit system

   :param liczba: Base number system
   :type liczba: float

   :return: List with sign, exponent and mantissa
   :rtype: list
   """
    sign = '0'
    if liczba[0] == '-':
        liczba = liczba[1:]
        sign = '1'
    number = liczba.split('.')
    bin_number = [dec_to_another(2, int(number[0]))]
    bin_number.append(float_to_bin('0.'+number[1], 53))
    exponent = dec_to_another(2, 1023 + len(bin_number[0]) - 1)
    return [sign, exponent, (bin_number[0][1:] + bin_number[1])[:51], (sign+exponent+bin_number[0][1:] + bin_number[1])[:64]]


def twos_complement(dec):
    """
    Convert decimal integer number to U2

    :param dec: Number to change
    :type dec: int

    :return: Number in U2
    :rtype: string
    """
    if dec >= 0:
        binint = "{0:b}".format(dec)
        if binint[0] == "1": binint = "0" + binint
    else:
        dec2 = abs(dec + 1)
        binint_r = "{0:b}".format(dec2)

        binint = "1"
        for bit in binint_r:
            if bit == "1":
                binint += "0"
            else:
                binint += "1"

    return binint


def bin_extend_in_U2(binint, amount):
    """
    Extends number in U2

    :param binint: Number to extend in U2
    :type binint: string

    :param amount: number of characters to be added
    :type amount: int

    :return: Number in U2
    :rtype: string
    """
    for _ in range(amount):
        binint = binint[0] + binint

    return binint


def twos_complement_equal_length(dec1, dec2):
    """
    Convert two decimal integer numbers to U2, that both are the same length

    :param dec1: First number to change to U2
    :type dec1: int

    :param dec2: Second number to change to U2
    :type dec2: int

    :return: Numbers in U2 in list: [First number, The number opposite to the first number, Second number]
    :rtype: list
    """
    # conversion
    bin1 = twos_complement(dec1)
    bin1n = twos_complement(-dec1)
    bin2 = twos_complement(dec2)

    len1 = len(bin1)
    len1n = len(bin1n)
    len2 = len(bin2)

    # extending until same length
    while len1 != len2 or len1n != len2:
        minimal = min(len1, len1n, len2)
        maximal = max(len1, len1n, len2)
        if minimal == maximal:
            return
        if len1 == minimal:
            bin1 = bin_extend_in_U2(bin1, maximal - minimal)
        if len1n == minimal:
            bin1n = bin_extend_in_U2(bin1n, maximal - minimal)
        if len2 == minimal:
            bin2 = bin_extend_in_U2(bin2, maximal - minimal)

        len1 = len(bin1)
        len1n = len(bin1n)
        len2 = len(bin2)

    return [bin1, bin1n, bin2]


def bin_add_U2(bin1, bin2):
    """
    Adds two binary numbers in U2

    :param bin1: First number in U2
    :type bin1: string

    :param bin2: Second number in U2
    :type bin2: string

    :return: Result of adding in U2
    :rtype: string
    """
    result = ""
    moving = 0
    for i in range(len(bin1) - 1, -1, -1):
        if moving:
            if bin1[i] == "0" and bin2[i] == "0":
                result = "1" + result
                moving = 0
            elif bin1[i] == "0" and bin2[i] == "1":
                result = "0" + result
            elif bin1[i] == "1" and bin2[i] == "0":
                result = "0" + result
            elif bin1[i] == "1" and bin2[i] == "1":
                result = "1" + result
        elif not moving:
            if bin1[i] == "0" and bin2[i] == "0":
                result = "0" + result
            elif bin1[i] == "0" and bin2[i] == "1":
                result = "1" + result
            elif bin1[i] == "1" and bin2[i] == "0":
                result = "1" + result
            elif bin1[i] == "1" and bin2[i] == "1":
                result = "0" + result
                moving = 1
    return result


def booth(dec1, dec2):
    """
    Generates step by step solution of multiplication of two integers with the booth algorithm

    :param dec1: First number
    :type dec1: int
    :param dec2: Second number
    :type dec2: int

    :return: List of steps and solution: [[steps], solution]
    :rtype: list
    """
    steps = [["Krok", "A", "Q", "Q-1", "Operacja"]]
    conversion = twos_complement_equal_length(dec1, dec2)
    P = conversion[0]
    P_n = conversion[1]
    Q = conversion[2]
    A = "0" * len(Q)
    q = "0"
    step = 0
    shr_count = 0
    while True:
        if shr_count == len(Q):
            steps.append(["", A, Q, q, "STOP"])
            return [steps, A + Q]

        if (Q[-1] == "0" and q == "0") or (Q[-1] == "1" and q == "1"):
            steps.append([str(step), A, Q, q, "SHR"])
            q = Q[-1]
            Q = A[-1] + Q[0:-1]
            A = A[0] + A[0:-1]
            shr_count += 1
        elif Q[-1] == "0" and q == "1":
            steps.append([str(step), A, Q, q, "+P"])
            steps.append(["", P, "", "", "ADD"])
            A = bin_add_U2(A, P)
            steps.append(["", A, Q, q, "SHR"])
            q = Q[-1]
            Q = A[-1] + Q[0:-1]
            A = A[0] + A[0:-1]
            shr_count += 1
        elif Q[-1] == "1" and q == "0":
            steps.append([str(step), A, Q, q, "-P"])
            steps.append(["", P_n, "", "", "ADD"])
            A = bin_add_U2(A, P_n)
            steps.append(["", A, Q, q, "SHR"])
            q = Q[-1]
            Q = A[-1] + Q[0:-1]
            A = A[0] + A[0:-1]
            shr_count += 1

        step += 1
