# Battle Line
'''--- Tools ---'''
import random
import time
import pygame as pg
from pygame.locals import QUIT
from pygame.locals import KEYDOWN, KEYUP
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE
import sys
import socket
import pickle

'''--- Server imformation ---'''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]	#自動取得主機IP
print(HOST)
s.close()
# HOST = '10.46.220.195'  #我電腦的IP
PORT = 65432	# Port to listen on (non-privileged ports are > 1023)

'''--- Class ---'''
# 卡牌 Class
class Card():
	## 基本資料 ##
	def __init__(self,color,num):
		self.color = color				# 顏色
		self.number = num				# 數字
	
	## 回傳color
	def getColor(self):
		return self.color

	## 回傳color
	def getNumber(self):
		return self.number
		
	## 顯示卡牌資訊 ##
	def showData(self):	# 回傳值
		return "%s-%02d"%(self.color[0:3],self.number)

# 母牌堆 Class
class Cardpool():
	## 基本資料 ##
	def __init__(self):
		# 建立母牌堆 60張普通卡
		self.cardPile = self.createNew_normal60()
		# 母牌堆洗牌
		random.shuffle(self.cardPile)
		# 已經取出的數量cnt (牌堆剩下 60 - cnt)
		self.used_cnt = 0
		# 訊息提示
		# print("洗牌中...")

	## 牌堆是否有牌 ##
	def has_next(self):
		return self.used_cnt < 60
	
	## 牌堆取出牌 ##
	def get_next(self):
		newCard = self.cardPile[self.used_cnt]
		self.used_cnt += 1
		return newCard
		
	## 建立60張普通牌 ##
	def createNew_normal60(self):
		cardPile = []
		for cl in ['RED','ORANGE','YELLOW','GREEN','BLUE','PURPLE']:
			for nm in range(1,11):
				newCard = Card(cl,nm)
				cardPile.append(newCard)
		return cardPile
		
	## 牌堆進行洗牌 ##
	def shuffleCardPile(self):
		random.shuffle(self.cardPile)

# 玩家手牌Class
class Hands():
	## 基本資料 ##
	def __init__(self,id,cardpile):
		self.id = id
		self.cardHold = []
		self.take7(cardpile)
		
		
	## 抽七張手牌##
	def take7(self,cardpile):
		for i in range(7):
			self.takeCard(cardpile)
	
	## 抽牌(手牌+1) ##
	def takeCard(self,cardpile):
		if cardpile.has_next():
			self.cardHold.append(cardpile.get_next())
		else:	# 沒牌不抽
			pass
		# self.showHold()
		# 重新整理 好看
		self.cardHold = sorted(self.cardHold,key=lambda x:[x.getColor(),x.getNumber()])
		# self.showHold()
		
	## 出牌(手牌-1)
	def throwcard(self,num):	# 回傳卡牌
		card = self.cardHold[num]
		self.cardHold.remove(self.cardHold[num])
		return card
		
	## 檢視手牌 ##
	def showHold(self):
		global bg
		global screen
		global pg
		
		for i in range(len(self.cardHold)):
			card = pg.image.load("C:\\pbc_python\\Battle Line\\cards\\"+self.cardHold[i].showData()+".png")
			card.convert()
			bg.blit(card,(-48+113*i,498))
		screen.blit(bg, (0,0))
		pg.display.update()

