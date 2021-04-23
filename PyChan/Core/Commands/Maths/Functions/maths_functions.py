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
