from card import Card
from evaluation_result import Evaluation_result

import copy

'''
Układy kart
10 Poker królewski (strit w kolorze od 10 do As)
9 Poker (strit w kolorze)
8 Kareta (czwórka)
7 Full (trójka + para)
6 Kolor 
5 Strit (5 kart następujących po sobie)
4 Trójka
3 Dwie pary
2 Para
1 Wysoka karta
'''

def value_to_rank(value):
    match value:
        case 1:
            return "A"
        case 11:
            return "J"
        case 12:
            return "Q"
        case 13:
            return "K"
        case 14:
            return "A"
        case _:
            return str(value)

def is_high_card(cards):
    print("Wysoka karta")
    print(list(reversed(cards)))
    return Evaluation_result(1, "Wysoka karta", list(reversed(cards))[:5])

def best_kind(kind, candidate, max_num=5):
    if candidate[0] > max_num:
        candidate = (max_num, candidate[1])
    if candidate > kind:
        return candidate
    return kind

def how_many_of_kinds(cards):
    cards_by_value = [[] for _ in range(15)]
    cards_in_order = []

    for card in cards:
        cards_by_value[card.get_value()].append(card)

    taken_cards = 0

    results = []

    for _ in range(2):
        kind = (0, 0)
        for i, value in enumerate(cards_by_value):
            kind = best_kind(kind, (len(value), i), 5 - taken_cards)

        results.append(kind)
        cnt, value = kind

        for _ in range(cnt):
            if len(cards_by_value[value]) > 0:
                cards_in_order.append(cards_by_value[value].pop())

        taken_cards += cnt


    for cards in reversed(cards_by_value):
         cards_in_order += cards

    cards_in_order = cards_in_order[:5]

    for i, (cnt, value) in enumerate(results):
        results[i] = (cnt, value_to_rank(value))

    if results[0][0] == 4:
        return Evaluation_result(8, "Kareta (czwórka) " + results[0][1], cards_in_order)
    elif results[0][0] == 3 and results[1][0] == 2:
        return Evaluation_result(7, "Full - trójka " + results[0][1] + " i para " + results[1][1], cards_in_order)
    elif results[0][0] == 3:
        return Evaluation_result(4, "Trójka " + results[0][1], cards_in_order)
    elif results[0][0] == 2 and results[1][0] == 2:
        return Evaluation_result(3, "Dwie pary " + results[0][1] + " i " + results[1][1], cards_in_order)
    elif results[0][0] == 2:
        return Evaluation_result(2, "Para " + results[0][1], cards_in_order)
    return Evaluation_result(0)

def color_with_5_cards(cards):
    colors = [0] * 4
    #1 - Pik
    #2 - Kier
    #3 - Karo
    #4 - Trefl
    for card in cards:
        colors[card.color_to_number()] += 1

    if (max(colors) >= 5):
        m = max(colors)
        if (colors[0] == m):
            return 0
        elif (colors[1] == m):
            return 1
        elif (colors[2] == m):
            return 2
        elif (colors[3] == m):
            return 3
    return None

def color_number_to_color(color):
    match color:
        case 0:
            return "Pik"
        case 1:
            return "Kier"
        case 2:
            return "Karo"
        case 3:
            return "Trefl"

def is_flush(cards, color):
    if color == None:
        return Evaluation_result(0)

    cards_in_order = []
    for card in reversed(cards):
        if card.color_to_number() == color:
            cards_in_order.append(card)

    cards_in_order = cards_in_order[:5]
        
    return Evaluation_result(6, "Kolor " + color_number_to_color(color), cards_in_order)

def is_straight(cards):
    cards_by_value = [[] for _ in range(15)]
    cards_in_order = []

    for card in cards:
        cards_by_value[card.get_value()].append(card)
    
    cnt = 0
    start_num = 0

    for i, cards in enumerate(cards_by_value):
        if len(cards) > 0:
            cnt += 1
        else:
            cnt = 0
        if cnt >= 5:
            start_num = cards[0].get_value()

    if start_num == 0:
        return Evaluation_result(0)

    for i in range(5):
        cards_in_order.append(cards_by_value[start_num - i].pop())
    
    return Evaluation_result(5, "Strit (5 kart następujących po sobie)", cards_in_order)

def is_straight_flush(cards, color):
    if color == None:
        return Evaluation_result(0)
    
    cards_in_color = []
    cards_in_order = []

    for card in cards:
        if card.color_to_number() == color:
            cards_in_color.append(card)

    result = is_straight(cards_in_color)
    if result.power == 0:
        return Evaluation_result(0)
    else:
        cards_in_order = result.cards
    
        card = cards_in_order[0]
        color = color_number_to_color(color)

        if card.get_value() == 14:
            return Evaluation_result(10, "Poker królewski w kolorze " + color, cards_in_order)
        else:
            return Evaluation_result(9, "Poker w kolorze " + color + " zaczynający się od " + card.rank, cards_in_order)

def evaluate_hand(cards):
    cards.sort()
    result = Evaluation_result(1, "Wysoka karta " + cards[0].rank, list(reversed(cards))[:5])

    result = max(result, how_many_of_kinds(cards))

    result = max(result, is_straight(cards))

    color = color_with_5_cards(cards)
    if color != None:
        result = max(result, is_flush(cards, color))

        result = max(result, is_straight_flush(cards, color))

    return result


def print_result(result):
    print()
    if result.power == 0:
        print("Siła 0")
    else:
        print("Siła " + str(result.power))
        print(result.comment)
        print()
        for card in result.cards:
            print(card)
    print()
    print()

def test():
    a = Card("Pik", "4")
    b = Card("Pik", "5")
    c = Card("Pik", "10")
    d = Card("Pik", "J")
    e = Card("Pik", "Q")
    f = Card("Pik", "K")
    g = Card("Pik", "A")
    cards = [a, b, c, d, e, f, g]


    print_result(evaluate_hand(cards))
    
    
