import random
from help_functions import *
from print_handling import *

class Game:
    def __init__(self, pl_num):
        self.pl_num = pl_num
        self.player_list = []
        self.deck = Deck()
        self.deck.shuffle()
        self.discards = []
        self.info_tokens = 8
        self.fuse_tokens = 3
        self.action_number = 0
        self.game_finished_status = False
        PLAYER_NAMES = ['Mr. Blonde', 'Mr. Pink', 'Mr. Orange', 'Mr. Brown', 'Mr. White', 'Mr. Blue']
        self.player_names = PLAYER_NAMES[0:pl_num] # self.player_names = random.sample(PLAYER_NAMES, self.pl_num) replace with this when player shuffle is wanted
        self.action_list = []
        # scoreboard
        self.board = {'G': 0,
                      'Y': 0,
                      'B': 0,
                      'W': 0,
                      'R': 0}

        self.score = 0

        for n in range(0, self.pl_num):
            self.player_list.append(Player(self.player_names[n]))
        self.current_player_index = 0
        self.current_player = self.player_list[self.current_player_index]

        for index, pl in enumerate(self.player_list):
            if self.pl_num in [2, 3]:
                for i in range(0, 5):
                    pl.draw(self.deck)
            if self.pl_num in [4, 5]:
                for i in range(0, 4):
                    pl.draw(self.deck)
            pl.assign_player_index(index)

    def increment_action_num(self):
        self.action_number += 1

    def finish_game(self):
        self.game_finished_status = True
        print(f'Length of game was {len(self.action_list)} actions')
        return self.action_list

    def consume_fuse_token(self):
        self.fuse_tokens -= 1
        if self.fuse_tokens == 0:
            self.finish_game()

    def spend_info_token(self):
        self.info_tokens -= 1

    def replenish_info_token(self):
        if self.info_tokens < 8:
            self.info_tokens += 1

    def is_finished(self):
        return self.game_finished_status

    def calc_score(self):
        score = 0
        for key in self.board:
            score += int(self.board[key])
        self.score = score
        return self.score

    def print_score(self):
        for key in self.board:
            print(key, ':', int(self.board[key]))
            self.score += int(self.board[key])
        return self.score

    def next_player(self):
        if self.current_player_index < self.pl_num - 1:
            self.current_player_index += 1
        else:
            self.current_player_index = 0
        self.current_player = self.player_list[self.current_player_index]

    def get_other_player_cards(self):
        other_player_hands = []
        for player in self.player_list:
            hand = []
            if player.player_index != self.current_player_index:
                hand.append(player.return_hand())
                other_player_hands.append(hand)
        return other_player_hands

    def get_game_status(self):
        info_tokens = self.info_tokens
        fuse_tokens = self.fuse_tokens
        own_hand = []
        for card in self.player_list[self.current_player_index].hand:
            own_hand.append(card)
        other_players_hands = []

        for pl, player_index in zip(self.player_list, range(0,self.pl_num)):
            if pl.player_index != self.current_player_index:
                other_players_hands.append((pl.hand, player_index))
        own_hand_knowledge = self.player_list[self.current_player_index].hand_knowledge
        board = self.board

        game_status = {'info_tokens': info_tokens,
                       'fuse_tokens': fuse_tokens,
                       'own_hand': own_hand,
                       'other_player_hands': other_players_hands,
                       'own_hand_knowledge': own_hand_knowledge,
                       'board': board}
        return game_status

    def discard_card(self, action):
        discard_card_index = action['discard_card_index']
        player = self.player_list[self.current_player_index]
        discarded_card = player.discard_card(discard_card_index)
        self.discards.append(discarded_card)

        if len(self.deck.cards) != 0:
            player.draw(self.deck)
        self.replenish_info_token()
        return action


    def give_info(self, action):
        info_receiver_player_index = action['info_receiver_player_index']
        action_type = action['action_type']


        if action_type == 'I-C':
            value = action['color']
            indexes = action['color_indexes']
            player = self.player_list[info_receiver_player_index]
            player.update_hand_knowledge(action_type, value, indexes)
        elif action_type == 'I-N':
            value = action['number']
            indexes = action['number_indexes']
            player = self.player_list[info_receiver_player_index]
            player.update_hand_knowledge(action_type, value, indexes)
        self.spend_info_token()

        return action


    def play_card(self, action):
        play_card_index = action['play_card_index']
        player = self.player_list[self.current_player_index]
        played_card = player.play_card(play_card_index)
        card_color = played_card[0]
        self.board[card_color] += 1
        if len(self.deck.cards) != 0:
            player.draw(self.deck)
        return action


    def add_action_to_action_list(self, action):
        self.action_list.append(action)

    def player_action(self, discard_rate, print_game_status):
        # STATUS:

        action_completed = {}

        blockPrint()

        if print_game_status:

            print(f"{self.current_player.name}'s turn:")
            ck = self.player_list[self.current_player_index].hand_knowledge

            for pl in self.player_list:
                if pl.player_index != self.current_player_index:

                    print(f"{pl.name}'s cards: ", end="")
                    for card in pl.hand:
                        print(card.get_card(), end=" ")
                    print("\n", end="")

            print('BOARD: ', self.board)
            print('INFO TOKENS:', end="")
            for it in range(0,self.info_tokens):
                print('| O ',end="")
            print('|')
            print('FUSE TOKENS:', end="")
            for ft in range(0,self.fuse_tokens):
                print('| X ',end="")
            print('|')

        # GAME STATUS:
        actions = (list_possible_actions(self.get_game_status()))
        # list actions
        # look for play card option

        play_action_index = []
        discard_action_index = []
        info_action_index = []


        for action in actions:

            if action['action_type'] == 'P':
                play_action_index.append(action['action_number'])
            if action['action_type'] == 'D':
                discard_action_index.append(action['action_number'])
            if action['action_type'] == 'I-C' or action['action_type'] == 'I-N':
                info_action_index.append(action['action_number'])



        if play_action_index:
            action = actions[random.choice(play_action_index)]
            action_completed = self.play_card(action)

        elif self.info_tokens == 0:
            action = actions[random.choice(discard_action_index)]
            action_completed = self.discard_card(action)
        elif self.info_tokens > 4:
            action = actions[random.choice(info_action_index)]
            if action['action_type'] == 'I-C':
                action_completed = self.give_info(action)
            elif action['action_type'] == 'I-N':
                action_completed = self.give_info(action)
        else:
            discard_or_give_info = random.choices(['D','I'], weights=[discard_rate, 1-discard_rate])[0]
            if discard_or_give_info == 'D':
                action = actions[random.choice(discard_action_index)]
                action_completed = self.discard_card(action)

            elif discard_or_give_info == 'I': # and info_action_index:
                action = actions[random.choice(info_action_index)]
                if action['action_type'] == 'I-C':
                    action_completed = self.give_info(action)
                elif action['action_type'] == 'I-N':
                    action_completed = self.give_info(action)

            else:
                action_completed = {'action_number': 'ERROR',
                       'action_type': 'ERROR',
                       'action_description':'ERROR',
                       'discard_card_index': 'ERROR',
                       'play_card_index': 'ERROR',
                       'info_receiver_player_index': 'ERROR',
                       'color': 'ERROR',
                       'color_indexes': 'ERROR',
                       'number': 'ERROR',
                       'number_indexes': 'ERROR'}



        self.increment_action_num()


        self.add_action_to_action_list(action_completed)
        self.next_player()


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.player_index = 0
        self.hand_knowledge = []


    def draw(self, deck):
        self.hand.append(deck.draw_card())
        self.hand_knowledge.append('CN')
        return self

    def show_hand(self):
        hand = []
        for card in self.hand:
            hand.append(card.get_card())
        print(self.name)
        print(hand)

    def return_hand(self):
        return self.hand

    def assign_player_index(self, index):
        self.player_index = index

    def discard_card(self, index):
        discarded_card = self.hand[index].get_card()
        self.hand.pop(index)
        self.hand_knowledge.pop(index)
        return discarded_card

    def play_card(self, index):
        played_card = self.hand[index].get_card()
        self.hand.pop(index)
        self.hand_knowledge.pop(index)
        return played_card

    def update_hand_knowledge(self, type, value, indexes):
        new_hk = []

        for index, ck in enumerate(self.hand_knowledge):
            if index not in indexes:
                new_hk.append(ck)
            else:
                new_ck = ck
                if type == 'I-C':
                    new_ck = value + ck[1]
                elif type == 'I-N':
                    new_ck = ck[0] + value
                new_hk.append(new_ck)
        self.hand_knowledge = new_hk






class Card:

    def __init__(self, color, number):
        self.color = color
        self.number = str(number)
        self.full_card = color + str(number)

    def show_card(self):
        print('{}{}'.format(self.color, self.number))

    def get_card(self):
        return self.full_card

    def get_color(self):
        return self.color

    def get_number(self):
        return self.number

    def __eq__(self, other):
        return True if self.get_card() == other.get_card() else False


class Deck:

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for c in ['R', 'G', 'B', 'Y', 'W']:
            for n in [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]:
                self.cards.append(Card(c, n))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()


