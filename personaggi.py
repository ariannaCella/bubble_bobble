import actor_arena as a
from random import choice, randrange

class Dragon(a.Actor):
        
    def __init__(self, arena,pos,CONSTANT_CONTORNO):
        self._x , self._y = pos
        self._dx, self._dy = 0, 0
        self._w, self._h= 20,18
        self._speed=3
        self._salto=10
        self._contorno=CONSTANT_CONTORNO
        self._terra=False
        self._arena=arena
        self._ARENA_W, self._ARENA_H= arena.size()
        arena.add(self)
        self._lives = 1
        self._shoot=False
   
    def bolla(self):
        if self._lives!=0:
            self._shoot=True
            if self._dx>=0:
               Bolle(self._arena,self._x+self._w, self._y, self._dx)
            else:
               Bolle(self._arena,self._x-self._w, self._y, self._dx)
           
    def no_sparo(self):
        self._shoot=False
       
    def direzione_dx(self)-> int:
        return self._dx
    
    def move(self):
        g=0.4
        self._dy += g
        self._y += self._dy
        if self._y < self._contorno:
            self._y = self._contorno
        elif self._y >= self._ARENA_H - self._h-self._contorno:
            self._y = self._ARENA_H - self._h-self._contorno
            self.terra = True
            self._lives=0
        if self._lives!=0:
            self._x += self._dx
            if self._x < self._contorno:
                self._x = self._contorno
            elif self._x > self._ARENA_W - self._w-self._contorno:
                self._x = self._ARENA_W - self._w-self._contorno
        
    def jump(self):
        if self._lives!=0:
            if self._y == self._ARENA_H - self._h- self._contorno or self._terra:
                self._dy=-self._salto
                self._terra=False
            
    def go_left(self, go: bool):
        if go:
            self._dx = -self._speed
        elif self._dx < 0:
            self._dx = 0

    def go_right(self, go: bool):
        if go:
            self._dx = self._speed
            self._dy=0
        elif self._dx > 0:
            self._dx = 0
            
    def stay(self):
        self._dx = 0

    def go_down(self, go: bool):
        if go:
            self._dy = self._speed
        elif self._dy > 0:
            self._dy = 0

    def lives(self) -> int:
        return self._lives
    
    def collide(self, other):
        if isinstance(other, Piattaforma):
            x1, y1, w1, h1 = self.position()  
            x2, y2, w2, h2 = other.position()
            bordi = [(x1+w1 - x2, -1, 0), (x2+w2 - x1, 1, 0),
                       (y1+h1 - y2, 0, -1)]#distanza,segno_dx,segno_dy
            move = min(bordi)
            if self._dy>0:
                self._x += move[1] * move[0]  ## sign_dx * distance
                self._y += move[2] * move[0]  ## sign_dy * distance
                if move[2] < 0:
                    self._terra = True
                if move[2] != 0:
                    self._dy = 1
            else:
                self._x += move[1]        
        elif isinstance(other, Avversari):
            self._lives=0
            #self._arena.remove(self)
                
    def position(self) -> (int, int, int, int):
        return self._x, self._y, self._w, self._h
    
    def symbol(self) -> (int, int, int, int):
        #quando si sposta verso sinistra
        if self._dx<0 and self._shoot==False and self._lives!=0:
             return 325,15, self._w, self._h
            
        #quando si sposta verso destra
        elif self._dx>0 and self._shoot==False and self._lives!=0:
            return 943,15, self._w, self._h
        
        #quando è fermo
        elif ((self._dx==0 and self._dy==0) or self._terra) and self._lives!=0 and self._shoot==False:
            return 329, 189, self._w, self._h
        
        #quando va verso il basso dopo un salto
        elif self._dy<0 and self._shoot==False and self._lives!=0:
            return 443,65, self._w, self._h
        
        #quando salta
        elif self._dy>0 and self._shoot==False and self._lives!=0:
            return 783, 66, self._w, self._h
        
        #quando si scontra con un avversario
        elif self._lives==0:
            return 566, 144, 32,33
        
        #quando spara bolla verso sinistra
        elif self._shoot and self._dx<0 and self._lives!=0:
           return 453,36,18,18
        
        #quando spara bolla verso destra
        elif self._shoot and self._dx>=0 and self._lives!=0:
           return 902,36,17,18


