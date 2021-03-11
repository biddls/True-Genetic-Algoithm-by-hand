# this class manages all of the conversion between gray code and base 10 numbers
class gray:
    def __init__(self, value, typeUsed):
        # if its given a string (genome) it coverts it to a number
        if typeUsed == str:
            self.value: dict = {'gray': value, 'numb': self.g2f(value)}
        # if its given a number it converts it to a genome (string)
        elif typeUsed == float:
            self.value: dict = {'gray': self.f2g(value), 'numb': value}

    # function to convert from a string to a float (genome to arrays)
    def g2f(self, value: str) -> float:
        # 8 bits, gives us a range from 0 - 255, so it will be scaled linearly between -1 and 2
        value: str = self.xOR(value)
        value: float = (int(value, 2) / 85) - 1
        return value

    # function to convert from a float to a string (arrays to genome)
    def f2g(self, value: float) -> str:
        # 8 bits, gives us a range from 0 - 255, so it will be scaled linearly between -1 and 2
        value: str = bin((value + 1) * 85)[2:]  # converts it to 8 bit binary
        value: str = self.xOR(value)
        return value

    # this function converts from a gray code to binary, this is done by coppying down the MSB then doing an
    # XOR opperation on every bit there after in pairs, one bit is from the old genome seq and the other bit is
    # from the new sequence that is being generated
    def xOR(self, value):
        for index, bit in enumerate(value[1:]):
            value: str = value[:index+1] + str(int(value[index]) ^ int(bit)) + value[index + 2:]
        return value

    # basic statements to return certain values
    def gray(self) -> str:
        return self.value['gray']

    def numb(self) -> float:
        return self.value['numb']

    # overwriting inbuilt functions to return values if the class is printed for example
    def __repr__(self) -> str:
        return "Gray Class: " + str(self.value['gray']) + " | " + str(self.value['numb'])

    def __str__(self) -> str:
        return str(self.value['gray']) + "|" + str(self.value['numb'])