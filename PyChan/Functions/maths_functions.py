def dec_to_another(to_param, number: int):
    digits = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
              13: 'D', 14: 'E', 15: 'F'}
    number_copy = number
    converted_number = ''
    print(f'{number} / {to_param}')
    while number_copy > 0:
        rest = number_copy % to_param
        converted_number = digits[rest] + converted_number
        number_copy = number_copy // to_param
        print(f'{number_copy} r {rest}')
    return converted_number


def float_to_bin(num, length):
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


def ieee754_32(liczba):
    sign = '0'
    if liczba[0] == '-':
        liczba = liczba[1:]
        sign = '1'
    number = liczba.split('.')
    bin_number = [dec_to_another(2, int(number[0]))]
    bin_number.append(float_to_bin('0.' + number[1], 27))
    exponent = dec_to_another(2, 127 + len(bin_number[0]) - 1)
    return (sign + exponent + bin_number[0][1:] + bin_number[1])[:32]


def dec_float_to_another(to_param, number: float):
    digits = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
              13: 'D', 14: 'E', 15: 'F'}

    integer = int(number)
    fraction = number - int(number)

    numbers_dict = {'integer': [], 'fraction': [], 'converted': {}}

    if integer != 0:
        converted_integer = ''
        while integer > 0:
            rest = integer % to_param
            converted_integer = digits[rest] + converted_integer
            integer = integer // to_param
            numbers_dict['integer'].append({integer: rest})
        numbers_dict['converted']['integer'] = converted_integer
    else:
        numbers_dict['converted']['integer'] = 0

    if fraction != 0:
        converted_fraction = ''
        counter = 0
        while fraction != 0 or (fraction != 0 and counter < 16):
            fraction = fraction * 2
            integ = int(fraction)
            converted_fraction = converted_fraction + str(integ)
            numbers_dict['fraction'].append({fraction: integ})
            fraction = fraction - integ
            counter = counter + 1
        numbers_dict['converted']['fraction'] = converted_fraction

    numbers_dict['converted']['number'] = numbers_dict['converted']['integer'] + '.' + numbers_dict['converted']['fraction']

    return numbers_dict
