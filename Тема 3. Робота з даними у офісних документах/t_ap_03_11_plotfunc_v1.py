#t_ap_03_11_plotfunc_v1.py
# Створення робочої книги MS Excel
# Зображення графіку функції f на інтервалі [a,b] у n точках

from openpyxl import Workbook
from openpyxl.chart import (
    ScatterChart,
    LineChart,
    Reference,
    Series,
)

from math import sin


def tabulate(f, a, b, n):
    '''Табулює функцію f на інтервалі [a,b] у n точках
    '''
    h = (b - a) / (n - 1)
    x = [a + i * h for i in range(n - 1)] + [b]
    y = [f(xi) for xi in x]
    return x, y


def fun(x):
    '''x**3 - 7*x - 1
    '''
    return x**3 - 7*x - 1


def plotfunc1(a, b, n, f):
    '''Зображує графік функції f на інтервалі [a,b] у n точках
    '''
    x, y = tabulate(f, a, b, n) # табулювати функцію
    wb = Workbook()             # створити робочу книгу 
    ws = wb.active              # вибрати активний робочий аркуш
    ws.append(['x', f.__name__])# додати заголовки стовпчиків
    for i in range(n):
        ws.append([x[i], y[i]]) # додати дані

    # побудуувати графік
    chart1 = ScatterChart()
    chart1.legend = None
    xdata = Reference(ws, min_col=1, min_row=2, max_row=n+1)
    ydata = Reference(ws, min_col=2, min_row=2, max_row=n+1)
    s = Series(ydata, xvalues=xdata)
    chart1.append(s)
    ws.add_chart(chart1, "E1")
    
    wb.save(f.__name__ + '.xlsx')   #зберегти робочу книгу


if __name__ == '__main__':
    n = int(input('Кількість точок: '))
    a = float(input('Початок відрізку: '))
    b = float(input('Кінець відрізку: '))

    funcs = [fun, sin]
    for ff in funcs:
        plotfunc1(a, b, n, ff)
