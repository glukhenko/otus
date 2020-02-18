#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------

import itertools
import collections


RED_JOKER = '?R'
BLACK_JOKER = '?B'
RED_SUITS = ('H', 'D')
BLACK_SUITS = ('C', 'S')

RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
SUITS = ('S', 'C', 'D', 'H')  # ('♠', '♣', '♦', '♥')

RED_CARDS = ['{}{}'.format(rank, suit) for rank in RANKS for suit in RED_SUITS]
BLACK_CARDS = ['{}{}'.format(rank, suit) for rank in RANKS for suit in BLACK_SUITS]
WEIGHT_RANKS = {rank: i for i, rank in enumerate(RANKS)}
WEIGHT_SUITS = {suit: i for i, suit in enumerate(SUITS)}

get_rank = lambda card: card[0]
get_index_rank = lambda card: RANKS.index(card[0])
get_suit = lambda card: card[1]


# is not implemented
def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


# is not implemented
def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    return


# is not implemented
def flush(hand):
    """Возвращает True, если все карты одной масти"""
    return


# is not implemented
def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    return


# is not implemented
def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    return


# is not implemented
def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    return


# is not implemented
def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    return


def best_hand(hand):
    """
    :param hand: набор из [5-7] карт
    :return: возвращает лучший набор из 5 карт
    Примечание:
    -
    Поправки: вместо card_ranks, используем конкретную функцию best_ проверяющую комбинацию.
    Примечания:
    - метод не проверяет на наличие 5 карт, т.е. T♥ T♦ T♣ T♠ Дж, т.к. джокер мы заменяем на любую другую карту
    """
    jokers = list(set(hand) & {RED_JOKER, BLACK_JOKER})
    for joker in jokers:
        hand.remove(joker)
    # джокерные карты не могут быть заменены на те, которые уже есть в hand
    joker_hand = generate_cards_by_jokers(hand, jokers)
    kind_joker_hand = jokers_cards_for_kind(joker_hand)

    hand = sort_hand(hand)
    joker_hand = sort_hand(joker_hand)

    for func, name_combination in (
            (best_straight_flush, 'STRAIGHT FLUSH'),
            (best_care, 'CARE'),
            (best_full_house, 'FULL HOUSE'),
            (best_flash, 'FLASH'),
            (best_straight, 'STRAIGHT'),
            (best_set, 'SET'),
            (best_two_pair, 'TWO PAIR'),
            (best_pair, 'PAIR'),
            (best_high_card, 'HIGH CARD'),
    ):
        joker_cards = joker_hand
        if name_combination not in ('STRAIGHT FLUSH', 'FLASH', 'STRAIGHT'):
            joker_cards = kind_joker_hand
        # нужно передавать копии, ибо внутри массивы могут подтвергаться изменениям
        combination = func(hand[:], joker_cards[:])
        if combination:
            print(name_combination, combination)
            return combination


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    return best_hand(hand)


def best_straight_flush(hand, joker_hand):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает лучший набор из возможных стрит-флэшей, если таковые имеются, в противном случае None
    Примечание важно проверять сначала на флэш, поскольку там может сыграть только один джокер, т.е. у нас сокращается
    набор джокерных карт, которые пойдут на определение стрита
    """
    flash = best_flash(hand, joker_hand, straight_flush_mode=True)
    if flash:
        joker_hand = list(set(joker_hand) & set(flash))
        straight = best_straight(flash, joker_hand)
        if straight:
            return straight


def best_care(hand, joker_hand):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает набор из каре + старшую карту, если таковые имеются, в противном случае None
    """
    cards = hand + joker_hand
    care = best_kind(4, cards)
    if care:
        joker_cards_used = list(set(care) & set(joker_hand))
        joker_hand = cut_joker_hand(joker_hand, joker_cards_used)
        sub_hand = cut_hand(hand, exclude_hand=care)
        return care + best_kind(1, sub_hand + joker_hand)


