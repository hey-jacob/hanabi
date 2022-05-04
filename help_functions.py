def list_possible_actions(game_status):

    NA = 'None'
    actions = []
    # discard
    discard_actions = []
    for card_index, card in enumerate(game_status['own_hand_knowledge']):
        action_dict = {'action_number': 0,
                       'action_type': 'D',
                       'action_description': f'Discard card at index {card_index} with value {card}',
                       'discard_card_index': card_index,
                       'play_card_index': NA,
                       'info_receiver_player_index': NA,
                       'color': NA,
                       'color_indexes': NA,
                       'number': NA,
                       'number_indexes': NA}

        discard_actions.append(action_dict)

    # play
    play_actions = []
    board = game_status["board"]
    possible_plays = []
    for key, value in board.items():
        possible_plays.append(key+str(value+1))

    for card_index, card in enumerate(game_status['own_hand_knowledge']):
        if card in possible_plays:
            action_dict = {'action_number': 0,
                           'action_type': 'P',
                           'action_description': f'Play card at index {card_index} with value {card}',
                           'discard_card_index': NA,
                           'play_card_index': card_index,
                           'info_receiver_player_index': NA,
                           'info_giver_player_index': NA,
                           'color': NA,
                           'color_indexes': NA,
                           'number': NA,
                           'number_indexes': NA}
            play_actions.append(action_dict)

    # give info
    info_actions = []
    for hand_obj in game_status['other_player_hands']:
        hand = hand_obj[0]
        pl_index = hand_obj[1]
        colors = []
        numbers = []
        for card_index, card in enumerate(hand):
            colors.append(card.get_color())
            numbers.append(card.get_number())
        colors = set(colors)
        numbers = set(numbers)

        for color in colors:
            color_indexes = []
            for card_index, card in enumerate(hand):
                if card.get_color() == color:
                    color_indexes.append(card_index)
            action_dict = {'action_number': 0,
                           'action_type': 'I-C',
                           'action_description': f'Give information to player {pl_index} on color {color} on index {color_indexes}',
                           'discard_card_index': NA,
                           'play_card_index': NA,
                           'info_receiver_player_index': pl_index,
                           'info_giver_player_index': NA,
                           'color': color,
                           'color_indexes': color_indexes,
                           'number': 'N/A',
                           'number_indexes': 'N/A'}

            info_actions.append(action_dict)

        for number in numbers:
            number_indexes = []
            for card_index, card in enumerate(hand):
                if card.get_number() == number:
                    number_indexes.append(card_index)
            action_dict = {'action_number': 0,
                           'action_type': 'I-N',
                           'action_description': f'Give information to player {pl_index} on number {number} on index {number_indexes}',
                           'discard_card_index': NA,
                           'play_card_index': NA,
                           'info_receiver_player_index': pl_index,
                           'info_giver_player_index': NA,
                           'color': NA,
                           'color_indexes': NA,
                           'number': number,
                           'number_indexes': number_indexes}
            info_actions.append(action_dict)

    for element in discard_actions:
        actions.append(element)

    for element in play_actions:
        actions.append(element)

    for element in info_actions:
        actions.append(element)

    for index, action in enumerate(actions):
        action['action_number'] = index

    return actions

#adding a random comment