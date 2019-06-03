import pygame as pg

## pygame初始化 ##
pg.init()
## 音樂初始化 ##
#pg.mixer.init()

## 音樂 ##
#pg.mixer.music.load("...")  #括弧為音檔名稱
#pg.mixer.music.play(1,0.0)

## 視窗 ##
width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("BATTLE LINE")

## 背景 ##
bg = pg.Surface(screen.get_size())	#get_size
bg = bg.convert()
bg.fill((255, 255, 255))	#白色

## 插入圖片 ##
#image = pg.image.load("...")	#括弧為圖檔名稱
#image.convert()
#bg.blit(image, (20,10))

## 建立卡牌方格 ##
for i in range(9):
	pg.draw.rect(bg, (255,0,0),[10 + 68*i,150,60,90],2)
	pg.draw.rect(bg, (0,0,255),[10 + 68*i,100,60,90],2)
	pg.draw.rect(bg, (255,255,0),[10 + 68*i,50,60,90],2)
	pg.draw.rect(bg, (0,0,0),[10 + 68*i,250,60,90],2)
	pg.draw.rect(bg, (255,0,0),[10 + 68*i,350,60,90],2)
	pg.draw.rect(bg, (0,0,255),[10 + 68*i,400,60,90],2)
	pg.draw.rect(bg, (255,255,0),[10 + 68*i,450,60,90],2)

pg.draw.rect(bg, (0,0,0),[675,250,60,90],2)

## 插入文字 ##
font = pg.font.SysFont("simhei", 48)
text1 = font.render("Rival", True, (255,0,0), (255,255,255))
text2 = font.render("You", True, (0,0,255), (255,255,255))
bg.blit(text1, (665,150))
bg.blit(text2, (675,425))

## 顯示 ##
screen.blit(bg, (0,0))	#繪製覆蓋整個視窗
pg.display.update()

## 關閉 ##
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
pg.quit() 