import random

class Card():
	def __init__(self,color,num):
		self.color = color
		self.number = num

	def showData(self):
		return "%s-%02d"%(self.color[0:3],self.number)

'''--- Class ---'''

class Cardpool(object):
    def __init__(self):
        self.cardPile = []
        for cl in ['RED','ORANGE','YELLOW','GREEN','BLUE','PURPLE']:
            for nm in range(1, 11):
                newCard = Card(cl, nm)
                self.cardPile.append(newCard)

        random.shuffle(self.cardPile)

        self.used_cnt = 0

    def has_next(self):
        return self.used_cnt < 60

    def get_next(self):
        newCard = self.cardPile[self.used_cnt]
        self.used_cnt += 1
        return newCard

cardpool = Cardpool()