import random
from FlaggedPrefixAdder import FlaggedParallerPrefixAdder


class TestyFlaggedPrefixAdder:
    def __init__(self):
        self.results = {}  # Przechowuje wyniki dla każdej szerokości

    def _test_operation(self, fpa, a, b, operation_type, width):
        """Testuje pojedynczą operację i zwraca True/False"""
        try:
            if operation_type == "add":
                expected = (a + b) & ((1 << width) - 1)
                actual = fpa.add(a, b)
            elif operation_type == "inc":
                expected = (a + b + 1) & ((1 << width) - 1)
                actual = fpa.add(a, b, inc=1)
            elif operation_type == "abs":
                expected = abs(a - b) & ((1 << width) - 1)
                actual = fpa.add(a, b, absolute=True)

            return expected == actual
        except:
            return False

    def test_width(self, width, num_tests):
        """Testuje określoną szerokość bitową z określoną liczbą testów"""
        print(f"\n{'=' * 50}")
        print(f"TESTY DLA {width}-BITOWYCH LICZB ({num_tests} testów każdego typu)")
        print(f"{'=' * 50}")

        fpa = FlaggedParallerPrefixAdder(width=width)
        max_val = (1 << width) - 1

        # Inicjalizacja wyników dla tej szerokości
        self.results[width] = {
            'add': {'passed': 0, 'total': num_tests},
            'inc': {'passed': 0, 'total': num_tests},
            'abs': {'passed': 0, 'total': num_tests}
        }

        print(f"Zakres liczb: 0 - {max_val}")

        # Test A + B
        print(f"\n--- Test A + B ({num_tests} testów) ---")
        for i in range(num_tests):
            a = random.randint(0, max_val)
            b = random.randint(0, max_val)

            if self._test_operation(fpa, a, b, "add", width):
                self.results[width]['add']['passed'] += 1
                status = "✓"
            else:
                status = "✗"

            print(f"{status} Test {i + 1:2d}: {a:>6} + {b:>6} = {fpa.add(a, b):>6}")

        # Test A + B + 1
        print(f"\n--- Test A + B + 1 ({num_tests} testów) ---")
        for i in range(num_tests):
            a = random.randint(0, max_val)
            b = random.randint(0, max_val)

            if self._test_operation(fpa, a, b, "inc", width):
                self.results[width]['inc']['passed'] += 1
                status = "✓"
            else:
                status = "✗"

            print(f"{status} Test {i + 1:2d}: {a:>6} + {b:>6} + 1 = {fpa.add(a, b, inc=1):>6}")

        # Test |A - B|
        print(f"\n--- Test |A - B| ({num_tests} testów) ---")
        for i in range(num_tests):
            a = random.randint(0, max_val)
            b = random.randint(0, max_val)

            if self._test_operation(fpa, a, b, "abs", width):
                self.results[width]['abs']['passed'] += 1
                status = "✓"
            else:
                status = "✗"

            print(f"{status} Test {i + 1:2d}: |{a:>6} - {b:>6}| = {fpa.add(a, b, absolute=True):>6}")

        # Podsumowanie dla tej szerokości
        self._print_width_summary(width)

    def _print_width_summary(self, width):
        """Wyświetla podsumowanie dla określonej szerokości"""
        print(f"\n--- PODSUMOWANIE {width}-BIT ---")

        for operation, data in self.results[width].items():
            passed = data['passed']
            total = data['total']
            percentage = (passed / total) * 100

            op_name = {
                'add': 'A + B',
                'inc': 'A + B + 1',
                'abs': '|A - B|'
            }[operation]

            print(f"{op_name:>10}: {passed:>2}/{total:>2} ({percentage:>5.1f}%)")

    def run_all_tests(self):
        """Uruchamia wszystkie testy"""
        print("ROZPOCZYNANIE TESTÓW FLAGGED PARALLEL PREFIX ADDER")
        print("=" * 80)


        # Definicja liczby testów dla każdej szerokości
        test_configs = {
            2: 5,  # 2-bit: 5 testów każdego typu
            4: 10,  # 4-bit: 10 testów każdego typu
            8: 15,  # 8-bit: 15 testów każdego typu
            16: 20  # 16-bit: 20 testów każdego typu
        }

        # Uruchom testy dla każdej szerokości
        for width, num_tests in test_configs.items():
            self.test_width(width, num_tests)

        # Globalne podsumowanie
        self._print_global_summary()

    def _print_global_summary(self):
        """Wyświetla globalne podsumowanie wszystkich testów"""
        print(f"\n{'=' * 80}")
        print("GLOBALNE PODSUMOWANIE WSZYSTKICH TESTÓW")
        print(f"{'=' * 80}")

        total_passed = 0
        total_tests = 0

        print(f"{'Szerokość':<10} {'Operacja':<10} {'Wynik':<10} {'Procent':<10}")
        print("-" * 50)

        for width in sorted(self.results.keys()):
            for operation, data in self.results[width].items():
                passed = data['passed']
                total = data['total']
                percentage = (passed / total) * 100

                op_name = {
                    'add': 'A + B',
                    'inc': 'A + B + 1',
                    'abs': '|A - B|'
                }[operation]

                print(f"{width:<10} {op_name:<10} {passed}/{total:<7} {percentage:>6.1f}%")

                total_passed += passed
                total_tests += total

        print("-" * 50)
        overall_percentage = (total_passed / total_tests) * 100
        print(f"{'OGÓŁEM':<10} {'WSZYSTKIE':<10} {total_passed}/{total_tests:<7} {overall_percentage:>6.1f}%")

        print(f"\n🎯 KOŃCOWY WYNIK: {total_passed}/{total_tests} testów zaliczonych ({overall_percentage:.1f}%)")

        if overall_percentage == 100:
            print("🎉 WSZYSTKIE TESTY ZALICZONE!")
        elif overall_percentage >= 90:
            print("✅ Bardzo dobry wynik!")
        elif overall_percentage >= 75:
            print("👍 Dobry wynik!")
        else:
            print("⚠️ Wynik wymaga poprawy")


# Uruchomienie testów
if __name__ == "__main__":
    tester = TestyFlaggedPrefixAdder()
    tester.run_all_tests()
