import pygame
import os, sys
from random import choice

pygame.init()
size = 1000, 1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Нарды")
color = pygame.Color('white')
posic1 = 0
posic2 = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

class Board: #Задание игрового поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        global beliy
        beliy = [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 2]
        global cherniy
        cherniy = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0,
                   5, 0, 0, 0, 0, 0]

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, color,
                                 (i * self.cell_size + self.left,
                                  j * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def hod(self, kletk, cvet, kub): #Проверяет можно ли встать на выбранную клетку
        f = kub != 0
        if cvet == 0:
            if not(kletk - kub - 1 >= 24):
                f1 = cherniy[kletk - kub - 1] <= 1
            else:
                f1 = True
            if (kletk - kub - 1 >= 0) and f1 and f:
                return True
            else:
                return False
        else:
            if not(kletk + kub - 1 >= 24):
                f1 = beliy[kletk + kub - 1] <= 1
            else:
                f1 = True
            if (kletk + kub - 1 < 24) and f1 and f:
                return True
            else:
                return False

    def poed(self, kletk, cvet, kub): #Можно ли съесть фишку (можно, если она одна в клетке и другого цвета)
        global posic1
        global posic2
        if cvet == 0:
            if (cherniy[kletk - kub - 1] == 1) and (posic1 - 1 <= 8):
                posic1 += 1
                cherniy[kletk - kub - 1] -= 1
                return True
            else:
                return False
        else:
            if (beliy[kletk + kub - 1] == 1) and (posic2 - 1 <= 8):
                posic2 += 1
                beliy[kletk + kub - 1] -= 1
                return True
            else:
                return False

    def vozvrat(self, kletk, cvet, kub): #Опция возврата для съеденных фишек
        global posic1
        global posic2
        if cvet == 0:
            if kletk != 25:
                beliy[kletk - 1] -= 1
            else:
                posic2 -= 1
            beliy[kletk - kub - 1] += 1
            return (beliy[kletk - kub - 1] - 1)
        else:
            if kletk != 0:
                cherniy[kletk - 1] -= 1
            else:
                posic1 -= 1
            cherniy[kletk + kub - 1] += 1
            return (cherniy[kletk + kub - 1] - 1)

    def spis(self, kletk, a, cvet, kub): #Проверяет корректность хода с перепрыгивание на другую сторону доски
        if a == 0:
            if cvet == 0:
                return (beliy[kletk - 1] - 1)
            else:
                return (cherniy[kletk - 1] - 1)
        else:
            if cvet == 0:
                if ((kletk - kub - 1) >= 0) and (kub != 0):
                    m = (beliy[kletk - kub - 1] + 1) < 8
                else:
                    return False
                if m:
                    return True
                else:
                    return False
            else:
                if ((kletk + kub - 1) < 24) and (kub != 0):
                    m = (cherniy[kletk + kub - 1] + 1) < 8
                else:
                    return False
                if m:
                    return True
                else:
                    return False

    def return_posic(self, cvet):  #когда съеденная фишка она возвращается на середину доски с верхней/нижней стороны в зависимости от цвета
        if cvet == 1:
            return posic1
        else:
            return posic2


class Beliy(pygame.sprite.Sprite): 
    image = pygame.image.load("beliy.png")

    def __init__(self, x, rasp, kletk):
        super().__init__(all_sprites2)
        self.image = Beliy.image
        self.rect = self.image.get_rect()
        self.x = x[0]
        self.y = x[1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.f = False
        self.rasp = rasp
        self.kletk = kletk
        self.perehod = False
        self.cvet = 0
        self.kub1 = 0
        self.kub2 = 0

    def cifri_s_kubika(self, kub1, kub2):
        self.kub1 = kub1
        self.kub2 = kub2

    def nagat(self, event): #при зажатой клавише - шашка едет за курсором
        k = Board.spis(self, self.kletk, 1, self.cvet, self.kub1)
        k1 = Board.spis(self, self.kletk, 1, self.cvet, self.kub2)
        if self.kletk != 25:
            s = Board.spis(self, self.kletk, 0, self.cvet, 0)
            s1 = (42 + 62 * s)
            s2 = (910 - 62 * s)
        else:
            posic = Board.return_posic(self, self.cvet)
            s1 = 42 + 62 * (posic - 1)
        if self.rect.collidepoint(event.pos):
            if self.rasp == 1:
                if (self.rect.y == s1) and (k or k1):
                    self.f = True
            else:
                if (self.rect.y == s2) and (k or k1):
                    self.f = True

    def on_board(self, event):
        if self.f:
            self.rect.x = event.pos[0] - 20
            self.rect.y = event.pos[1] - 20

    def otgat(self): #проверяет, может ли шашка встать на позицию, над которой была отжата мышь,меняя значение hod_prois
        perviy = Board.hod(self, self.kletk, self.cvet, self.kub1)
        vtoroy = Board.hod(self, self.kletk, self.cvet, self.kub2)
        self.perviy1 = False
        self.vtoroy1 = False
        self.hod_prois = False
        self.poed = False
        if self.rasp == 1:
            if perviy:
                a1 = self.x - 62 * self.kub1
                if (self.kletk >= 19) and (self.kletk - self.kub1 < 19):
                    a1 -= 90
                m = 42 <= self.rect.y <= 476
                if (self.kletk >= 13) and (self.kletk - self.kub1 < 13):
                    a1 = 84 + abs(62 * (self.kletk - self.kub1 - 12))
                    m = 538 <= self.rect.y <= 910
                if self.kletk == 25:
                    a1 = 918 - 62 * self.kub1
                t = a1 - 61 <= self.rect.x < a1 + 62
                if t and m:
                    self.perviy1 = True
                    hod = Board.vozvrat(self, self.kletk, self.cvet, self.kub1)
                    self.poed = Board.poed(self, self.kletk, self.cvet,
                                           self.kub1)
                    self.kletk -= self.kub1
                    self.x = a1
                    self.y = hod * 62 + 42
                    if (self.kletk + self.kub1 >= 13) and (self.kletk < 13):
                        self.y = 910 - hod * 62
                        self.rasp = 0
            if vtoroy and not(self.perviy1):
                a1 = self.x - 62 * self.kub2
                if (self.kletk >= 19) and (self.kletk - self.kub2 < 19):
                    a1 -= 90
                m = 42 <= self.rect.y <= 476
                if (self.kletk >= 13) and (self.kletk - self.kub2 < 13):
                    a1 = 84 + abs(62 * (self.kletk - self.kub2 - 12))
                    m = 538 <= self.rect.y <= 910
                if self.kletk == 25:
                    a1 = 918 - 62 * self.kub2
                t = a1 - 61 <= self.rect.x < a1 + 62
                if t and m:
                    self.vtoroy1 = True
                    hod = Board.vozvrat(self, self.kletk, self.cvet, self.kub2)
                    self.poed = Board.poed(self, self.kletk, self.cvet,
                                           self.kub2)
                    self.kletk -= self.kub2
                    self.x = a1
                    self.y = hod * 62 + 42
                    if (self.kletk + self.kub2 >= 13) and (self.kletk < 13):
                        self.y = 910 - hod * 62
                        self.rasp = 0
        else:
            if perviy:
                a1 = self.x + 62 * self.kub1
                if (self.kletk >= 7) and (self.kletk - self.kub1 < 7):
                    a1 += 90
                t = a1 - 61 <= self.rect.x < a1 + 62
                m = 538 <= self.rect.y <= 910
                if t and m:
                    self.perviy1 = True
                    hod = Board.vozvrat(self, self.kletk, self.cvet, self.kub1)
                    self.poed = Board.poed(self, self.kletk, self.cvet,
                                           self.kub1)
                    self.kletk -= self.kub1
                    self.x = a1
                    self.y = 910 - hod * 62
            if vtoroy and not(self.perviy1):
                a1 = self.x + 62 * self.kub2
                if (self.kletk >= 7) and (self.kletk - self.kub2 < 7):
                    a1 += 90
                t = a1 - 61 <= self.rect.x < a1 + 62
                m = 538 <= self.rect.y <= 910
                if t and m:
                    self.vtoroy1 = True
                    hod = Board.vozvrat(self, self.kletk, self.cvet, self.kub2)
                    self.poed = Board.poed(self, self.kletk, self.cvet,
                                           self.kub2)
                    self.kletk -= self.kub2
                    self.x = a1
                    self.y = 910 - hod * 62

        if self.kub1 == 0 and self.kub2 == 0:
            self.hod_prois = True
        self.rect.topleft = self.x, self.y
        self.f = False

    def odin_hod(self):
        if self.perviy1 or self.vtoroy1:
            if self.perviy1:
                return 1
            elif self.vtoroy1:
                return 2
        else:
            return 3

    def poed_fish(self):
        return self.poed #"Съеден ли я"

    def return_kletk(self):
        if self.poed:
            return self.kletk

    def perenos(self, kletk_perenos): #Совершает перенос между сторонами доска
        if self.kletk == kletk_perenos:
            posic = Board.return_posic(self, self.cvet)
            self.rasp = 1
            self.kletk = 25
            self.x = 472
            self.y = 42 + 62 * (posic - 1)
            self.rect.topleft = self.x, self.y

    def game_process(self):
        return self.hod_prois #глядим на возмоность ходов


class Cherniy(pygame.sprite.Sprite):
    image = pygame.image.load("cherniy.png")

    def __init__(self, x, rasp, kletk):
        super().__init__(all_sprites3)
        self.image = Cherniy.image
        self.rect = self.image.get_rect()
        self.x = x[0]
        self.y = x[1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.f = False
        self.rasp = rasp
        self.kletk = kletk
        self.cvet = 1

    def cifri_s_kubika(self, kub1, kub2): #возвращает рандомные значения
        self.kub1 = kub1
        self.kub2 = kub2

    def nagat(self, event):
        s = Board.spis(self, self.kletk, 0, self.cvet, 0)
        k = Board.spis(self, self.kletk, 1, self.cvet, self.kub1)
        k1 = Board.spis(self, self.kletk, 1, self.cvet, self.kub2)
        if self.kletk != 0:
            s = Board.spis(self, self.kletk, 0, self.cvet, 0)
            s1 = (42 + 62 * s)
            s2 = (910 - 62 * s)
        else:
            posic = Board.return_posic(self, self.cvet)
            s2 = 910 - 62 * (posic - 1)
        if self.rect.collidepoint(event.pos):
            if self.rasp == 1:
                if (self.rect.y == s1) and (k or k1):
                    self.f = True
            else:
                if (self.rect.y == s2) and (k or k1):
                    self.f = True

    def on_board(self, event):
        if self.f:
            self.rect.x = event.pos[0] - 20
            self.rect.y = event.pos[1] - 20

    def otgat(self):
        perviy = Board.hod(self, self.kletk, self.cvet, self.kub1)
        vtoroy = Board.hod(self, self.kletk, self.cvet, self.kub2)
        self.perviy1 = False
        self.vtoroy1 = False
        self.hod_prois = False
        self.poed = False
        if self.rasp == 1:
            if perviy:
                a1 = self.x + 62 * self.kub1
                if (self.kletk <= 18) and (self.kletk + self.kub1 > 18):
                    a1 += 90
                t = a1 - 61 <= self.rect.x < a1 + 62
                m = 42 <= self.rect.y <= 476
                if t and m:
                    self.perviy1 = True
                    hod = Board.vozvrat(self, self.kletk, self.cvet, self.kub1)
                    self.poed = Board.poed(self, self.kletk, self.cvet,
                                           self.kub1)
                    self.kletk += self.kub1
                    self.x = a1
                    self.y = hod * 62 + 42
            if vtoroy and not(self.perviy1):
                a1 = self.x + 62 * self.kub2
                if (self.kletk <= 18) and (self.kletk + self.kub2 > 18):
                    a1 += 90
                t = a1 - 61 <= self.rect.x < a1 + 62
                m = 42 <= self.rect.y <= 476
                if t and m:
                    self.vtoroy1 = True
                    hod = Board.vozvrat(self, self.kletk, self.cvet, self.kub2)
                    self.poed = Board.poed(self, self.kletk, self.cvet,
                                           self.kub2)
                    self.kletk += self.kub2
                    self.x = a1
                    self.y = hod * 62 + 42
                else:
                    if self.kletk == 12:
                        self.rasp = 0
        else:
            if perviy:
                a1 = self.x - 62 * self.kub1
                if (self.kletk <= 6) and (self.kletk + self.kub1 > 6):
                    a1 -= 90
                m = 538 <= self.rect.y <= 910
                if (self.kletk <= 12) and (self.kletk + self.kub1 > 12):
                    a1 = 84 + abs(62 * (self.kletk + self.kub1 - 13))
                    m = 42 <= self.rect.y <= 476
                if self.kletk == 0:
                    a1 = 918 - 62 * self.kub1
                t = a1 - 61 <= self.rect.x < a1 + 62
                if t and m:
                    self.perviy1 = True
                    hod = Board.vozvrat(self, self.kletk, self.cvet, self.kub1)
                    self.poed = Board.poed(self, self.kletk, self.cvet,
                                           self.kub1)
                    self.kletk += self.kub1
                    self.x = a1
                    self.y = 910 - hod * 62
                    if (self.kletk - self.kub1 <= 12) and (self.kletk > 12):
                        self.y = hod * 62 + 42
                        self.rasp = 1
            if vtoroy and not(self.perviy1):
                a1 = self.x - 62 * self.kub2
                if (self.kletk <= 6) and (self.kletk + self.kub2 > 6):
                    a1 -= 90
                m = 538 <= self.rect.y <= 910
                if (self.kletk <= 12) and (self.kletk + self.kub2 > 12):
                    a1 = 84 + abs(62 * (self.kletk + self.kub2 - 13))
                    m = 42 <= self.rect.y <= 476
                if self.kletk == 0:
                    a1 = 918 - 62 * self.kub2
                t = a1 - 61 <= self.rect.x < a1 + 62
                if t and m:
                    self.vtoroy1 = True
                    hod = Board.vozvrat(self, self.kletk, self.cvet, self.kub2)
                    self.poed = Board.poed(self, self.kletk, self.cvet,
                                           self.kub2)
                    self.kletk += self.kub2
                    self.x = a1
                    self.y = 910 - hod * 62
                    if (self.kletk - self.kub2 <= 12) and (self.kletk > 12):
                        self.y = hod * 62 + 42
                        self.rasp = 1

        if self.kub1 == 0 and self.kub2 == 0:
            self.hod_prois = True
        self.rect.topleft = self.x, self.y
        self.f = False

    def odin_hod(self):
        if self.perviy1 or self.vtoroy1:
            if self.perviy1:
                return 1
            elif self.vtoroy1:
                return 2
        else:
            return 3

    def poed_fish(self):
        return self.poed

    def return_kletk(self):
        if self.poed:
            return self.kletk

    def perenos(self, kletk_perenos):
        if self.kletk == kletk_perenos:
            posic = Board.return_posic(self, self.cvet)
            self.rasp = 0
            self.kletk = 0
            self.x = 472
            self.y = 910 - 62 * (posic - 1)
            self.rect.topleft = self.x, self.y

    def game_process(self):
        return self.hod_prois


class arrow(pygame.sprite.Sprite):
    image = pygame.image.load("arrow.png")

    def __init__(self):
        super().__init__(all_sprites1)
        self.image = arrow.image
        self.rect = self.image.get_rect()

    def cursor(self, event):
        self.rect.topleft = event.pos


class kubik:
    def __init__(self, a, b, cvet):
        self.a = a
        self.b = b
        self.cvet = cvet

    def brosok(self):    #Два рандомных числа и их отображение на, прости господи, "кубиках"
        if self.cvet == 0:
            a1 = 239
            b1 = 302
        else:
            a1 = 701
            b1 = 764
        if self.a == 1:
            pygame.draw.circle(screen, pygame.Color("black"), [a1, 507], 7)

        elif self.a == 2:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)

        elif self.a == 3:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"), [a1, 507], 7)

        elif self.a == 4:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 527], 7)

        elif self.a == 5:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1, 507], 7)

        elif self.a == 6:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 507], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 507], 7)

        if self.b == 1:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1, 507], 7)

        elif self.b == 2:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)

        elif self.b == 3:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1, 507], 7)

        elif self.b == 4:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 487], 7)

        elif self.b == 5:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1, 507], 7)

        elif self.b == 6:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 507], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 507], 7)


