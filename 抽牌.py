import random

'''--- Class ---'''

class Cardpool(object):
    def __init__(self):
        self.cards = []
        for c in range(6):
            for i in range(1, 11):
                card = "%c%d" % (chr(ord('A') + c), i)
                self.cards.append(card)
        random.shuffle(self.cards)

        self.used_cnt = 0

    def has_next(self):
        return self.used_cnt < 60

    def get_next(self):
        card = self.cards[self.used_cnt]
        self.used_cnt += 1
        return card

cardpool = Cardpool()