# 旗幟 Class
class Flag():
	## 基本資料 ##
	def __init__(self,flagID):
		self.containerA = []
		self.containerB = []
		self.flagID = flagID
		self.winner = 0
	
	## 在A槽放置卡牌 ##
	def placeCard_inA(self,card):
		self.containerA.append(card)
		self.containerA = sorted(self.containerA,key=lambda x:[x.getColor(),x.getNumber()])
		if len(self.containerA)==3 & len(self.containerB)==3:
			self.winner = self.duel('A')
	
	## 在B槽放置卡牌 ##
	def placeCard_inB(self,card):
		self.containerB.append(card)
		self.containerB = sorted(self.containerB,key=lambda x:[x.getColor(),x.getNumber()])
		if len(self.containerA)==3 & len(self.containerB)==3:
			self.winner = self.duel('B')
	
	## 牌組的分數 ##
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
		
	## 比較A槽B槽的分數大小 ##
	def duel(self,lastPlayer):	#判斷誰獲得該棋
		aPoint = self.what_types(self.containerA)
		bPoint = self.what_types(self.containerB)
		if lastPlayer == 'A':
			bPoint += 0.5
		elif lastPlayer == 'B':
			aPoint += 0.5
			
		if aPoint >= bPoint:
			return "A"
		else:
			return "B"

	def showFlag(self):
		
		global bg
		global screen
		global pg
		
		# 旗幟: 已被佔領
		if self.winner == 'A':
			flagGet = pg.image.load("C:\\pbc_python\\Battle Line\\flags\\redflag.png")
			flagGet.convert()
			bg.blit(flagGet,((self.flagID-1)*116,220))	#旗幟座標
			screen.blit(bg, (0,0))
			pg.display.update()
		elif self.winner == 'B':
			flagGet = pg.image.load("C:\\pbc_python\\Battle Line\\flags\\blueflag.png")
			flagGet.convert()
			bg.blit(flagGet,((self.flagID-1)*116,220))	#旗幟座標
			screen.blit(bg, (0,0))
			pg.display.update()
		else :
			pass
		
		
		# 玩家A方 卡牌位置
		counterA=0
		for i in self.containerA:
			card = pg.image.load("C:\\pbc_python\\Battle Line\\cards\\"+i.showData()+".png")
			card.convert()
			bg.blit(card,(-67+(self.flagID-1)*116,-27+counterA*30))
			counterA+=1

		# 玩家B方 卡牌位置
		counterB=0
		for i in self.containerB:
			card = pg.image.load("C:\\pbc_python\\Battle Line\\cards\\"+i.showData()+".png")
			card.convert()
			bg.blit(card,(-67+(self.flagID-1)*116,280+counterB*30))
			counterB+=1
			
		# 輸出所有卡牌 
		screen.blit(bg, (0,0))
		pg.display.update()

# 棋盤 Class
class Board():
	## 基本資料 ##
	def __init__(self):
		# 包含九個旗幟
		self.all_flag = self.buildNew_flag9()
		self.gameWinner = 0
		# 訊息提示
		# print("棋盤初始化...")
		
	## 建立9座新旗幟 ##
	def buildNew_flag9(self):
		flagSeries = []
		for fl in range(1,10):
			newFlag = Flag(fl)
			flagSeries.append(newFlag)
		return flagSeries
	
	## 顯示棋盤 (所有旗幟) ##
	def show_allFlag(self):
		global bg
		global screen
		global pg	

		# 背景: 棋盤
		imageBoard = pg.image.load("C:\\pbc_python\\Battle Line\\Interface\\無功能卡\\遊戲介面_nofunc_forA.png")	#括弧為圖檔名稱		
		# 母牌堆
		imageBack = pg.image.load("C:\\pbc_python\\Battle Line\\cards\\Acardback.png")
		imageBoard.convert()
		imageBack.convert()
		bg.blit(imageBoard, (0,0))
		bg.blit(imageBack, (988,160))
		screen.blit(bg, (0,0))
		pg.display.update()	#進行更新顯示

		for fg in self.all_flag:
			fg.showFlag()	
		
	## 判斷輸贏 ##
	def judge_gameWinner(self):
		aWin = 0
		bWin = 0
		# 一一檢查
		for ck in self.all_flag:
			if ck.winner == 'A':
				aWin += 1
			elif ck.winner == 'B':
				bWin +=1
		# 判斷
		if aWin > 4:
			self.gameWinner = 'A'
		elif bWin > 4:
			self.gameWinner = 'B'
	
	## 顯示贏家 ##
	def showWinner(self):
		return self.gameWinner
		
