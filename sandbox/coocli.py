from collections import OrderedDict


def quantizations_ordered():
    quantization_thresholds = {'': 1e0,
                               'Thousands': 1e3,
                               'Millions': 1e6,
                               'Billions': 1e9,
                               'Trillions': 1e12,
                               'Quadrillions': 1e15,
                               'Quintillions': 1e18}
    return OrderedDict(sorted(quantization_thresholds.items(), key=lambda k: k[1]))


def human_readable(total):
    quantizations = quantizations_ordered()
    final_name, final_quant = determine_quantization(quantizations, total)
    readable_string = '{:.1f} {}'.format(total / final_quant, final_name)
    return readable_string


def determine_quantization(quantizations, total):
    final_name, final_quant = '', 0
    for name, quant in quantizations.items():
        if total >= quant:
            final_name = name
            final_quant = quant
    return final_name, final_quant


def c_per_minute(income_):
    total = 60 * income_
    return human_readable(total)


def c_per_hour(income_):
    total = 3600 * income_
    return human_readable(total)


def main():
    print('C per minute: {}'.format(c_per_minute(income)))
    print('C per hour: {}'.format(c_per_hour(income)))


if __name__ == '__main__':
    income = 6e15

    main()
