# Battle Line

'''--- Class ---'''
# 卡牌 Class
class Card():
	def __init__(self,color,num):
		self.color = color
		self.number = num

	def showData(self):
		return "%s-%02d"%(self.color[0:3],self.number)

# 旗幟槽位
class Flag():
	def __init__(self,flagID):
		self.countainerA = []
		self.countainerB = []
		self.flagID = 'FLAG-'+str(flagID)

	def placeCard_inA(self,card):
		self.countainerA.append(card)

	def placeCard_inB(self,card):
		self.countainerB.append(card)

	def showFlag(self):

		# print('####',end='')
		# 玩家A方 卡牌位置
		for i in self.countainerA:
			print('|',i.showData(),'|',sep='',end='')
		if len(self.countainerA)==3:
			pass
		else:
			for i2 in range(3-len(self.countainerA)):
				print('|      |',sep='',end='')
		# 旗幟id
		print('[',self.flagID,']',sep = '',end = '')
		# 玩家B方 卡牌位置
		for j in self.countainerB:
			print('|',j.showData(),'|',sep='',end='')
		if len(self.countainerB)==3:
			pass
		else:
			for j2 in range(3-len(self.countainerB)):
				print('|      |',sep='',end='')
		# print('####',end='')
		print()

'''--- Main Pre-Game ---'''
#建立卡牌堆(普通)
cardPile = []
for cl in ['RED','ORANGE','YELLOW','GREEN','BLUE','PURPLE']:
	for nm in range(1,11):
		newCard = Card(cl,nm)
		cardPile.append(newCard)

# 檢查牌堆 60張
# for cd in cardPile:
	# print(cd.showData())

# 建立旗幟槽位
flagSeries = []
for fl in range(1,10):
	newFlag = Flag(fl)
	flagSeries.append(newFlag)

# 測試 加入牌
flagSeries[0].placeCard_inA(cardPile[1])
flagSeries[0].placeCard_inA(cardPile[6])
flagSeries[3].placeCard_inB(cardPile[32])
flagSeries[2].placeCard_inA(cardPile[22])
flagSeries[7].placeCard_inB(cardPile[19])
flagSeries[7].placeCard_inB(cardPile[12])
flagSeries[7].placeCard_inB(cardPile[33])

# 檢查旗幟 9面
for fg in flagSeries:
	fg.showFlag()
