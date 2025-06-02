class FlaggedParallerPrefixAdder():
    def __init__(self, width):
        self.width = width

    def _bit_list(self, value):
        return [(value >> i) & 1 for i in range(self.width)]

    def _int_from_bits(self, bits):
        return sum([bit << i for i, bit in enumerate(bits)])

    def add(self, A, B, inc=0, cmp=0, absolute=False):
        # If absolute difference mode is on, compute A - B and check sign
        if absolute:
            # Step 1: Try A - B (using A + ~B + 1)
            result = self._add_internal(A, B, inc=1, cmp=0, invert_B=True)
            msb = (result >> (self.width - 1)) & 1

            # Step 2: If result is negative (MSB=1), switch operands
            if msb == 1:
                result = self._add_internal(B, A, inc=1, cmp=0, invert_B=True)

            return result
        else:
            # Regular flagged prefix adder
            return self._add_internal(A, B, inc, cmp, invert_B=False)

    def _add_internal(self, A, B, inc=0, cmp=0, invert_B=False):
        a_bits = self._bit_list(A)
        b_bits = self._bit_list(B ^ (0xFF if invert_B else 0))

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

        s = [p[i] ^ (G[i] | (NK[i] & inc)) ^ cmp for i in range(self.width)]

        return self._int_from_bits(s)


