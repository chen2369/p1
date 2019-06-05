
'''--- Tools ---'''
import random
import time
import socket
import pickle

'''--- Server Information ---'''
HOST = '10.46.220.195'  # The server's hostname or IP address
PORT = 65432            # The port used by the server

'''--- Class ---'''
# 卡牌 Class
class Card():
    ## 基本資料 ##
    def __init__(self,color,num):
        self.color = color                # 顏色
        self.number = num                # 數字
    
    ## 回傳color
    def getColor(self):
        return self.color

    ## 回傳color
    def getNumber(self):
        return self.number
        
    ## 顯示卡牌資訊 ##
    def showData(self):    # 回傳值
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
        print("洗牌中...")

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
        else:    # 沒牌不抽
            pass
        # self.showHold()
        # 重新整理 好看
        self.cardHold = sorted(self.cardHold,key=lambda x:[x.getColor(),x.getNumber()])
        # self.showHold()
        
    ## 出牌(手牌-1)
    def throwcard(self,num):    # 回傳卡牌
        card = self.cardHold[num-1]
        self.cardHold.remove(self.cardHold[num-1])
        return card
        
    ## 檢視手牌 ##
    def showHold(self):
        print("Player",self.id,"-Card List :",sep='')
        # 每張手牌
        for i in range(len(self.cardHold)):
            print('<',self.cardHold[i].showData(),sep='',end='> ')
        print()
        

# 旗幟 Class
class Flag():
    ## 基本資料 ##
    def __init__(self,flagID):
        self.containerA = []
        self.containerB = []
        self.flagID = 'FLAG-'+str(flagID)
        self.winner = 0
    
    ## 在A槽放置卡牌 ##
    def placeCard_inA(self,card):
        self.containerA.append(card)
        if len(self.containerA)==3 & len(self.containerB)==3:
            self.winner = self.duel()
    
    ## 在B槽放置卡牌 ##
    def placeCard_inB(self,card):
        self.containerB.append(card)
        if len(self.containerA)==3 & len(self.containerB)==3:
            self.winner = self.duel()
    
    ## 牌組的分數 ##
    def what_types(self, combin):    #判斷類型，傳入三張牌，回傳分數

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
    def duel(self):    #判斷誰獲得該棋
        if self.what_types(self.containerA) > self.what_types(self.containerB):
            return "A"
        else:
            return "B"

    def showFlag(self):
        
        # 已被佔領
        if self.winner == 'A':
            mid = 'A佔領 '
        elif self.winner == 'B':
            mid = 'B佔領 '
        else :
            mid = self.flagID
        
        # print('####',end='')
        # 玩家A方 卡牌位置
        for i in self.containerA:
            print('|',i.showData(),'|',sep='',end='')
        if len(self.containerA)==3:
            pass
        else:
            for i2 in range(3-len(self.containerA)):
                print('|      |',sep='',end='')
        # 旗幟id
        print(']',mid,'[',sep = '',end = '')
        # 玩家B方 卡牌位置
        for j in self.containerB:
            print('|',j.showData(),'|',sep='',end='')
        if len(self.containerB)==3:
            pass
        else:
            for j2 in range(3-len(self.containerB)):
                print('|      |',sep='',end='')
        # print('####',end='')
        print()

# 棋盤 Class
class Board():
    ## 基本資料 ##
    def __init__(self):
        # 包含九個旗幟
        self.all_flag = self.buildNew_flag9()
        self.gameWinner = 0
        # 訊息提示
        print("棋盤初始化...")
        
    ## 建立9座新旗幟 ##
    def buildNew_flag9(self):
        flagSeries = []
        for fl in range(1,10):
            newFlag = Flag(fl)
            flagSeries.append(newFlag)
        return flagSeries
    
    ## 顯示棋盤 (所有旗幟) ##
    def show_allFlag(self):
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
    dataA = s.recv(1024) #接收A的出牌選擇
    
    decision_A = pickle.loads(dataA)
    #print(decision_A)
    cardTaken = decision_A[0]                                           
    global board    
    board.all_flag[decision_A[1]].placeCard_inA(cardTaken)                              #將牌放上場
    
# 回合指令 B
def movement_playerB():
    global round
    if round <= 23:                                           #牌沒了就不抽
        dataA = s.recv(1024)                                  #A幫忙抽一張牌
        new_card = pickle.loads(dataA)
        cards_playerB.cardHold.append(new_card[0])
    cards_playerB.showHold()                                            #顯示手牌
    command = input("輸入指令(如格式): 卡牌編號,旗幟位置\t").split(',')
    print()
    global board
    cardTaken = cards_playerB.throwcard(int(command[0]))                #出一張牌
    send_list = [cardTaken, int(command[1])-1]          #要傳出的list
    dataB = pickle.dumps(send_list)
    s.send(dataB)
        
    board.all_flag[int(command[1])-1].placeCard_inB(cardTaken)    
    #將牌放上場
'''--- Server Connection ---'''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    '''--- Main Pre-Game ---'''    
    # 建立棋盤 (同事建立9座旗幟)
    board = Board()
    time.sleep(3)
    board.show_allFlag()     # 首次檢視棋盤
    time.sleep(1)
    #接收手牌
    dataA = s.recv(1024)
    cards_playerB = pickle.loads(dataA)
    # 檢視手牌
    print("==== PlayerB ====")
    confirm = input("...按下ENTER確認手牌...")
    print()
    cards_playerB.showHold()
    confirm = input("...按下ENTER確認開始...")
    print()
    
    
    '''--- Main In-Game ---'''
    # 執行27回合
    
    for round in range(1,28):
        ## A的回合 ##
        print("==== Round %02d PlayerA ===="%round)
        board.show_allFlag()                             # 顯示棋盤
        # confirm = input("...按下ENTER確認...")        # A 確認開始
        movement_playerA()                                # A 下指令
        board.show_allFlag()                              # 顯示棋盤
        time.sleep(0.5)
        dataA = s.recv(1024)
        ## 判斷遊戲是否分出勝負
        board.judge_gameWinner()
        if board.showWinner() != 0:
            print("Game Over >> ",board.showWinner(),"Wins !") 
            break
        ## B的回合 ##
        print("==== Round %02d PlayerB ===="%round)
        board.show_allFlag()                              # 顯示棋盤
        # confirm = input("...按下ENTER確認...")        # B 確認開始
        movement_playerB()                                # B 下指令
        board.show_allFlag()                              # 顯示棋盤
        time.sleep(0.5)
        confirm = input("...按下ENTER確認結束回合...")
        s.send(bytes("over", "utf-8"))
        print()
        ## 判斷遊戲是否分出勝負
        board.judge_gameWinner()
        if board.showWinner() != 0:
            print("Game Over >> ",board.showWinner(),"Wins !") 
            break

# 判斷輸贏
# board.judge_gameWinner()
# print("Game Over >> ",board.showWinner(),"Wins !")


'''------'''

'''------'''
