from copy import deepcopy
from math import gcd


def OutPutSluTex(slu, sep, output, delim=''):
    print(f'{delim} ' + '\\left( \\begin{array}{' + 'c' * sep + ('|' if sep != len(slu[0]) else '') + 'c' * (
            len(slu[0]) - sep) + '}', file=output)
    for i in range(len(slu)):
        print(' & '.join(map(str, slu[i])) + ('\\\\' if i != len(slu) - 1 else ''), file=output)
    print('\\end{array}\\right)', file=output)


def OutPutSlu(slu, sep):
    x = max(map(len, map(str, [slu[i][j] for i in range(len(slu)) for j in range(len(slu[0]))]))) + 1
    for i in range(len(slu)):
        for j in range(len(slu[0])):
            print(f'{str(slu[i][j]).rjust(x)}', end=('|' if j == sep - 1 and sep != len(slu[0]) else ' '))
        print('')


def TransposeSLU(slu):
    a = len(slu)
    b = len(slu[0])
    resSLU = []
    for i in range(b):
        temp = []
        for j in range(a):
            temp.append(slu[j][i])
        resSLU.append(deepcopy(temp))
    return resSLU


def Move(slu, x, y, z, tr):
    if tr:
        slu = TransposeSLU(slu)
    if z == 'swap':
        slu[x - 1], slu[y - 1] = slu[y - 1], slu[x - 1]
    elif z == '*':
        slu[x - 1] = [item * y for item in slu[x - 1]]
    elif z == '/':
        for item in slu[x - 1]:
            if item % y != 0:
                break
        else:
            slu[x - 1] = [item // y for item in slu[x - 1]]
    else:
        for i in range(len(slu[0])):
            slu[x - 1][i] += z * slu[y - 1][i]
    if tr:
        slu = TransposeSLU(slu)
    return slu


def addHist(slu, hist, trHist, sepHist, sep, tr):
    if slu != hist[-1]:
        hist.append(deepcopy(slu))
        trHist.append(tr)
        sepHist.append(sep)

def Shrink(slu, hist, trHist, sepHist, sep, tr):
    for i in range(len(slu)):
        temp = 1
        for j in range(len(slu[0])):
            if slu[i][j] != 0:
                temp = slu[i][j]
                for k in range(j + 1, len(slu[0])):
                    if slu[i][k] != 0:
                        temp = gcd(temp, slu[i][k])
                break
        if temp != 1:
            slu = Move(deepcopy(slu), i + 1, temp, '/', 0)
    addHist(slu, hist, trHist, sepHist, sep, tr)
    return slu


def EchelonForm(slu, mode, hist, trHist, sepHist, sep, tr):
    slu = Shrink(deepcopy(slu), hist, trHist, sepHist, sep, tr)
    row, col = 0, 0
    fav = []
    while row < len(slu) and col < len(slu[0]):
        temp = []
        for i in range(row, len(slu)):
            if slu[i][col] != 0:
                temp.append([slu[i][col], i])
        if temp:
            temp.sort(key=lambda x: abs(x[0]))
            slu = Move(deepcopy(slu), row + 1, temp[0][1] + 1, 'swap', 0)
        if slu[row][col] != 0:
            if slu[row][col] < 0:
                slu = Move(deepcopy(slu), row + 1, -1, '*', 0)
            slu = Shrink(deepcopy(slu), hist, trHist, sepHist, sep, tr)
            fav.append([row, col])
            for i in range(row + 1, len(slu)):
                if slu[i][col] != 0:
                    if slu[i][col] % slu[row][col] == 0:
                        slu = Move(deepcopy(slu), i + 1, row + 1, -slu[i][col] // slu[row][col], 0)
                    else:
                        idx = slu[row][col] // gcd(slu[i][col], slu[row][col])
                        slu = Move(deepcopy(slu), i + 1, idx, '*', 0)
                        slu = Move(deepcopy(slu), i + 1, row + 1, -slu[i][col] // slu[row][col], 0)
                    addHist(slu, hist, trHist, sepHist, sep, tr)
            row += 1
            col += 1
        else:
            col += 1
        slu = Shrink(deepcopy(slu), hist, trHist, sepHist, sep, tr)
    if mode:
        fav.reverse()
        for row, col in fav:
            for i in range(row, 0, -1):
                if slu[i - 1][col] != 0:
                    if slu[i - 1][col] % slu[row][col] == 0:
                        slu = Move(deepcopy(slu), i, row + 1, -slu[i - 1][col] // slu[row][col], 0)
                    else:
                        idx = slu[row][col] // gcd(slu[i - 1][col], slu[row][col])
                        slu = Move(deepcopy(slu), i, idx, '*', 0)
                        slu = Move(deepcopy(slu), i, row + 1, -slu[i - 1][col] // slu[row][col], 0)
                    addHist(slu, hist, trHist, sepHist, sep, tr)
        slu = Shrink(deepcopy(slu), hist, trHist, sepHist, sep, tr)
    return slu


def SluLoad():
    slu = []
    sep = 0
    colName = []
    with open('input.txt') as file_handler:
        for num, line in enumerate(file_handler):
            temp = list(line.replace('\n', '').split())
            if num == 0:
                sep = len(temp) if '|' not in temp else temp.index('|')
                if not temp[0].replace('-', '').isdigit():
                    if '|' in temp:
                        temp.remove('|')
                    colName = temp
                    continue
            if '|' in temp:
                temp.remove('|')
            temp = [x.replace('|', '') for x in temp]
            slu.append(list(map(int, temp)))
    with open('config.txt') as file_handler:
        res = []
        for num, line in enumerate(file_handler):
            if num == 3:
                break
            #temp =
            res.append(list(line.replace(' ', '').replace('\n', '').split('='))[-1])
    autoPrint, mode, delim = res
    return slu, sep, colName, int(autoPrint), int(mode), delim


def SaveSLU(slu, sep):
    inp = open('input.txt', 'w')
    for i in range(len(slu)):
        for j in range(len(slu[0])):
            print(f'{slu[i][j]}' + (' |' if j == sep - 1 != len(slu[0]) - 1 and i == 0 else ''), end='\t', file=inp)
        print(file=inp)


def UnionName(slu, colName, tr):
    if tr:
        for i in range(len(colName)):
            slu[i] = [colName[i]] + slu[i]
        return slu
    else:
        return [colName] + slu


def main():
    slu, sep, colName, autoPrint, mode, delim = SluLoad()
    post = ''
    trans = False
    if len(slu) == 0:
        print('bad SLU, try again')
        return 0
    print(f'SLU load complete, mode =', ('col' if mode else 'row'))
    print('input \'help\' for help')
    hist = [deepcopy(slu)]
    trHist = [trans]
    sepHist = [sep]
    while post != 'exit':
        if autoPrint:
            OutPutSlu(slu, sep)
        posts = input(f'step {len(hist)}: ').replace(' ', '').lower().split(',')
        for post in posts:
            if post == 'p':
                OutPutSlu(slu, sep)
            elif post == 'pt':
                cnt = 0
                constRes = ''
                while not constRes.isdigit():
                    constRes = input('How many slu one row?: ')
                constRes = int(constRes)
                output = open('output.txt', 'w')
                print('\\[', file=output)
                for sepX, trX, sluX in zip(sepHist, trHist, hist):
                    OutPutSlu(sluX, sepX)
                    ans = input('Save this matrix? (y/n): ')
                    if ans.lower() == 'y':
                        if cnt % constRes == 0 and cnt != 0:
                            print(f'{delim} \\]\n\\[', file=output)
                        if not colName:
                            OutPutSluTex(deepcopy(sluX), sepX + trX, output,
                                         delim if cnt != 0 and cnt % constRes != 0 else '')
                        else:
                            OutPutSluTex(UnionName(deepcopy(sluX), colName, trX), sepX + trX, output,
                                         delim if cnt != 0 and cnt % constRes != 0 else '')
                        cnt += 1
                print('\\]', file=output)
                output.close()
            elif post == 'back':
                if len(hist) != 1:
                    hist.pop()
                    slu = deepcopy(hist[-1])
            elif post == 'help':
                print('(i)(j) —— swap row i and row j')
                print('(i)*(k) —— elems row i * num k')
                print('(i)/(k) —— elems row i / num k')
                print('(i)+-k(j) —— row i +- k * row j')
                print('p —— print SLU')
                print('pt —— print history LaTeX code SLU')
                print('back —— cancel last action')
                print('tr —— transpose matrix')
                print('mode —— поменять вид преобразований (строки/столбцы)')
                print('form —— ступенчатый вид')
                print('best form —— улучшенный ступенчатый вид')
                print('shrink —— упростить СЛУ')
                print('save —— сохранить матрицу в input.txt')
            elif post == 'tr':
                if sep == len(slu[0]):
                    trans = False if trans else True
                    slu = TransposeSLU(slu)
                    sep = len(slu[0])
                    hist.append(deepcopy(slu))
                    trHist.append(trans)
                    sepHist.append(sep)
                else:
                    print('delete partition')
            elif post == 'mode':
                mode = (mode + 1) % 2
                print(f'now mode =', ('col' if mode else 'row'))
            elif post == 'save':
                if trans:
                    SaveSLU(slu, sep)
                else:
                    SaveSLU(UnionName(deepcopy(slu), colName, trans), sep)
            elif post == 'form':
                slu = EchelonForm(slu, 0, hist, trHist, sepHist, sep, trans)
            elif post == 'bestform':
                slu = EchelonForm(slu, 1,  hist, trHist, sepHist, sep, trans)
            elif post == 'shrink':
                slu = Shrink(deepcopy(slu), hist, trHist, sepHist, sep, trans)
            else:
                try:
                    temp = post[post.find(')') + 1:post.rfind('(')]
                    if temp == '-':
                        temp = -1
                    elif temp == '+':
                        temp = 1
                    if temp == '*':
                        slu = Move(deepcopy(slu), int(post[1:post.find(')')]), int(post[post.rfind('(') + 1:-1]), '*',
                                   mode)
                    elif temp == '/':
                        slu = Move(deepcopy(slu), int(post[1:post.find(')')]), int(post[post.rfind('(') + 1:-1]), '/',
                                   mode)
                    elif temp != '':
                        slu = Move(deepcopy(slu), int(post[1:post.find(')')]), int(post[post.rfind('(') + 1:-1]),
                                   int(temp),
                                   mode)
                    else:
                        slu = Move(deepcopy(slu), int(post[1:post.find(')')]), int(post[post.rfind('(') + 1:-1]),
                                   'swap', mode)
                        if mode and colName:
                            x = int(post[1:post.find(')')])
                            y = int(post[post.rfind('(') + 1:-1])
                            colName[x - 1], colName[y - 1] = colName[y - 1], colName[x - 1]
                    if hist[-1] != slu:
                        hist.append(deepcopy(slu))
                        trHist.append(trans)
                        sepHist.append(sep)
                except BaseException:
                    slu = deepcopy(hist[-1])


if __name__ == '__main__':
    main()