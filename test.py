

class Floatt(object):
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        for i in range(50):
            yield i
    
    def __str__(self):
        return "fucker"

    def __len__(self):
        return "really fucking big"


number = Floatt(1)

for i in number:
    print(i)

print(number)
