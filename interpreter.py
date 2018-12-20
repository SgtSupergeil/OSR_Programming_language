from random import randint,random
from sys import argv

#This is the official interpreter for OSR!


#define regisers,stack and the valid instructions, all other instructions will be bocked

registers =  {'R0':0,'R1':0,'R2':0,'R3':0,'ACC':0,'CMP':0}
stack = []
instruction_set = ['MOV','ADD','SUB','MUL','DIV','CMP','JMP','JE','JNE','JGE','JLE','JG','JL','PSH','POP','PSS','PSI','REI','RES','EXT','RNI','PS','PI','SET']


def special_split(string):

    #Sperate line by spaces but also watch out for user defined strings:
    #123 "string with spaces" ACC => ["123","string with spaces","ACC"]

    out = []
    tmp = ''
    string_trigger = False

    for x in string:
        if x == ' ' and not string_trigger:
            out.append(tmp)
            tmp = ''
        if x == '"':
            if string_trigger:
                #string is closed
                string_trigger = False
                out.append(tmp+'"')
                tmp = ''
            else:
                #string is opened
                string_trigger = True
                tmp += '"'
        else:
            tmp += x

    out.append(tmp)
    return [x.strip() for x in out if x.strip()]

def get_true_value(string):

    #convert all tokens in line to their real values:
    #for example: ACC = 0; R0 = 42
    #ACC "string test" R0 => [0,"string test",42]

    if string in instruction_set:
        return string

    if string[0] == '"' and string[-1] == '"':
        return string[1:-1]

    if string[0:3] == 'STK' and string[-1] == ']' and string[3] == '[':
        val = string.split('[')[-1].split(']')[0]

        try:
            int(get_true_value(val))
        except:
            raise TypeError('A stack index must be an int')

        try:
            return stack[int(get_true_value(val))]
        except:
            raise ValueError('Stack index out of bounds')

    if string == 'R0':
        return registers['R0']
    elif string == 'R1':
        return registers['R1']
    elif string == 'R2':
        return registers['R2']
    elif string == 'R3':
        return registers['R3']
    elif string == 'ACC':
        return registers['ACC']
    else:
        if  string[0] == '+': # relative jumps
            try:
                rel_jmp = int(get_true_value(string[1:]))
                return '+'+str(rel_jmp)
            except:
                pass
        else:
            try:
                return float(string)
            except Exception as e:
                raise ValueError('Invalid token: {} could not be parsed'.format(string))

def intlist_to_string(intlist):

    #convert a list of ints to a string
    #ignore unprintables
    #usefull when printing stack as a string

    out = ''

    for x in intlist:
        try:
            out += chr(int(x))
        except:
            pass

    return out