all_sprites = pygame.sprite.Group()
all_sprites1 = pygame.sprite.Group()
all_sprites2 = pygame.sprite.Group()
all_sprites3 = pygame.sprite.Group()

sprite_image = pygame.image.load("pole.jpg")
sprite = pygame.sprite.Sprite(all_sprites)
sprite.image = sprite_image
sprite.rect = sprite.image.get_rect()


fishki = pygame.image.load("fishki.png") #изначальные координаты шашек
pygame.display.set_icon(fishki)
shashkab1 = Beliy((84, 42), 1, 13)
shashkab2 = Beliy((84, 104), 1, 13)
shashkab3 = Beliy((84, 166), 1, 13)
shashkab4 = Beliy((84, 228), 1, 13)
shashkab5 = Beliy((84, 290), 1, 13)
shashkab6 = Beliy((332, 910), 0, 8)
shashkab7 = Beliy((332, 848), 0, 8)
shashkab8 = Beliy((332, 786), 0, 8)
shashkab9 = Beliy((546, 910), 0, 6)
shashkab10 = Beliy((546, 848), 0, 6)
shashkab11 = Beliy((546, 786), 0, 6)
shashkab12 = Beliy((546, 724), 0, 6)
shashkab13 = Beliy((546, 662), 0, 6)
shashkab14 = Beliy((856, 42), 1, 24)
shashkab15 = Beliy((856, 104), 1, 24)
shashkac1 = Cherniy((84, 910), 0, 12)
shashkac2 = Cherniy((84, 848), 0, 12)
shashkac3 = Cherniy((84, 786), 0, 12)
shashkac4 = Cherniy((84, 724), 0, 12)
shashkac5 = Cherniy((84, 662), 0, 12)
shashkac6 = Cherniy((332, 42), 1, 17)
shashkac7 = Cherniy((332, 104), 1, 17)
shashkac8 = Cherniy((332, 166), 1, 17)
shashkac9 = Cherniy((546, 42), 1, 19)
shashkac10 = Cherniy((546, 104), 1, 19)
shashkac11 = Cherniy((546, 166), 1, 19)
shashkac12 = Cherniy((546, 228), 1, 19)
shashkac13 = Cherniy((546, 290), 1, 19)
shashkac14 = Cherniy((856, 910), 0, 1)
shashkac15 = Cherniy((856, 848), 0, 1)
dvor = Board(6, 15)
dvor.set_view(84, 42, 62)
dom = Board(6, 15)
dom.set_view(546, 42, 62)
zone = Board(1, 15)
zone.set_view(472, 42, 62)
konec = Board(1, 15)
konec.set_view(934, 42, 62)
cursor = arrow()
kub1 = choice((1, 2, 3, 4, 5, 6))
kub2 = choice((1, 2, 3, 4, 5, 6))
cvet = 0
kub = kubik(kub1, kub2, cvet)
nomer_hoda = 1
font = pygame.font.Font('freesansbold.ttf', 50)
orig_surf = font.render('Ход белых', True, (255, 255, 255))
txt_surf = orig_surf.copy()
alpha_surf = pygame.Surface(txt_surf.get_size(),
                            pygame.SRCALPHA)
