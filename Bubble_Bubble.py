import personaggi as p
import actor_arena as a
import g2d
class BubbleBobbleGame:
   
   def __piattaforme(self):
        if self._level==1:
            y_platform_position=158
            SPACE_PLATFORM=81
            for i in range(3):
               p.Piattaforma(self._arena,  33, y_platform_position, 31, 15)
               p.Piattaforma(self._arena,  113, y_platform_position, 286, 18)
               p.Piattaforma(self._arena,  448, y_platform_position, 31, 15)
               y_platform_position+=SPACE_PLATFORM
               
        if self._level==2:
            p.Piattaforma(self._arena,720-509, 81, 93, 15)
            p.Piattaforma(self._arena,675-509, 161, 77, 14)
            p.Piattaforma(self._arena,785-509, 161, 80, 17)
            p.Piattaforma(self._arena,624-509, 240, 288, 14)
            p.Piattaforma(self._arena,577-509, 321, 111, 16)
            p.Piattaforma(self._arena,721-509,321, 96 ,15)
            p.Piattaforma(self._arena,849-509, 321, 112, 13)
           
   def __init__(self, level):
        CONSTANT_CONTORNO=31
        self._level=level
        self._arena = a.Arena((509, 425))
        if self._level==1:
           self._avv1=p.Avversari(self._arena,(10,200),CONSTANT_CONTORNO)
           self._avv2=p.Avversari(self._arena,(10,200),CONSTANT_CONTORNO)
           self._avv3=p.Avversari(self._arena,(10,200),CONSTANT_CONTORNO)
        if self._level==2:
           self._avv4=p.Avversari(self._arena,(110,200),CONSTANT_CONTORNO)
           self._avv5=p.Avversari(self._arena,(240,200),CONSTANT_CONTORNO)
           self._avv6=p.Avversari(self._arena,(190,200),CONSTANT_CONTORNO)
           self._avv7=p.Avversari(self._arena,(90,200),CONSTANT_CONTORNO)

        self._drago = p.Dragon(self._arena, (200, 60),CONSTANT_CONTORNO)
        self._drago1=p.Dragon(self._arena, (210, 60),CONSTANT_CONTORNO)
        self._playtime = 60  # seconds
        self.__piattaforme()
   
           
   def arena(self) -> a.Arena:
      return self._arena

   def drago(self) -> p.Dragon:
      return self._drago

   def drago1(self) -> p.Dragon:
      return self._drago1

   def avversario1(self)-> p.Avversari:
      if self._level==1:
         return self._avv1

   def avversario2(self)-> p.Avversari:
      if self._level==1:
         return self._avv2

   def avversario3(self)-> p.Avversari:
      if self._level==1:
         return self._avv3
      
   def avversario4(self)-> p.Avversari:
      if self._level==2:
         return self._avv4
      
   def avversario5(self)-> p.Avversari:
      if self._level==2:
         return self._avv5

   def avversario6(self)-> p.Avversari:
      if self._level==2:
         return self._avv6
      
   def avversario7(self)-> p.Avversari:
      if self._level==2:
         return self._avv7

   def level(self)-> int:
      return self._level
   
   def level1_won(self)->bool:
      if self._level==1:
         return self._avv1.death() and self._avv2.death() and self._avv3.death()
   
   def game_over(self) -> bool:
      return (self._drago1.lives() <= 0 and self._drago.lives() <= 0) or self.remaining_time() <= 0
   
   def game_won(self) -> bool:
      if self._level==2:
         return self._avv4.death() and self._avv5.death() and self._avv6.death() and self._avv7.death()

   def remaining_time(self) -> int:
      return (self._playtime - self._arena.count() // 30)


class BubbleBobbleGui:
    def __init__(self, BB_level):
        self._game = BB_level
        g2d.init_canvas(self._game.arena().size())
        self._img_drago=g2d.load_image("bubble-bobble.png")
        self._img_piattaforma=g2d.load_image("bubble-bobble-tiles.png")
        self._img_maps=g2d.load_image("bubble-bobble-maps.png")
        g2d.main_loop(self.tick)
       
    def handle_keyboard(self):
        drago = self._game.drago()
        drago1= self._game.drago1()
        
        #COMANDI per drago
        if g2d.key_pressed("ArrowUp"):
            drago.jump()
        elif g2d.key_pressed("ArrowLeft"):
            drago.go_left(True)
        elif g2d.key_pressed("ArrowRight"):
            drago.go_right(True)
        elif (g2d.key_released("ArrowLeft") or g2d.key_released("ArrowRight")):
            drago.stay()
        elif g2d.key_pressed("Spacebar"): #spara bolle
            drago.bolla()
        elif g2d.key_released("Spacebar"):
            drago.no_sparo()

        #COMANDI per drago1
        if g2d.key_pressed("w"):
            drago1.jump()
        if g2d.key_pressed("a"):
            drago1.go_left(True)
        if g2d.key_pressed("d"):
            drago1.go_right(True)
        if (g2d.key_released("a") or g2d.key_released("d")):
            drago1.stay()
        if g2d.key_pressed("s"): #spara bolle
            drago1.bolla()
        if g2d.key_released("s"):
            drago1.no_sparo()
      
    def tick(self):
        self.handle_keyboard()
        arena = self._game.arena()
        level=self._game.level()
        arena.move_all() 
        g2d.clear_canvas()
        
        if level==1:
            g2d.draw_image_clip(self._img_maps,(0,0,509,425),(0,0,509,425)) #mappa livello 1
        elif level==2:
            g2d.draw_image_clip(self._img_maps,(510,0,509,425),(0,0,509,425))#mappa livello 2
        
        for a in arena.actors():
            if not isinstance(a, p.Piattaforma):
                g2d.draw_image_clip(self._img_drago, a.symbol(), a.position())
                    
        lives = "Lives player_1 = " + str(self._game.drago().lives())
        lives1 = "Lives player_2 = " + str(self._game.drago1().lives())
        if level==1:
           punti= "Points: " + str(int(self._game.avversario1().bonus())+int(self._game.avversario2().bonus())+int(self._game.avversario3().bonus()))
        elif level==2:
           punti= "Points: " + str(300 +int(self._game.avversario4().bonus())+int(self._game.avversario5().bonus())+int(self._game.avversario6().bonus()) +int(self._game.avversario7().bonus()) )
        toplay = "Time: " + str(self._game.remaining_time())
        level = "Level: " + str(self._game.level())
        g2d.set_color((0,0,0))
        g2d.draw_text( lives + "   " + lives1 + "  ", (0, 2), 23)
        g2d.draw_text( level+  "   " + punti, (0, 405), 20)
        g2d.draw_text( toplay, (400, 405), 20)
        
        if self._game.game_over():
            g2d.alert(" HAI PERSO!! :( ")
            g2d.close_canvas()

        elif self._game.level1_won():
            g2d.alert("HAI SUPERATO IL PRIMO LIVELLO")
            second_level()
              
        elif self._game.game_won():
            g2d.alert("HAI VINTO!! :)")
            g2d.close_canvas()
   
def first_level():
   BB_level1=BubbleBobbleGame(1)
   while BB_level1.level1_won()==False:
      BubbleBobbleGui(BB_level1)
      
def second_level():
   BB_level2=BubbleBobbleGame(2)
   while not BB_level2.game_won():
      BubbleBobbleGui(BB_level2)
      
first_level()
  
       
