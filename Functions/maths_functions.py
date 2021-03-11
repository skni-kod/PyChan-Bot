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
    bin_number.append(float_to_bin('0.'+number[1], 27))
    exponent = dec_to_another(2, 127 + len(bin_number[0]) - 1)
    return (sign+exponent+bin_number[0][1:] + bin_number[1])[:32]