'''--- Global Pre-Game Function ---'''
# 回合指令 A
def movement_playerA():
	pg.draw.line(bg,(255,0,0),(1060,65),(1190,65),4)
	screen.blit(bg, (0,0))
	pg.display.update()
	global board

	cards_playerA.takeCard(cardPile)									#抽一張牌
	cards_playerA.showHold()											#顯示手牌
	color1 = (0, 0, 0)
	color2 = (255, 10, 10)
	color = [color1] * 8
	running = True
	while running:
		for i in range(len(cards_playerA.cardHold)):	#產生8個方框
			pg.draw.rect(bg, color[i], [44+i*113,570,82,123],3)
		screen.blit(bg, (0,0))
		pg.display.update()
		event = pg.event.wait()	#等待玩家點擊
		# if event.type == pg.KEYDOWN and event.dict['key'] == pg.K_SPACE:	#當空白鍵被按下則跳出
			# running = False
		x, y = pg.mouse.get_pos()
		for i in range(8):
			if event.type == pg.MOUSEBUTTONDOWN and 44+i*113 < x < 126+i*113 and 570 < y < 693:	#選牌
				for i2 in range(8):	#變色
					color[i2] = color1
				color[i] = color2
			if color[i] == color2:
				for j in range(9):					
					if event.type == pg.MOUSEBUTTONDOWN and 25+j*117 < x < 108+j*117 and 46 < y < 231 and len(board.all_flag[j].containerA)<3:	#出牌
						cardTaken = cards_playerA.throwcard(i)				#出一張牌
						board.all_flag[j].placeCard_inA(cardTaken)			#將牌放上場
						running = next_step()
						#### server ####
						send_list = [cardTaken,j]          #要傳出的list
						dataA = pickle.dumps(send_list)
						conn.send(dataA)   
						#### server ####
						
		screen.blit(bg, (0,0))
		pg.display.update()
               
# 回合指令 B
def movement_playerB():
	pg.draw.line(bg,(255,0,0),(1060,533),(1190,533),4)
	screen.blit(bg, (0,0))
	pg.display.update()
	global round
	if round <= 23:                                                    #牌沒了就不抽
		#### server ####
		new_card = [cardPile.get_next()]                               #幫B抽一張牌
		dataA = pickle.dumps(new_card)
		conn.send(dataA)
		#### server ####
	#### server ####
	dataB = conn.recv(1024)                                         #顯示手牌
	decision_B = pickle.loads(dataB)
	cardTaken = decision_B[0] 
	#### server ####
	global board    
	board.all_flag[decision_B[1]].placeCard_inB(cardTaken)            #將牌放上場



def next_step():
	# global running
	running = True
	while running:
		textImage = myfont40.render("PRESS SPACE TO CONTINUE...", True, (255,255,255))
		bg.blit(textImage, (340,500))
		screen.blit(bg, (0,0))
		pg.display.update()
		event = pg.event.wait()	#等待玩家點擊
		if event.type == pg.KEYDOWN and event.dict['key'] == pg.K_SPACE:	#當空白鍵被按下則跳出
			return False

'''--- Pygame Pre-set ---'''
## pygame初始化 ##
pg.init()
## 音樂初始化 ##
pg.mixer.init()
## 使用字型 ##
myfont40 = pg.font.SysFont("arial",40)	#字型、大小
myfont60 = pg.font.SysFont("arial",60)	#字型、大小

## 音樂 ##
#pg.mixer.music.load("...")  #括弧為音檔名稱
#pg.mixer.music.play(-1,0.0)  #括弧(重複次數(-1:無限循環)、開始時間)

## 視窗 ##
screen_size = (1200, 700)
screen = pg.display.set_mode(screen_size, 0, 0)
pg.display.set_caption("BATTLE LINE")

## 背景 ##
bg = pg.Surface(screen.get_size())	#get_size
bg = bg.convert()				#優化(?)
bg.set_alpha(255)				#透明度
bg.fill((0, 0, 0))				#顏色

