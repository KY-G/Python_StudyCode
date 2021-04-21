#pygame first program
import pygame
from pygame.locals import *
from sys import exit
__author__ = {'name' : 'Hongten',
       'mail' : 'hongtenzone@foxmail.com',
       'QQ'  : '648719819',
       'Version' : '1.0'}
BG_IMAGE = 'E:\MyFile\Picture\python_dabao.PNG'
MOUSE_IMAGE = 'E:\MyFile\Picture\hahaha.PNG'
pygame.init()
#设置窗口的大小
screen = pygame.display.set_mode((500, 500), 0, 32)
pygame.display.set_caption('Hongten\'s First Pygame Program')
bg = pygame.image.load(BG_IMAGE).convert()
mouse_cursor = pygame.image.load(MOUSE_IMAGE).convert_alpha()
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      exit()
  screen.blit(bg, (0, 0))
  #鼠标的x,y坐标
  x, y = pygame.mouse.get_pos()
  #隐藏鼠标
  pygame.mouse.set_visible(False)
  x -= mouse_cursor.get_width() / 2
  y -= mouse_cursor.get_height() / 2
  #用其他图形代替鼠标
  screen.blit(mouse_cursor, (x, y))
  pygame.display.update()