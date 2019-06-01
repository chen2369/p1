import itertools

'''--- Class ---'''
# 比大小 Class
class Compare():	#傳入場面上的牌，兩方的牌面 list[0:30] * 2

	def __init__(self, cardboard):

		self.acard = cardboard[0:27]
		self.bcard = cardboard[27:54]
		self.win = []

	def duel(self, acard, bcard):	#判斷誰獲得該旗幟

		if self.what_types(acard) > self.what_types(bcard):
			return "a"
		else:
			return "b"

	def what_types(self, combin):	#判斷類型，傳入三張牌，回傳分數

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

	def who_get_flag(self):
		for i in range(9):
			com = self.duel(self.acard[3*i : 3*(i+1)], self.bcard[3*i : 3*(i+1)])
			self.win.append(com)
			if i == 9:
				print(self.who_win())
				
	def who_win(self):	#判斷誰贏

		who_times = [(k, len(list(v))) for k, v in itertools.groupby(self.win)]
		who = {"a" : 0, "b" : 1}
		for i in range(len(who_times)):
			if who_times[i][1] == 3:
				return who_times[i][0]
			else:
				who[who_times[i][0]] += 1
		if who['a'] > who['b']:
			return "a"
		else:
			return "b"


cardboard = [...]
winner = Compare(cardboard)
winner.who_win()