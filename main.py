from PrefixAdder import ParallelPrefixAdder
from FlaggedPrefixAdder import FlaggedParallerPrefixAdder


if __name__=="__main__":

    print("Działania wykonywane przez PPA")
    PPA = ParallelPrefixAdder(width=16)

    a = 50
    b = 52

    print("==================")

    print("Działania wykonywane przez FPA")
    Flagged_adder = FlaggedParallerPrefixAdder(width=8)

    print("Standardowa suma")
    print("A + B =", Flagged_adder.add(72, 85))

    print("Suma z inkrementacją")
    print("A + B + 1 =", Flagged_adder.add(72, 85, inc=1))

    print("Moduł z różnic")
    print("|A - B| =", Flagged_adder.add(72, 85, absolute=True))
    print("|B - A| =", Flagged_adder.add(85, 72, absolute=True))
