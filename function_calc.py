import re
import numpy as np


def calc(operand1, operand2, operator):
    # calculate the basic operations
    # Input:
    #   - operand1: first operand of the basic operation
    #   - operand2: second operand of the basic operation
    #   - operator: the operator of the basic operation
    # Output:
    #   - return the result as a float number
    op1 = float(operand1)
    op2 = float(operand2)
    if operator == '^':
        return op1 ** op2
    if operator == '*':
        return op1 * op2
    if operator == '/':
        if op2 == 0:
            return np.nan
        return op1 / op2
    if operator == '+':
        return op1 + op2
    if operator == '-':
        return op1 - op2


def calcByIdx(fArray, idx):
    # this function reduce the function expression by calculating the operation of the given index in the function array
    # Input:
    #   - fArray: array of expression elements
    #   - idx   : index of the operator to calculate its basic operation
    # Output:
    #   - newFunArray: array of the new resulted expression elements
    oldFunArray = fArray.copy()
    newFunArray = []
    result = str(calc(oldFunArray[idx - 1], oldFunArray[idx + 1], oldFunArray[idx]))
    for j, value in enumerate(oldFunArray):
        if j == idx or j == idx + 1:
            continue
        if j == idx - 1:
            newFunArray.append(result)
        else:
            newFunArray.append(value)

    return newFunArray




def calculateExpersion(functionArray, xValue):
    # the main procedure to calculate function expression for a given x value
    # Input:
    #   - functionArray: array of elements of the function expression (operators, operands and x char)
    #   - xValue: the value of x to compute the function at that point by substitution
    # Output:
    #   - finalResult: the y value of the corresponding x value from the function expression
    newFunction = functionArray.copy()
    found = True
    i = -1

    # substituting the x char with its given value in the whole expression
    while i < len(newFunction) and found == True:
        if 'x' in newFunction[i + 1:]:
            i = newFunction.index('x', i + 1)
            found = True
            newFunction[i] = xValue
        elif '-x' in newFunction[i + 1:]:
            i = newFunction.index('-x', i + 1)
            found = True
            newFunction[i] = -xValue
        else:
            found = False


    # calculate ^ (from right to left)
    while '^' in newFunction:
        # looping in reverse
        for idx,element in enumerate(newFunction[::-1]):
            if element == '^':
                newFunction = calcByIdx(newFunction, len(newFunction)-idx-1)
                break

    # calculate *, / (from left to right)
    while '*' in newFunction or '/' in newFunction:
        for idx,element in enumerate(newFunction):
            if element == '*' or element == '/':
                newFunction = calcByIdx(newFunction, idx)
                break

    # calculate +, - (form left to right)
    while '+' in newFunction or '-' in newFunction:
        for idx,element in enumerate(newFunction):
            if element == '+' or element == '-':
                newFunction = calcByIdx(newFunction, idx)
                break

    finalResult = newFunction[0]
    return finalResult



def function_parsing(funcString):
    # convert the function expression string into array of well organized elements (operators, operands and x char)
    # Input:
    #   - funcString: the input function expression as a string
    # Output:
    #   - functionElements: the well organized array of separated elements (operators, operands and x char)
    negative = False
    operator = False
    number = False
    opIdx_old = -1
    functionElements = []
    for index, char in enumerate(funcString):
        if (number == False and negative == False and char == '-'): #index == 0 or
            negative = True
            operator = False
            number = True
        elif (number == True and negative == False and char in "-+*/^"):
            negative = False
            operator = True
            number = False
            functionElements.append(funcString[opIdx_old+1:index])
            opIdx_old = index
            functionElements.append(char)
        elif (char in "0123456789."):
            negative = False
            operator = False
            number = True
        elif (char == 'x'):
            operator = False
            number = True
    functionElements.append(funcString[opIdx_old+1:index+1])

    # print(functionElements)
    return functionElements


def funcStringIsValid(funcString):
    # this function validate the input string as an accepted function expression
    # Input:
    #   - funcString: the input string for function expression
    # Output:
    #   - True or False: True in case of accepted expression

    # validate the allowed characters in the string (first check without any order)
    found = re.findall("[-+*/^x.0-9]",funcString) # "^-[0-9]+|^[0-9]+|[0-9]+[-+*/^][0-9]+"
    # # print(len(found), len(funcString))
    if (len(found) < len(funcString)):
        return False

    # check the start of the expression
    start = re.match('^[-x0-9]',funcString)
    if (start == None):
        # print("no match start")
        return False

    # check the end of the expression
    end = re.findall('[x0-9]$', funcString)
    if (len(end) == 0):
        # print("no match end")
        return False

    # check for no 2 operators in sequence
    errors = re.findall('[-+*/^][+*/^]|[-+][-]', funcString)
    if (len(errors) > 0):
        return False

    # split by operators to find restrictions on operands
    operands = re.split('[-+*/^]',funcString)
    for operand in operands:
        if operand == '':
            continue
        x = re.fullmatch('(\d+[.]{1}\d+)|x{1}|\d+', operand)
        if x == None:
            return False

    return True
