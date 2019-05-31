'''---class---'''
# 卡牌Class
'''---Class---'''
# 卡牌Class
class Card():
	def __init__(self,color,num):
		self.color = color
		self.number = num
	
	def showData(self):
		print("%s-%02d"%(self.color[0:3],self.number))

'''---Main---'''
#建立卡牌堆(普通)
cardPile = []
for cl in ['RED','ORANGE','YELLOW','GREEN','BLUE','PURPLE']:
	for nm in range(1,11):
		newCard = Card(cl,nm)
		cardPile.append(newCard)

for cd in cardPile:
	cd.showData()