## 初始畫面 ##
textImage = myfont60.render("BATTLE LINE", True, (255,255,255))
screen.blit(textImage, (440,350))
pg.display.update()
time.sleep(1)
screen.blit(bg, (0,0)) 			#清除繪圖視窗
textImage = myfont60.render("Initialization...", True, (255,255,255))
screen.blit(textImage, (450,350))
pg.display.update()
time.sleep(1)
# 開始視窗
startbk = pg.image.load("C:\\pbc_python\\Battle Line\\Interface\\start.jpg")
startbk.convert()
bg.blit(startbk, (0,0))
screen.blit(bg, (0,0))
pg.display.update()
time.sleep(3)
next_step()
# 規則視窗
rulebk = pg.image.load("C:\\pbc_python\\Battle Line\\Interface\\rule.jpg")
rulebk.convert()
bg.blit(rulebk, (0,0))
screen.blit(bg, (0,0))
pg.display.update()
time.sleep(3)
next_step()
rule2bk = pg.image.load("C:\\pbc_python\\Battle Line\\Interface\\rule2.jpg")
rule2bk.convert()
bg.blit(rule2bk, (0,0))
screen.blit(bg, (0,0))
pg.display.update()
time.sleep(3)
next_step()

'''--- Server Connection ---'''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:         #建立伺服器
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen()
	conn, addr = s.accept()
	'''--- Main Pre-Game ---'''
	# 建立棋盤 (同事建立9座旗幟)
	board = Board()
	board.show_allFlag() 	# 首次檢視棋盤
	next_step()
	#建立卡牌堆(普通)
	cardPile = Cardpool()
	# 發牌
	cards_playerA = Hands('A',cardPile)
	cards_playerB = Hands('B',cardPile)
	#把B的手牌傳給B
	dataA = pickle.dumps(cards_playerB)
	conn.send(dataA)
	# 檢視手牌
	cards_playerA.showHold()
	#當空白鍵被按下則跳出
	next_step()

	'''--- Main In-Game ---'''
	# 執行27回合
	for round in range(1,28):

		## A的回合 ##
		# print("==== Round %02d PlayerA ===="%round)
		board.show_allFlag() 							# 顯示棋盤
		movement_playerA()								# A 下指令
		board.show_allFlag()  							# 顯示棋盤
		conn.send(bytes("over", "utf-8"))
		## 判斷遊戲是否分出勝負
		board.judge_gameWinner()
		if board.showWinner() != 0:
			endbk = pg.image.load("C:\\pbc_python\\Battle Line\\Interface\\end.jpg")
			endbk.convert()
			bg.blit(endbk, (0,0))
			screen.blit(bg, (0,0)) 	
			textImage = myfont60.render("Game Over >> "+board.showWinner()+"Wins !", True, (255,255,255))
			screen.blit(textImage, (440,350))
			pg.display.update()
			break 
		## B的回合 ##
		# print("==== Round %02d PlayerB ===="%round)
		board.show_allFlag()  							# 顯示棋盤
		cards_playerA.showHold()
		# confirm = input("...按下ENTER確認...")		# B 確認開始
		movement_playerB()								# B 下指令
		board.show_allFlag()  							# 顯示棋盤
		#### server ####
		dataB = conn.recv(1024)
		#### server ####
		#	confirm = input("...按下ENTER確認結束回合...")
		#	print()
		## 判斷遊戲是否分出勝負
		board.judge_gameWinner()
		if board.showWinner() != 0:
			endbk = pg.image.load("C:\\pbc_python\\Battle Line\\Interface\\end.jpg")
			endbk.convert()
			bg.blit(endbk, (0,0))
			screen.blit(bg, (0,0)) 	
			textImage = myfont60.render("Game Over >> "+board.showWinner()+"Wins !", True, (255,255,255))
			screen.blit(textImage, (440,350))
			pg.display.update()
			break 

## 關閉 ##
time.sleep(5)

# 結束視窗
# endbk = pg.image.load("C:\\pbc_python\\Battle Line\\Interface\\end.jpg")
# endbk.convert()
# bg.blit(endbk, (0,0))
# screen.blit(bg, (0,0))
# pg.display.update()
# time.sleep(3)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.quit:
           next_step()
pg.quit()



