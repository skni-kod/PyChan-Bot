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