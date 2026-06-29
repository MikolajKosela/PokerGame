from models import Card, EvaluationResult

'''
Układy kart
10 Poker królewski (strit w kolorze od 10 do As) / Royal flush
9 Poker (strit w kolorze) / Straight flush
8 Kareta (czwórka) / Four of kinds
7 Full (trójka + para) / Full house
6 Kolor / Flush
5 Strit (5 kart następujących po sobie) / Straight
4 Trójka / Three of kinds
3 Dwie pary / Two pair
2 Para / One pair
1 Wysoka karta / High card
'''

def value_to_rank(value: int) -> str:
    match value:
        case 1 | 14:
            return "A"
        case 11:
            return "J"
        case 12:
            return "Q"
        case 13:
            return "K"
        case _:
            return str(value)


def is_high_card(cards: list[Card]) -> EvaluationResult:
    return EvaluationResult(1, "Wysoka karta " + cards[-1].rank, list(reversed(cards))[:5])


def best_kind(
    kind: tuple[int, int],
    candidate: tuple[int, int],
    max_num: int = 5,
) -> tuple[int, int]:
    count, value = candidate

    if count > max_num:
        candidate = (max_num, value)

    if candidate > kind:
        return candidate

    return kind


def how_many_of_kinds(cards: list[Card]) -> EvaluationResult:
    cards_by_value: list[list[Card]] = [[] for _ in range(15)]
    cards_in_order: list[Card] = []

    for card in cards:
        cards_by_value[card.get_value()].append(card)

    taken_cards = 0
    results: list[tuple[int, int]] = []

    for _ in range(2):
        kind = (0, 0)

        for i, value_cards in enumerate(cards_by_value):
            kind = best_kind(kind, (len(value_cards), i), 5 - taken_cards)

        results.append(kind)

        count, value = kind

        for _ in range(count):
            if len(cards_by_value[value]) > 0:
                cards_in_order.append(cards_by_value[value].pop())

        taken_cards += count

    for value_cards in reversed(cards_by_value):
        cards_in_order += value_cards

    cards_in_order = cards_in_order[:5]

    named_results: list[tuple[int, str]] = [
        (count, value_to_rank(value)) for count, value in results
    ]

    first_count, first_rank = named_results[0]
    second_count, second_rank = named_results[1]

    if first_count == 4:
        return EvaluationResult(8, "Kareta (czwórka) " + first_rank, cards_in_order)

    if first_count == 3 and second_count == 2:
        return EvaluationResult(
            7,
            "Full - trójka " + first_rank + " i para " + second_rank,
            cards_in_order,
        )

    if first_count == 3:
        return EvaluationResult(4, "Trójka " + first_rank, cards_in_order)

    if first_count == 2 and second_count == 2:
        return EvaluationResult(
            3,
            "Dwie pary " + first_rank + " i " + second_rank,
            cards_in_order,
        )

    if first_count == 2:
        return EvaluationResult(2, "Para " + first_rank, cards_in_order)

    return EvaluationResult(0)


def color_with_5_cards(cards: list[Card]) -> int | None:
    colors = [0] * 4

    for card in cards:
        colors[card.color_to_number()] += 1

    if max(colors) < 5:
        return None

    return colors.index(max(colors))


def color_number_to_color(color: int) -> str:
    match color:
        case 0:
            return "Pik"
        case 1:
            return "Kier"
        case 2:
            return "Karo"
        case 3:
            return "Trefl"
        case _:
            return "Nieznany kolor"


def is_flush(cards: list[Card], color: int | None) -> EvaluationResult:
    if color is None:
        return EvaluationResult(0)

    cards_in_order: list[Card] = []

    for card in reversed(cards):
        if card.color_to_number() == color:
            cards_in_order.append(card)

    cards_in_order = cards_in_order[:5]

    return EvaluationResult(
        6,
        "Kolor " + color_number_to_color(color),
        cards_in_order,
    )


def is_straight(cards: list[Card]) -> EvaluationResult:
    cards_by_value: list[list[Card]] = [[] for _ in range(15)]
    cards_in_order: list[Card] = []

    for card in cards:
        cards_by_value[card.get_value()].append(card)

    count = 0
    start_num = 0

    for value_cards in cards_by_value:
        if len(value_cards) > 0:
            count += 1
        else:
            count = 0

        if count >= 5:
            start_num = value_cards[0].get_value()

    if start_num == 0:
        return EvaluationResult(0)

    for i in range(5):
        cards_in_order.append(cards_by_value[start_num - i].pop())

    return EvaluationResult(
        5,
        "Strit (5 kart następujących po sobie)",
        cards_in_order,
    )


def is_straight_flush(cards: list[Card], color: int | None) -> EvaluationResult:
    if color is None:
        return EvaluationResult(0)

    cards_in_color: list[Card] = []

    for card in cards:
        if card.color_to_number() == color:
            cards_in_color.append(card)

    result = is_straight(cards_in_color)

    if result.power == 0:
        return EvaluationResult(0)

    cards_in_order = result.cards
    card = cards_in_order[0]
    color_name = color_number_to_color(color)

    if card.get_value() == 14:
        return EvaluationResult(
            10,
            "Poker królewski w kolorze " + color_name,
            cards_in_order,
        )

    return EvaluationResult(
        9,
        "Poker w kolorze " + color_name + " zaczynający się od " + card.rank,
        cards_in_order,
    )


def evaluate_hand(cards: list[Card]) -> EvaluationResult:
    cards.sort()

    result = is_high_card(cards)
    result = max(result, how_many_of_kinds(cards))
    result = max(result, is_straight(cards))

    color = color_with_5_cards(cards)

    if color is not None:
        result = max(result, is_flush(cards, color))
        result = max(result, is_straight_flush(cards, color))

    return result


def print_result(result: EvaluationResult) -> None:
    if result.power == 0:
        print("Siła 0")
    else:
        print("Siła " + str(result.power))

    print(result.comment)
    print()

    for card in result.cards:
        print(card)