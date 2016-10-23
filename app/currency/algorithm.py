from models import Multiplier, Currency
import views
import itertools


def count_profit(sequence):
    result = 1
    for i in range(0, len(sequence) - 1):
        try:
            result *= Multiplier.objects.get(currency_first=sequence[i], currency_second=sequence[i+1]).rate
        except Multiplier.DoesNotExist:
           raise views.MyError('Not enough values in database')

    return result


def find_sequence():
    result = {'profit_percent': 0, 'sequence': []}
    for depth in range(2, Currency.objects.count()+1):
        for seq in itertools.permutations(Currency.objects.all(), depth):
            sequence = list(seq)
            sequence.append(seq[0])
            profit = count_profit(sequence)
            if result['profit_percent'] == 0 and profit > 1.001:
                result['profit_percent'] = round(profit, 4)
                result['sequence'] = []
                for cur in sequence:
                    result['sequence'].append(cur.name)
            elif profit > result['profit_percent'] and len(result['sequence']) > len(sequence):
                result['profit_percent'] = round(profit, 4)
                result['sequence'] = []
                for cur in sequence:
                    result['sequence'].append(cur.name)

    if result['profit_percent'] < 1.01:
        return {'MSG': 'no risk-free opportunities exist yielding over 1.00% profit exist'}
    else:
        return result