def best_full_house(hand, joker_hand):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает набор из сета и пары, если таковые имеются, в противном случае None
    """
    cards = hand + joker_hand
    _set = best_kind(3, cards)
    if _set:
        joker_cards_used = list(set(_set) & set(joker_hand))
        joker_hand = cut_joker_hand(joker_hand, joker_cards_used)
        sub_hand = cut_hand(hand, exclude_hand=_set)
        pair = best_kind(2, sub_hand + joker_hand)
        if pair:
            return _set + pair


def best_flash(hand, joker_hand, straight_flush_mode=False):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :param straight_flush_mode: в результате будет содержатся несколько джокерных карт, каждая из которых составляет флэш
    :return: возвращает лучший флеш, если таковой имеется, в противном случае None
    Примечание: для получения флеша можно сыграть только одной джокерной картой, если даны две
    """
    if joker_hand:
        high_joker_cards = get_high_card_by_suits(joker_hand)
        best_flash = best_flash_by_5(hand, high_joker_cards)
        if best_flash:
            if straight_flush_mode:
                suit_flash = get_suit(best_flash[0])
                best_joker_cards = [card for card in joker_hand if get_suit(card) == suit_flash]
                # уберем дубли, т.к. best_flash может содержать джокера
                return list(set(best_flash + best_joker_cards))
            else:
                return best_flash
    else:
        return best_flash_by_5(hand)


def best_flash_by_5(hand, high_joker_cards=None):
    """
    :param hand:
    :param high_joker_cards: набор старших джокерных карт на каждую масть, т.е. 4 старших карты в случае 2 джокеров
    :return: возвращает лучший флеш, если таковой имеется, в противном случае None
    """
    cards = list(hand)
    if high_joker_cards:
        cards += high_joker_cards
    suits = list(map(get_suit, cards))
    for suit in SUITS:
        if suits.count(suit) >= 5:
            res = [card for card in sort_hand(cards) if get_suit(card) == suit][-5:]
            return res


def best_straight(hand, joker_hand):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает лучший набор из возможных стритов, если таковые имеются, в противном случае None
    Примечание: при наличии джокеров среди нескольких стритов выбираем лучший по весу
    """
    if joker_hand:
        hand = list(set(hand) - set(joker_hand))
        weight_straight = {}
        for joker_cards in jokers_cards_for_straight(joker_hand):
            straight = best_straight_by_hand(hand + joker_cards)
            if straight:
                weight = get_weight_hand(straight)
                weight_straight[weight] = straight
        if weight_straight:
            best_weight = max(weight_straight)
            return weight_straight[best_weight]
    else:
        straight = best_straight_by_hand(hand)
        if straight:
            return straight


def best_straight_by_hand(hand):
    """
    :param hand: набор из 7 карт
    :return: возвращает набор из 5 карт если он является стритом, в противном случае None
    PS: в случае отсортированной руки достаточно 3 проверки на стрит
    """
    for shift in reversed(range(3)):
        cards = hand[shift: shift + 5]
        if best_straight_by_5(cards):
            return cards


def best_straight_by_5(hand):
    """
    :param hand: набор из 5 карт
    :return: возвращает набор если он является стритом, в противном случае None
    PS: стритом будем считать, если все имеют одинаковые ранги и разница между границами составляет 4
    """
    hand = sort_hand(hand)
    ranks = list(map(get_index_rank, hand))
    first, last = ranks[0], ranks[-1]
    if len(set(ranks)) == 5 and (last - first) == 4:
        return hand

    # необходимо учесть случай перехода, т.е. 5♦ 4♥ 3♠ 2♦ A♦.
    rank_a = RANKS.index('A')
    rank_2 = RANKS.index('2')
    if rank_a in ranks and rank_2 in ranks:
        ranks.pop(rank_a)
        first, last = ranks[0], ranks[-1]
        if len(set(ranks)) == 4 and (last - first) == 3:
            return hand


def best_set(hand, joker_hand):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает сет + 2 старшие карты, если таковые имеются, в противном случае None
    """
    cards = hand + joker_hand
    _set = best_kind(3, cards)
    if _set:
        joker_cards_used = list(set(_set) & set(joker_hand))
        joker_hand = cut_joker_hand(joker_hand, joker_cards_used)
        sub_cards = cut_hand(hand, exclude_hand=_set)
        high_cards = best_kind(1, sub_cards + joker_hand, count_seq=2)
        return _set + high_cards


