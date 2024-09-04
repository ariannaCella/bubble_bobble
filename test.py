import unittest
#import Bubble_Bubble as BB
import actor_arena as aa
import personaggi as b

class DragonTest(unittest.TestCase):
   
   def test_move_destra(self):
      a = aa.Arena((509, 425))
      drago=b.Dragon(a, (40, 140),31) #dx=3
      p=b.Piattaforma(a,33, 158, 31, 15)
      drago.go_right(True)
      drago.move()
      drago.collide(p)
      drago.move()
      drago.collide(p)
      drago.go_right(False)
      self.assertTrue(drago.position()== (46, 140, 20 ,18))
      
   def test_move_sinistra_contorno(self):
      a = aa.Arena((509, 425))
      drago=b.Dragon(a, (31, 140),31) #dx=3
      p=b.Piattaforma(a,33, 158, 31, 15)
      drago.go_left(True)
      drago.move()
      drago.collide(p)
      drago.go_left(False)
      self.assertTrue(drago.position()== (31, 140, 20 ,18))
      
   def test_move_destra_contorno(self):
      a = aa.Arena((509, 425))
      drago=b.Dragon(a, (509-31-20, 140),31) #dx=3
      p=b.Piattaforma(a,448, 158, 31, 15)
      drago.go_right(True)
      drago.move()
      drago.collide(p)
      drago.go_right(False)
      self.assertTrue(drago.position()== (509-31-20, 140, 20 ,18))
      
   def test_move_sinistra(self):
      a = aa.Arena((509, 425))
      drago=b.Dragon(a, (40, 140),31) #dx=3
      p=b.Piattaforma(a,33, 158, 31, 15)
      drago.go_left(True)
      drago.move()
      drago.collide(p)
      drago.move()
      drago.collide(p)
      drago.go_left(False)
      self.assertTrue(drago.position()== (34, 140, 20 ,18))

   def test_salto(self): 
      a = aa.Arena((509, 425))
      p = b.Piattaforma(a, 33, 158, 31, 15)
      d = b.Dragon(a, (50, 158-18),31) #dx=10
      d.collide(p)
      d.jump()
      d.move()
      g=0.4
      self.assertTrue(d.position()== (50,158-18+g,20,18))
      
   def test_collide_piattaforma(self):
      a = aa.Arena((509, 425))
      p = b.Piattaforma(a, 113, 158, 286, 18)
      p1= b.Piattaforma(a, 200-31, 158-18-15, 31, 15)
      p2 = b.Piattaforma(a, 200+20, 158-18-15, 31, 15)
      d = b.Dragon(a, (200, 158-18),31)#20,18 dimensioni drago
      d.collide(p)
      d.collide(p1)
      d.collide(p2)
      self.assertTrue(d.position()== (200,158-18,20,18))
      
   def test_collide_avversari(self):
      a = aa.Arena((509, 425))
      avv = b.Avversari(a, (50, 50), 31)
      d = b.Dragon(a, (230, 170),31)
      d.collide(avv)
      self.assertTrue(d.lives() == 0)

                 
class BollaTest(unittest.TestCase):
   
   def test_move_destra(self):
      a = aa.Arena((509, 425))
      d = b.Dragon(a, (230, 170),31)
      ba=b.Bolle(a, 230+20, 170 ,3) #speed=4
      ba.move()
      ba.move()
      self.assertTrue(ba.position()== (230+20+4*2, 170, 18 ,18))
      
   def test_move_verso_alto(self): #nel caso di destra
      a = aa.Arena((509, 425))
      d = b.Dragon(a, (230, 170),31)
      ba=b.Bolle(a, 230+20, 170 ,3)#speed=4
      for i in range (1,26):
         ba.move()               #dopo 20 frame sale verso alto per 5 frame
      self.assertTrue(ba.position()== (330,150,18,18))

   def test_move_sinistra(self):
      a = aa.Arena((509, 425))
      d = b.Dragon(a, (230, 170),31)
      ba=b.Bolle(a, 230-20, 170 ,-3) #speed=4
      ba.move()
      ba.move()
      self.assertTrue(ba.position()== (230-20-(4*2), 170, 18 ,18))
      
   def test_collide_avversari_con_bolla_scoppiata(self):
        a = aa.Arena((509, 425))
        avv = b.Avversari(a, (200, 200), 31)
        d = b.Dragon(a, (230, 170),31)
        ba=b.Bolle(a, 230+20, 170 ,3)
        ba.collide(d)
        avv.collide(ba)
        self.assertTrue(avv.death() == False)

   def test_collide_avversari(self):
        a = aa.Arena((509, 425))
        avv = b.Avversari(a, (200, 200), 31)
        d = b.Dragon(a, (230, 170),31)
        ba=b.Bolle(a, 230+20, 170 ,3)
        ba.collide(avv)
        avv.collide(ba)
        self.assertTrue(avv.death() == True)
        self.assertTrue(ba.avv_catturati()==True)
        self.assertTrue(ba.symbol()==(375,244,16,18))
      

   
if __name__ == '__main__':
    unittest.main() 
   