class Bolle(a.Actor):
    def __init__(self,arena,x,y,dx):
        self._x,self._y=x,y
        self._speed_x=4
        self._speed_y=4
        self._dx=dx
        self._dy=0
        self._w,self._h=18,18
        self._arena=arena
        arena.add(self)
        self._frame=0
        self._bolla_scoppiata=False
        self._avversari_catturati=False
        self._ARENA_W, self._ARENA_H= arena.size()
        
    def move(self):
        if self._frame<20:
            self._frame+=1
            if self._dx>=0:
                self._x+=self._speed_x
            else:
                self._x-=self._speed_x
        else:
            self._y-=self._speed_y
            #if self._y < 31:
                #self._y = 31
            
        if self._avversari_catturati:
            self._y-=self._speed_y
            
    def collide(self, other):
        if isinstance(other,Avversari):
            self._avversari_catturati=True
            if self._bolla_scoppiata==False: 
                self._speed_x=0
        elif isinstance(other, Dragon):
            self._bolla_scoppiata=True 

    
    def avv_catturati(self)->bool:
        return self._avversari_catturati
    
    def bolla_scoppiata(self)->bool:
        return self._bolla_scoppiata
    
    def position(self) -> (int, int, int, int):
        return self._x,self._y,self._w,self._h

    def symbol(self) -> (int, int, int, int):
        if self._bolla_scoppiata:
            return 612,1048,18,20  
        elif self._avversari_catturati and self._bolla_scoppiata==False:
            return 375,244,16,18

        return 77,1071,self._w,self._h
    
        
    
class Piattaforma(a.Actor):

    def __init__(self, arena, x, y,w,h):
        self._x, self._y = x, y
        self._w, self._h = w,h
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def collide(self, other):
        pass

    def position(self) -> (int, int, int, int):
        return self._x, self._y, self._w, self._h

    def symbol(self) -> (int, int, int, int):
        return 113, 158, self._w, self._h

            
class Avversari(Dragon):
    
    def __init__(self, arena, pos,CONSTANT_CONTORNO):
        self._x, self._y = pos
        self._w, self._h = 19, 18
        self._dx,self._dy=0,0
        self._speed=3
        self._lives=1
        self._death=False
        self._salto=10
        self._bonus=0
        self._contorno=CONSTANT_CONTORNO
        self._contorno_basso=25
        self._terra=False
        self._arena=arena
        arena.add(self)
        self._ARENA_W, self._ARENA_H= arena.size()

    def move(self):
        r = randrange(100)
        if r == 0:
            self.go_left(True)
        elif r == 1:
            self.go_right(True)
        elif r == 2:
            self.jump()
        elif r== 3:
            self.stay()

        g=0.4
        self._dy += g
        self._y += self._dy
            
        if self._y < self._contorno:
            self._y = self._contorno
        elif self._y >= self._ARENA_H - self._h-self._contorno_basso:
            self._y = self._ARENA_H - self._h-self._contorno_basso
            self._terra = True
            
        self._x += self._dx
        if self._x < self._contorno:
            self._x = self._contorno
        elif self._x > self._ARENA_W - self._w-self._contorno:
            self._x = self._ARENA_W - self._w-self._contorno
        
        
    def collide(self, other):
        if isinstance(other, Piattaforma):
            x1, y1, w1, h1 = self.position()  
            x2, y2, w2, h2 = other.position()
            bordi = [(x1+w1 - x2, -1, 0), (x2+w2 - x1, 1, 0),
                       (y1+h1 - y2, 0, -1), (y2+h2 - y1, 0, 1)]#distanza,segno_dx,segno_dy
            move = min(bordi)
            if self._dy>0:
                self._x += move[1] * move[0]  ## sign_dx * distance
                self._y += move[2] * move[0]  ## sign_dy * distance
                if move[2] < 0:
                    self._terra = True
                if move[2] != 0:
                    self._dy = 1
            else:
                self._x += move[1] * move[0]
                
        elif isinstance(other, Bolle):
            if other.bolla_scoppiata()==False and other.avv_catturati()==True:
                self._death=True
                self._bonus+=100
                self._arena.remove(self)
            
            
    def death(self)-> bool:
        return self._death

    def bonus(self)->int:
        return self._bonus
    
    def position(self)-> (int, int, int, int):
        return self._x, self._y, self._w, self._h

    def symbol(self)-> (int, int, int, int):
        if self._death:
            return 244, 244, 20,18
        if self._dx<0:
            return 3, 244, self._w, self._h
        else:
            return 1269,244,self._w, self._h
        