alpha = 255
hod_prois = False
perenos = 0

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0),
                        (0, 0, 0, 0, 0, 0, 0, 0))

clock = pygame.time.Clock()
running = True
#Звуковое сопровождение действий/кликов
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.init()
            pygame.mixer.music.load('hod1.mp3')
            pygame.mixer.music.play()
            if nomer_hoda % 2 == 1:
                for k in all_sprites2:
                    k.cifri_s_kubika(kub1, kub2)
                for k in all_sprites2:
                    k.nagat(event)
            else:
                for k in all_sprites3:
                    k.cifri_s_kubika(kub1, kub2)
                for k in all_sprites3:
                    k.nagat(event)
        if event.type == pygame.MOUSEMOTION:
            for i in all_sprites1:
                i.cursor(event)

            if nomer_hoda % 2 == 1:
                for k in all_sprites2:
                    k.on_board(event)

            else:
                for k in all_sprites3:
                    k.on_board(event)
        if event.type == pygame.MOUSEBUTTONUP:
            pygame.mixer.init()
            pygame.mixer.music.load('hod.mp3')
            pygame.mixer.music.play()
            if nomer_hoda % 2 == 1:
                for k in all_sprites2:
                    k.otgat()
                    hod_prois += k.game_process()
                    if k.odin_hod() == 1:
                        kub1 = 0
                    elif k.odin_hod() == 2:
                        kub2 = 0
                    perenos += k.odin_hod()
                if perenos % 3 != 0:
                    for k in all_sprites2:
                        kletk_perenos = k.return_kletk()
                        for l in all_sprites3:
                            l.perenos(kletk_perenos)
                    else:
                        perenos = 0

            else:
                for k in all_sprites3:
                    k.otgat()
                    hod_prois += k.game_process()
                    if k.odin_hod() == 1:
                        kub1 = 0
                    elif k.odin_hod() == 2:
                        kub2 = 0
                    perenos += k.odin_hod()
                if perenos % 3 != 0:
                    for k in all_sprites3:
                        kletk_perenos = k.return_kletk()
                        for l in all_sprites2:
                            l.perenos(kletk_perenos)
                    else:
                        perenos = 0

            if hod_prois >= 1:
                kub1 = choice((1, 2, 3, 4, 5, 6))
                kub2 = choice((1, 2, 3, 4, 5, 6))
                if nomer_hoda % 2 == 1:
                    font = pygame.font.Font('freesansbold.ttf', 50)
                    orig_surf = font.render('Ход чёрных', True, (0, 0, 0))
                    txt_surf = orig_surf.copy()
                    alpha_surf = pygame.Surface(txt_surf.get_size(),
                                                pygame.SRCALPHA)
                    alpha = 255

                    cvet = 1
                else:
                    cvet = 0
                    font = pygame.font.Font('freesansbold.ttf', 50)
                    orig_surf = font.render('Ход белых', True, (255, 255, 255))
                    txt_surf = orig_surf.copy()
                    alpha_surf = pygame.Surface(txt_surf.get_size(),
                                                pygame.SRCALPHA)
                    alpha = 255
                kub = kubik(kub1, kub2, cvet)
                pygame.mixer.init()
                pygame.mixer.music.load('brosok.mp3')
                pygame.mixer.music.play()
    if hod_prois >= 1:
        nomer_hoda += 1
        hod_prois = False
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    all_sprites2.draw(screen)
    all_sprites2.update()
    all_sprites3.draw(screen)
    all_sprites3.update()
    if nomer_hoda % 2 == 1:
        pygame.draw.rect(screen, pygame.Color('white'), (208, 476, 62, 62), 0)
        pygame.draw.rect(screen, pygame.Color('white'), (271, 476, 62, 62), 0)
        if alpha > 0:
            alpha = max(alpha - 4, 0)
            txt_surf = orig_surf.copy()
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0),
                          special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(txt_surf, (363, 476))
    else:
        pygame.draw.rect(screen, pygame.Color('white'), (670, 476, 62, 62), 0)
        pygame.draw.rect(screen, pygame.Color('white'), (733, 476, 62, 62), 0)
        if alpha > 0:
            alpha = max(alpha - 4, 0)
            txt_surf = orig_surf.copy()
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0),
                          special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(txt_surf, (363, 476))
    kub.brosok()
    if (kub1 == 0) and (kub2 == 0):
        font = pygame.font.Font('freesansbold.ttf', 50)
        orig_surf = font.render('Нажмите для следующего хода', True,
                                (140, 0, 0))
        screen.blit(orig_surf, (93, 476))
    if pygame.mouse.get_focused():
        all_sprites1.draw(screen)
        all_sprites1.update()
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