def run(code,debug=0):
    global stack

    lines = [x for x in code.split('\n')]
    linecount = 0
    try:

        while True:

            if linecount >= len(lines):
                #we reached the end
                break

            line = lines[linecount]
            debug_linecount = linecount

            if not line or line.startswith('//'):
                #ignore empty lines and comments
                linecount += 1
                continue

            arguments = special_split(line)
            arguments_nums = [get_true_value(x) for x in arguments]
            instruction = arguments[0]



            if instruction == 'MOV':

                value  = arguments_nums[1]
                target = arguments[2]

                registers[target] = value

            if instruction == 'ADD':

                value  = arguments_nums[1]
                registers['ACC'] = registers['ACC'] + value

            if instruction == 'SUB':

                value  = arguments_nums[1]
                registers['ACC'] = registers['ACC'] - value

            if instruction == 'MUL':

                value  = arguments_nums[1]
                registers['ACC'] = registers['ACC'] * value

            if instruction == 'DIV':

                value  = arguments_nums[1]
                registers['ACC'] = registers['ACC'] / value

            if instruction == 'CMP':

                valuea = arguments_nums[1]
                valueb = arguments_nums[2]

                registers['CMP'] = valuea-valueb

            if instruction == 'JMP':

                value  = arguments_nums[1]

                if type(value) == str:
                    linecount += int(value[1:])-1
                else:
                    linecount = int(value)-1

            if instruction == 'JE':

                value = arguments_nums[1]

                if registers['CMP'] == 0:
                    if type(value) == str:
                        linecount += int(value[1:])-1
                    else:
                        linecount = int(value)-1

            if instruction == 'JNE':

                value = arguments_nums[1]

                if registers['CMP'] != 0:
                    if type(value) == str:
                        linecount += int(value[1:])-1
                    else:
                        linecount = int(value)-1

            if instruction == 'JGE':

                value = arguments_nums[1]

                if registers['CMP'] >= 0:
                    if type(value) == str:
                        linecount += int(value[1:])-1
                    else:
                        linecount = int(value)-1

            if instruction == 'JLE':

                value = arguments_nums[1]

                if registers['CMP'] <= 0:
                    if type(value) == str:
                        linecount += int(value[1:])-1
                    else:
                        linecount = int(value)-1

            if instruction == 'JG':

                value = arguments_nums[1]

                if registers['CMP'] > 0:
                    if type(value) == str:
                        linecount += int(value[1:])-1
                    else:
                        linecount = int(value)-1

            if instruction == 'JL':

                value = arguments_nums[1]

                if registers['CMP'] < 0:
                    if type(value) == str:
                        linecount += int(value[1:])-1
                    else:
                        linecount = int(value)-1

            if instruction == 'PSH':

                value = arguments_nums[1]

                stack.insert(0,value)

            if instruction == 'POP':

                target = arguments[1]

                value = stack[0]
                stack = stack[1:]

                registers[target] = value

            if instruction == 'PSS':
                #print stack string

                valuea = int(arguments_nums[1])
                valueb = int(arguments_nums[2])

                stack_nums = stack[valuea:valueb]

                string = intlist_to_string(stack_nums)

                print(string)

            if instruction == 'PSI':
                #print stack int

                n_args = len(arguments_nums)-1

                if n_args == 0:
                    stack_nums = stack

                if n_args == 1:

                    valuea = int(arguments_nums[1])
                    stack_nums = stack[valuea:]

                if n_args == 2:
                    valuea = int(arguments_nums[1])
                    valueb = int(arguments_nums[2])
                    stack_nums = stack[valuea:]


                print(' '.join([str(x) for x in stack_nums]))

            if instruction == 'REI':
                #read int

                target = arguments[1]

                try:
                    num = float(input())
                    registers[target] = num
                except:
                    pass

            if instruction == 'RES':
                #read string

                read_until = int(arguments_nums[1])

                try:
                    string = str(input()[:read_until])
                    nums = [ord(x) for x in string]
                    stack = nums+stack
                except:
                    pass

            if instruction == 'RNI':

                min = registers['R2']
                max = registers['R3']
                target = arguments[1]

                registers[target] = randint(min,max)

            if instruction == 'PS':

                string = arguments[1]

                print(string[1:-1].replace('\\n','\n'),end='')

            if instruction == 'PI':

                value = arguments_nums[1]

                print(value,end='')

            if instruction == 'SET':
                #set int on stack

                index = int(arguments_nums[1])
                value = arguments_nums[2]

                stack[index] = value

            if instruction == 'EXT':

                value = arguments_nums[1]

                exit(int(value))


            if debug:
                print('LINENUM: {} | LINE: {} | CONVERTED: {}'.format(debug_linecount,line,arguments_nums))
                print('\n'.join([' : '.join([str(x),str(registers[x])]) for x in registers]))
                print('STACK:',stack)
                print('-'*20)

            linecount += 1

    except Exception as e:
        print('ERROR IN LINE {}: {} | INST: {}'.format(debug_linecount,e,line))

if __name__ == '__main__':
    run(open(' '.join(argv[1:]),'r').read(),debug=0)
