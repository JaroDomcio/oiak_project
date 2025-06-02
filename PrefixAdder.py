class ParallelPrefixAdder:
    def __init__(self, width):
        self.width = width

    #Zamiana liczby na listę bitów od LSB do MSB (Odwrócona wartość binarna)
    def _bit_list(self, value):
        return [(value >> i) & 1 for i in range(self.width)]

    #Zamiana listy bitów na liczbę całkowitą
    def _int_from_bits(self, bits):
        return sum([bit << i for i, bit in enumerate(bits)])

    def add(self, A, B):
        # 1. Zamiana na listy bitów
        a_bits = self._bit_list(A)
        b_bits = self._bit_list(B)

        p = [a_bits[i] ^ b_bits[i] for i in range(self.width)]
        g = [a_bits[i] & b_bits[i] for i in range(self.width)]
        nk = [a_bits[i] | b_bits[i] for i in range(self.width)]

        G = [0] * (self.width + 1)
        NK = [1] * (self.width + 1)

        for i in range(1, self.width + 1):
            g_val = g[i - 1]
            nk_val = nk[i - 1]
            for j in range(i - 2, -1, -1):
                all_nk = 1
                for k in range(j + 1, i):
                    all_nk &= nk[k]
                g_val |= g[j] & all_nk
                nk_val &= nk[j]
            G[i] = g_val
            NK[i] = nk_val

        # 4. Obliczanie bitów sumy
        s = [p[i] ^ G[i] for i in range(self.width)]

        result = self._int_from_bits(s)
        return result


PPA = ParallelPrefixAdder(width=16)

a = 50
b = 52

PPAresult = PPA.add(a, b)
print(f"{a} + {b} = {PPAresult}")
