import math


def fano(message, alph):
    codeDict = []
    for line in alph:
        codeDict.append(line[0])
    codeDict = dict(zip(codeDict, ['1', '00', '01']))
    for char in message:            #encoding
        for key in codeDict:
            if char == key:
                message = message.replace(char, codeDict[key])
    print("Кодированное сообщение "+message)
    res =''
    while message:              #decoding
        for key in codeDict:
            if message.startswith(codeDict[key]):
                res+= key
                message = message[len(codeDict[key]):]
    message = res
    print("Раскодированное сообщение " + message)

def haffman_splitter(list):   #нужно получить отсюда множественно вложенные списки
    if len(list) == 1:
        return list
    devider = int(len(list)/2)
    sum1 =0
    sum2 =0
    correct = False
    while correct == False :
        for symbol, value, code in list[:devider]:
            sum1 += float(value)
        for key, value, code in list[devider:]:
            sum2 += float(value)
        if sum1 == sum2:
            correct = True
        elif sum1 - sum2 > 0:
            devider -= 1
            sum1= 0
            sum2=0
        else:
            devider += 1
            correct = True
    for line in list[:devider]:
        line[2]+= '0'
    for line in list[devider:]:
        line[2] += '1'

    return haffman_splitter(list[:devider]), haffman_splitter(list[devider:])


def haffman(message, alph):
    symbol_list = []
    for key, value in alph:
        symbol_list.append([key, value, ''])
    print(haffman_splitter(symbol_list))
    for char in message:                        #encode
        for key, value, code in symbol_list:
            if char == key:
                message = message.replace(char, code)
    print("Кодированное сообщение " +message)
    res = ''
    while message:                              #decode
        for key, value, code in symbol_list:
            if message.startswith(code):
                res += key
                message = message[len(code):]
    message = res
    print("Расодированное сообщение " + message)


def bit_parser_shennon(qum, dlina):          #Функция, возвращающая двоичное представление вероятности
    if dlina == 0: dlina += 1
    if dlina == 2: dlina += 1
    code=''
    buf = qum
    for i in range(dlina):
        buf *= 2
        code += str(buf).split('.')[0]
        buf = float('0.' + str(buf).split('.')[1])

    return code


def shennon_coder(symbols):
    codes = []
    for char, probability, qumsum in symbols:
        code = bit_parser_shennon(qumsum, int(((-1)*math.log(float(probability)))))
        #print(code)
        codes.append(code)
    return codes

def shennon(message, alph):
    q = []
    for i in range(len(alph)):
        if i == 0:
            q.append(0)
        else:
            q.append(q[i-1] + float(alph[i-1][1]))
    for i in range(len(alph)):
        alph[i].append(float(q[i]))
    #print(alph[1][2])
    codes = shennon_coder(alph)
    for i in range(len(alph)):
        alph[i].append(codes[i])        #На этом этапе имеем сформированный словарь
    for char_m in message:
        for char_a, prob, qum, code in alph:
            if char_m == char_a:
                message = message.replace(char_m, code)
    print("Кодированное сообщение " + message)
    res = ''
    while message:
        for char, prob, qum, code in alph:
            if message.startswith(code):
                res += char
                message = message[len(code):]
    message = res
    print("Раскодированное сообщение " +message)


alphabet = []

with open('alphabet.txt', 'r') as f_alph:
    for line in f_alph:
        alphabet.append(line.split())
    f_alph.close()
mes = open("input.txt").readline()
shennon(mes, alphabet)