def best_two_pair(hand, joker_hand):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает две лучшие пары, в противном случае None
    """
    cards = hand + joker_hand
    pairs = best_kind(2, cards, count_seq=2)
    if pairs:
        joker_cards_used = list(set(pairs) & set(joker_hand))
        joker_hand = cut_joker_hand(joker_hand, joker_cards_used)
        sub_cards = cut_hand(hand, exclude_hand=pairs)
        high_card = best_kind(1, sub_cards + joker_hand, count_seq=1)
        return pairs + high_card


def best_pair(hand, joker_hand):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возврает лучшую пару, в противном случае None
    """
    cards = hand + joker_hand
    pair = best_kind(2, cards)
    if pair:
        joker_cards_used = list(set(pair) & set(joker_hand))
        joker_hand = cut_joker_hand(joker_hand, joker_cards_used)
        sub_cards = cut_hand(hand, exclude_hand=pair)
        high_cards = best_kind(1, sub_cards + joker_hand, count_seq=3)
        return pair + high_cards


def best_high_card(hand, joker_hand):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает 5 лучших карт из набора
    """
    cards = hand + joker_hand
    high_cards = best_kind(1, cards, count_seq=5)
    if high_cards:
        return high_cards


###############################
### вспомогательные функции ###
###############################

def get_weight(card):
    """
    :param card: карта, str
    :return: Возвращает вес карты, int
    Примеры:
        2S -> 0
        4D -> 22
        TS -> 80
        AH -> 123
    """
    rank, suit = card
    return 10 * WEIGHT_RANKS.get(rank) + WEIGHT_SUITS.get(suit)


def get_weight_hand(hand):
    """
    :param hand: набор карт
    :return: Вовзращает вес руки
    """
    return sum(map(get_weight, hand))


def sort_hand(hand):
    """
    :param hand: набор карт, array str
    :return: отсортированный набор карт 2S, 2C, 2D, ... AC, AD, AH, array str
    """
    hand_with_weight = {get_weight(card): card for card in hand}
    return [hand_with_weight.get(weight) for weight in sorted(hand_with_weight)]


def cut_hand(hand, exclude_hand):
    """
    :param hand: набор карт
    :param exclude_hand: набор карт
    :return: Исключает из набора hand набор exclude_hand
    """
    # PS: важно сохранить порядок следования карт в руке, поэтому не используем разность множеств
    return [card for card in hand if card not in exclude_hand]


def cut_joker_hand(joker_hand, joker_cards_used):
    """
    :param joker_hand: набор джокерных карт
    :param joker_cards_used: набор разыгранных карт
    :return: Исключает все сгенерированные карты из joker_hand на основе уже сыгранных карт
    """
    for joker_card in joker_cards_used:
        joker_suit = get_suit(joker_card)
        if joker_suit in RED_SUITS:
            joker_hand = list(set(joker_hand) - set(RED_CARDS))
        if joker_suit in BLACK_SUITS:
            joker_hand = list(set(joker_hand) - set(BLACK_CARDS))
    return joker_hand


def best_kind(count_card_need, hand, count_seq=1):
    """
    :param count_card_need: искомое количество карт с одинаковым rank
    :param hand: набор из N кат, array str
    :param count_seq: количество наборов последовательностей с count_card_need
    :return: возвращает count_seq наборов с количеством count_card_need кард, в противном случае None
    Например: best_kind(count_card_need=3, hand, count_seq=2) => [6C, 6D, 6H, 10H, 10D, 10C]
    Примечание: чтобы не пропустить фул-хаус в примере выше, проверку делаем >= n
    """
    hand = sort_hand(hand)
    best_kind_cards = []

    i = count_seq
    while i:
        best_rank = find_best_rank(count_card_need, hand)
        if not best_rank:
            break
        n_cards = [card for card in hand if get_rank(card) == best_rank][-count_card_need:]
        best_kind_cards += n_cards
        hand = cut_hand(hand, exclude_hand=n_cards)
        i -= 1

    # проверим, вдруг нашли меньше, чем требуется
    if len(best_kind_cards) == count_card_need * count_seq:
        return best_kind_cards


def find_best_rank(count_card_need, hand):
    """
    :param count_card_need: искомое количество карт с одинаковым rank
    :param hand: набор из N кат, array str
    :return: Ищет лучшую комбинацию из count_card_need одинаковых rank
    """
    ranks = list(map(get_rank, hand))
    best_ranks = [rank for rank, count_rank in collections.Counter(ranks).items() if count_rank >= count_card_need]
    for rank in ranks[::-1]:
        if rank in best_ranks:
            return rank


def get_high_card_by_suits(joker_hand):
    """
    Возвращает старшие карты каждой масти из набора joker_hand
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает по 1 старшей карте на каждую масть из набора joker_hand
    PS: необходимо в основном для определения флэша
    Например:
        input: [..., 'JH', 'JD', 'QH', 'QD', 'KD', 'AD']
        output: ['QH', 'AD']
    """
    result = []
    suits = set(map(get_suit, joker_hand))
    for card in joker_hand[::-1]:
        suit = get_suit(card)
        if suit in suits:
            result.append(card)
            suits.remove(suit)
        if not suits:
            break
    return result


def generate_cards_by_jokers(hand, jokers):
    """
    Генерирует возможные карты колоды, которые могут быть заменены джокерами, в которые не входят входные карты
    :param hand: набор из [5-7] карт
    :param jokers: список джокеров
    :return: список карт
    """
    cards_by_jokers = {
        RED_JOKER: RED_CARDS,
        BLACK_JOKER: BLACK_CARDS,
    }
    cards = []
    for joker in jokers:
        cards += cards_by_jokers.get(joker)
    return list(set(cards) - set(hand))


def jokers_cards_for_straight(joker_hand):
    """
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает отсортированный набор джокерных карт для стрита, по одной карте или по двум (в зависимости
    от количества джокерных карт)
    PS: по сути не важно какой suit назначить по существующим джокерам, поэтому в случае только черного джокера
    берем крести, в противном случае черви. А для случая стрит-флеша, сначала идет проверка на флеш, которая
    фильтрует джокерные карты до одного suit.
    """
    joker_suits = set(map(get_suit, joker_hand))
    joker_suit = 'C' if joker_suits & set(BLACK_SUITS) else 'H'
    count_jokers = joker_suits & (set(RED_SUITS) | set(BLACK_SUITS))
    need_pair = count_jokers == 4

    joker_cards = ['{}{}'.format(rank, joker_suit) for rank in set(map(get_rank, joker_hand))]
    joker_cards = sort_hand(joker_cards)
    if need_pair:
        # формируем комбинации из соседних карт
        joker_cards = list(zip(joker_cards[:-1], joker_cards[1:]))
    else:
        joker_cards = [[card] for card in joker_cards]
    return joker_cards


def jokers_cards_for_kind(joker_hand):
    """
    :param hand: набор из [5-7] карт
    :param joker_hand: набор из n карт, в которые можно превратить джокеров
    :return: возвращает набор, в котором выбрана только одна карта из двух возможных для каждого rank
    """
    if not joker_hand:
        return []
    result = []
    for rank in RANKS:
        for cards in (
                (rank + 'H', rank + 'D'),
                (rank + 'C', rank + 'S'),
        ):
            exist_cards = list(filter(lambda card: card in joker_hand, cards))
            if exist_cards:
                result.append(exist_cards[0])
    return result


#############
### Тесты ###
#############

def test_best_hand():
    print "test_best_hand..."
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'


def test_best_wild_hand():
    print "test_best_wild_hand..."
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'

if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
