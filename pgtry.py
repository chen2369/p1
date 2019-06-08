import pygame as pg
from pygame.locals import QUIT
from pygame.locals import KEYDOWN, KEYUP
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE
import sys
import time

## pygame初始化 ##
pg.init()
## 音樂初始化 ##
pg.mixer.init()

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
myfont = pg.font.SysFont("arial",60)	#字型、大小
textImage = myfont.render("BATTLE LINE", True, (255,255,255))
screen.blit(textImage, (440,350))
pg.display.update()
time.sleep(1)
screen.blit(bg, (0,0)) 			#清除繪圖視窗
textImage = myfont.render("Initialization...", True, (255,255,255))
screen.blit(textImage, (450,350))
pg.display.update()
time.sleep(1)

## 插入 ##
image = pg.image.load("C:\\Users\\chen8\\Desktop\\遊戲介面_nofunc_forA.png")	#括弧為圖檔名稱
image1 = pg.image.load("C:\\Users\\chen8\\Desktop\\card\\Acardback.png")
image.convert()
image1.convert()
bg.blit(image, (0,0))
bg.blit(image1, (988,160))
screen.blit(bg, (0,0))
pg.display.update()

card0 = pg.image.load("C:\\Users\\chen8\\Desktop\\card\\RED-01.png")
card0.convert()
bg.blit(card0, (-48,498))
card1 = pg.image.load("C:\\Users\\chen8\\Desktop\\card\\BLU-01.png")
card1.convert()
bg.blit(card1, (66,498))
screen.blit(bg, (0,0))
pg.display.update()

running = True
change_color = True  # 控制方塊颜色
while running:
	for event in pg.event.get():
		if event.type == pg.KEYDOWN and event.dict['key'] == pg.K_SPACE:		#當空白鍵被按下則跳出
			running = False
		x, y = pg.mouse.get_pos()
		if event.type == pg.MOUSEBUTTONDOWN and 44 < x < 126 and 570 < y < 693:		#選牌
			change_color = not change_color
		elif event.type == pg.MOUSEBUTTONDOWN and 25 < x < 115 and 355 < y < 540 and color == (255, 10, 10):	#出牌
			bg.blit(card0, (-65,282))
			screen.blit(bg, (0,0))
			pg.display.update()
			
		color = None
	if change_color:
		color = (10, 10, 255)
	else:
		color = (255, 10, 10)
	pg.draw.rect(bg, color, [44,570,82,123],3)
	screen.blit(bg, (0,0))
	pg.display.update()


## 建立卡牌方格 ##
#for i in range(9):
#	pg.draw.rect(bg, (255,0,0),[10 + 68*i,150,60,90],2)
#	pg.draw.rect(bg, (0,0,255),[10 + 68*i,100,60,90],2)
#	pg.draw.rect(bg, (255,255,0),[10 + 68*i,50,60,90],2)
#	pg.draw.rect(bg, (0,0,0),[10 + 68*i,250,60,90],2)
#	pg.draw.rect(bg, (255,0,0),[10 + 68*i,350,60,90],2)
#	pg.draw.rect(bg, (0,0,255),[10 + 68*i,400,60,90],2)
#	pg.draw.rect(bg, (255,255,0),[10 + 68*i,450,60,90],2)
#pg.draw.rect(bg, (0,0,0),[675,250,60,90],2)

## 插入文字 ##
#font = pg.font.SysFont("simhei", 40)
#text1 = font.render("PLAYER B", True, (255,0,0), (0,255,255))
#text2 = font.render("PLAYER A", True, (0,0,255), (0,255,255))
#bg.blit(text1, (638,150))
#bg.blit(text2, (638,425))

## 顯示 ##
#screen.blit(bg, (0,0))	#繪製覆蓋整個視窗
#pg.display.update()

## 球建立 ##
#for i in range(7):
#	card = pg.Surface((60,90))     #建立球矩形繪圖區
#	card.fill((0,0,255))       #矩形區塊背景為白色
#	pg.draw.rect(card, (0,0,255), [800,450,60,90], 0)  #畫藍色球
#	rect = card.get_rect()         #取得球矩形區塊
#	rect.center = (600,450)        #球起始位置
#	x, y = rect.topleft            #球左上角坐標
#	speed = 9                      #球運動速度
#	clock = pg.time.Clock()        #建立時間元件
#
#	#關閉程式的程式碼
#	running = True
#	while running:
#		clock.tick(30)        #每秒執行30次
#		for event in pg.event.get():
#			if event.type == pg.quit():
#				running = False
#				pg.quit()
#		x -= speed                 #改變水平位置
#		y += speed / 2             #改變垂直位置
#		rect.center = (x,y)        #坐標差異讓它移動
#		if(rect.left <= 200):   #到達左右邊界
#			speed = 0            #正負值交換
#		screen.blit(bg, (0,0))
#		screen.blit(card, rect.topleft)  #繪製藍球
#		pg.display.update()     #更新視窗
		


## 操作鍵盤 ##
#x, y = 0, 0
#move = {K_LEFT:0, K_RIGHT:0, K_UP:0, K_DOWN:0}
# 
#while True:
#
#    for event in pg.event.get():
#        if event.type == KEYDOWN:
#            if event.key in move:
#                move[event.key] = 1
#        elif event.type == KEYUP:
#            if event.key in move:
#                move[event.key] = 0
#    
#    x -= move[K_LEFT]
#    x += move[K_RIGHT]
#    y -= move[K_UP]
#    y += move[K_DOWN]
#    screen.fill((255,255,255))
#    screen.blit(bg, (x, y))
#    pg.display.update()

## 旗幟 ##
A = True
if A:
	flag1 = pg.image.load("C:\\Users\\chen8\\Desktop\\redflag.png")
	flag1.convert()
	bg.blit(flag1, (0,221))
	screen.blit(bg, (0,0))
	pg.display.update()

## 關閉 ##
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.quit:
            running = False
pg.quit()