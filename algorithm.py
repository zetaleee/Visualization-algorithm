import pygame
from random import randint

gap = 10                        #竖条的间隔
width = 30                      #竖条的宽度
screenSize = (600, 250)         #显示屏幕的尺寸
barXPosition = []               #竖条在坐标轴的位置
Bars = []                       #竖条对象列表

#生成颜色
class color(object):
    @staticmethod
    def RandomColor():
        r,g,b = randint(0,225),randint(0,255),randint(0,255)
        return (r,g,b)
    @staticmethod
    def CalculateColor(self,num):
        pass

class bar(object):
    def __init__(self, n,num,screen,width = 30):
        self.n = n
        self.locationX = barXPosition[n]
        self.locationY = screenSize[1]-50-num
        self.num = num
        self.color = color.RandomColor()
        self.width = width
        self.font = pygame.font.Font(None, 20)
        self.screen = screen

    #绘制竖条及其上方的数字
    def BarDraw(self):
        pygame.draw.rect(self.screen, self.color,
                         ((self.locationX,self.locationY), (self.width, self.num)))
        self.txt = self.font.render("{}".format(self.num), True, self.color)
        self.screen.blit(self.txt, (self.locationX+5,self.locationY-20))

    #移动竖条，flag是用于判断移动方向 True向右 False向左
    def move(self,flag):
        pace = 2    #移动的步长
        #消除移动前的竖条
        pygame.draw.rect(self.screen, (255, 255, 235),
                         ((self.locationX, self.locationY), (self.width, self.num)))
        if flag:
            self.locationX += pace
        else:
            self.locationX -= pace
        # 绘制移动后的竖条
        pygame.draw.rect(self.screen, self.color,
                         ((self.locationX , self.locationY), (self.width, self.num)))

    #交换相邻两个竖条
    def ChangeLocation(self,otherBall):
        #清除当前位置图像与文字
        pygame.draw.rect(self.screen, (255, 255, 235),
                         ((self.locationX, self.locationY-20), (self.width, self.num+20)))
        pygame.draw.rect(otherBall.screen, (255, 255, 235),
                         ((otherBall.locationX, otherBall.locationY - 20), (otherBall.width, otherBall.num + 20)))
        #竖条移动的动画
        for n in range(20):
            self.move(True)
            otherBall.move(False)
            pygame.time.delay(40)
            pygame.display.flip()

        #移动后，重新写上竖条对应的数字
        self.screen.blit(self.txt, (self.locationX + 5, self.locationY - 20))
        otherBall.screen.blit(otherBall.txt, (otherBall.locationX + 5, otherBall.locationY - 20))

        #交换竖条对象在列表的位置，同时交换排位数字
        Bars[self.n],Bars[otherBall.n] =  Bars[otherBall.n],Bars[self.n]
        self.n,otherBall.n = otherBall.n,self.n
        pygame.display.flip()
        pygame.time.delay(200)      #此延时控制排序动画的快慢

#冒泡排序
def algorithm(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - 1 - i):
            if nums[j] > nums[j + 1]:
                Bars[j].ChangeLocation(Bars[j + 1])
                nums[j], nums[j + 1] = nums[j + 1], nums[j]

#计算十二个竖条在轴上的位置
def barX(gap,width,barXs):
        for n in range(12):
            barX = 50 + gap + (gap + width) * n
            barXs.append(barX)

def main():
    nums = []
    pygame.init()
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("算法")                #标题
    screen.fill((255, 255, 235))                     #背景色
    barX(gap,width,barXPosition)                     #计算bar位置并存于barXs
    pygame.draw.aaline(screen,(0,255,0),(50,screenSize[1]-50),
                       (screenSize[0]-50,screenSize[1]-50))  #绘制坐标轴
    pygame.display.flip()
    #生成十二个竖条并绘制
    for n in range(12):
        num = randint(20,160)
        tempBar = bar(n,num,screen)
        tempBar.BarDraw()
        nums.append(num)
        Bars.append(tempBar)
        pygame.time.delay(50)  #此处延时是为了开始时演示动画效果
        pygame.display.flip()

    algorithm(nums)  #排序

    #等待关闭窗口事件
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

if __name__ == "__main__":
    main()