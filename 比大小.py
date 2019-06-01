import itertools


class Compare(cardboard):	#傳入場面上的牌，兩方的牌面 list[0:30] * 2

	def __init__(self):

		self.acard = cardboard[0:30]
		self.bcard = cardboard[31:60]
		self.win = []
		for i in range(10):
			self.win.append(duel(self.acard[3*i : 3*(i+1)], self.bcard[3*i : 3*(i+1)]))

	def duel(acard, bcard):	#判斷誰獲得該棋

		if what_types(acard) > what_types(bcard):
			return "a"
		else:
			return "b"

	def what_types(combin):	#判斷類型，傳入三張牌，回傳分數

		color = [combin[i].color for i in range(3)]
		number = [combin[i].number for i in range(3)]
		number.sort()
		grade = 0
		if color[0] == color[1] == color[2]:
			grade += 970
		if number[0] + 1 == number[1] and number[1] + 1 == number[2]:
			grade += 100 * number[0]
		if number[0] == number[1] == number[2]:
			grade += 1000
		for i in range(3):
			grade += number[i]
		return grade

	def who_win(self.win):	#判斷誰贏

		who_times = [(k, len(list(v))) for k, v in itertools.groupby(self.win)]
		who = {}
		for i in range(len(who_times)):
			if who_times[i][1] == 3:
				return who_times[i][0]
			if who_times[i][0] not in who:
				who[who_times[i][0]] = 1
			else:
				who[who_times[i][0]] += 1
		if who["a"] > who["b"]:
			return "a"
		else:
			return "b"