import math

probability = [1 / 2, 1 / 8, 1 / 16, 1 / 16, 1 / 16, 1 / 16, 1 / 32, 1 / 32, 1 / 32, 1 / 32]
source = ['x' + str(i) for i in range(len(probability))]


def float_bin(number, places=3):
    print(number)
    whole, dec = str(number).split(".")
    whole = int(whole)
    dec = int(dec)
    res = bin(whole).lstrip("0b") + "."
    for x in range(places):
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole
    return res


def decimal_converter(num):
    while num > 0:
        num /= 10
    return num


def shannon():
    cumulative_probabilites = [float(sum(probability[: i - 1])) for i in range(1, len(probability) + 1)]
    print(cumulative_probabilites)
    shanon_lengths = [math.ceil(-math.log2(pi)) for pi in probability]
    print(shanon_lengths)
    binary_cum_prob = ['0.00000',
                       '0.100000', '0.10100000',
                       '0.101100000', '0.1100000',
                       '0.110100000', '0.11100000',
                       '0.1110100000', '0.111100000',
                       '0.11111']
    print(binary_cum_prob)
    codes = [binary_cum_prob[i][2:shanon_lengths[i] + 2]
             for i in range(len(binary_cum_prob))]
    print(codes)


def compute_useless_bits(m):
    for i in range(m):
        if 2 ** i >= m + i + 1:
            return i


def position_useless_bits(data, r, j=0, k=1, result=''):
    for i in range(1, len(data) + r + 1):
        if i == 2 ** j:
            result = result + '0'
            j += 1
        else:
            result = result + data[-1 * k]
            k += 1
    return result[::-1]


def compute_parity_bits(el_list, distance):
    for i in range(distance):
        val = 0
        for j in range(1, len(el_list) + 1):
            if j & (2 ** i) == (2 ** i):
                val = val ^ int(el_list[-1 * j])
        el_list = el_list[:len(el_list) - (2 ** i)] + str(val) + el_list[len(el_list) - (2 ** i) + 1:]
    return el_list


def find_error(el_list, nr, result=0):
    for i in range(nr):
        val = 0
        for j in range(1, len(el_list) + 1):
            if j & (2 ** i) == (2 ** i):
                val = val ^ int(el_list[-1 * j])
        result = result + val * (10 ** i)
    return int(str(result), 2)


shannon()

for i in range(15):
    print(i, end='&')

print()


def gray_n_bit(n):
    n = int(n)
    for i in range(0, 1 << n):
        gray = i ^ (i >> 1)
        print("{0:0{1}b}".format(gray, n))


gray_n_bit(4)


def shannon_fano(s):
    binary = ["" for _ in range(9)]
    s1 = s[0][0]
    s2 = s[1]
    while len(s2) >= 1:
        for i in range(9):
            if realisations[i] == s1:
                binary[i] += str(0)
            index = i
            break
        for x in range(len(binary)):
            if x > index:
                binary[x] += str(1)
    s1 = s2[0]
    s2 = s2[1:]
    print('\nCodes:')
    for i in range(len(binary)):
        print(realisations[i] + '=' + binary[i])


realisations = ["x" + str(i) for i in range(1, 11)]
array = [1 / 2, 1 / 8, 1 / 16, 1 / 16, 1 / 16, 1 / 16, 1 / 32, 1 / 32, 1 / 32, 1 / 32]


def sf():
    print(realisations)
    print(array)
    result = [0, 0, 'error']
    print('\nPossible situations: ')
    for i in range(len(array) - 1):
        if i == 0:
            result = [realisations[:i + 1], realisations[i + 1:],
                      sum(array[:i + 1]) - sum(array[i + 1:])]
        print('s1=', realisations[:i + 1], ' s2=', realisations[i + 1:],
              'Probability diff=', sum(array[:i + 1]) - sum(array[i + 1:]))  #
    shannon_fano(result)


def function(x):
    return pow(x, 5) - 32 * pow(x, 4) + 5 * pow(x, 3) + 20 * pow(x, 2) - 42 * x + 72


x = [i for i in range(-100, 100)]
