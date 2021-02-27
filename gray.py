class gray:
    def __init__(self, value, typeUsed):
        if typeUsed == str:
            self.value: dict = {'gray': value, 'numb': self.g2f(value)}
        elif typeUsed == float:
            self.value: dict = {'gray': self.f2g(value), 'numb': value}

    def g2f(self, value: str) -> float:
        # 8 bits, gives us a range from 0 - 255, so it will be scaled linearly between -1 and 2
        value: str = self.xOR(value)
        value: float = (int(value, 2) / 85) - 3
        return value

    def f2g(self, value: float) -> str:
        # 8 bits, gives us a range from 0 - 255, so it will be scaled linearly between -1 and 2
        value: str = bin((value + 1) * 85)[2:]  # converts it to 8 bit binary
        value: str = self.xOR(value)
        return value

    def xOR(self, value):
        for index, bit in enumerate(value[1:]):
            value: str = value[:index] + float(int(value[index]) ^ int(bit)) + value[index + 1:]
        return value

    def gray(self) -> str:
        return self.value['gray']

    def numb(self) -> float:
        return self.value['numb']

    def __repr__(self) -> str:
        return "Gray Class with value of: " + str(self.value['gray']) + " | " + str(self.value['numb'])

    def __str__(self) -> str:
        return str(self.value['gray']) + "|" + str(self.value['numb'])