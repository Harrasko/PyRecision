import re

class PyRecision:

    def sub_computations(self, x):
        sub_computation = re.findall('\((.*)\)', x)
        for computation in sub_computation:
            if '(' in computation:
                computation = self.sub_computations(computation)
            prime_ecuations = re.findall('(\d+(?:\.\d+|)(?:\/|\*)(?:\+|\-|)\d+(?:\.\d+|))', computation)
            if prime_ecuations:
                computation = self.prime_ecuations_func(prime_ecuations, computation)
            numbers = re.findall('(\d+(?:\.\d+|))[+-]([+-]?\d+(?:\.\d+|))', computation)
            symbols = re.findall('[+*\-\/]', computation)
            result = numbers[0][0]
            syms = 0
            for number in numbers[0][+1:]:
                result = self.calculator(result, number, symbols[syms])
                syms += 1
            x = re.sub(r'(\(.*?\).*)', str(result), x, 1)
        return x

    def correct_number(self, old):
        #return old
        strold = str(old)
        if 'e+' in strold:
            self.anno = 1
            old_towards = re.findall('(\d+\.\d+)(e\+(\d+))', strold)
            new_num = old_towards[0][0].replace('.', '')
            for z in range(int(old_towards[0][2])-16):
                new_num = new_num + '0'
            return new_num
        elif 'e-' in strold:
            self.anno = 1
            old_towards = re.findall('(\d+[\.\d+]*)(e\-(\d+))', strold)
            new_num = old_towards[0][0].replace('.', '')
            for z in range(int(old_towards[0][2])-1):
                new_num = '0' + new_num
            new_num = f'0.{new_num}'
            return new_num
        return old

    def calculator(self, x, y, sym):
        if '.' in str(x) or '.' in str(y):
            x = float(x)
            y = float(y)
            self.we_use_float = True
        else:
            x = int(x)
            y = int(y)
        if sym == '*':
            return x*y
        elif sym == '/':
            return x/y
        elif sym == '-':
            return x-y
        elif sym == '+':
            return x+y

    def prime_ecuations_func(self, prime_ecuations, x):
        numbers = re.findall('(\d+(?:\.\d+|))[*\/+-]([*\/+-]?\d+(?:\.\d+|))', prime_ecuations[0])
        symbols = re.findall('[*\/]', prime_ecuations[0])
        result = self.calculator(self.correct_number(numbers[0][0]), self.correct_number(numbers[0][1]), symbols[0])
        x = re.sub(r'(\d+(?:\.\d+|)(?:\/|\*)(?:\+|\-|)\d+(?:\.\d+|))', str(result), x, 1)
        prime_ecuations = re.findall('(\d+(?:\.\d+|)(?:\/|\*)(?:\+|\-|)\d+(?:\.\d+|))', x)
        if prime_ecuations:
            return self.prime_ecuations_func(prime_ecuations, x)
        return x

    def start(self):
        x = input("\nEnter computation: ")
        x = self.sub_computations(x)
        prime_ecuations = re.findall('(\d+(?:\.\d+|)(?:\/|\*)(?:\+|\-|)\d+(?:\.\d+|))', x)
        if prime_ecuations:
            x = self.prime_ecuations_func(prime_ecuations, x)
        symbols = re.findall('\d(?:(\+|\-))', x)
        if symbols:
            numbers = re.findall('(\d+(?:\.\d+|))[+-]([+-]?\d+(?:\.\d+|))', x)
            result = numbers[0][0]
            syms = 0
            for number in numbers[0][+1:]:
                result = self.calculator(result, number, symbols[syms])
                syms += 1
            x = result
        print(f'\nThe result is: {self.correct_number(float(x) if self.we_use_float else x)}')
        if self.anno:
            print("The value is approximate")
        
    def __init__(self):
        self.we_use_float = False
        self.anno = 0
        try:
            self.start()
        except Exception as err:
            print(f'\nAre you kidding me... {err}?!')


if __name__ == "__main__":
    PyRecision()
