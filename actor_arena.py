 
class Actor():
    def move(self):
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int, int, int):
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int, int, int):
        raise NotImplementedError('Abstract method')


class Arena():
    def __init__(self, size: (int, int)):
        self._w, self._h = size
        self._count = 0
        self._actors = []

    def add(self, a: Actor):
        if a not in self._actors:
            self._actors.append(a)

    def remove(self, a: Actor):
        if a in self._actors:
            self._actors.remove(a)

    def move_all(self):
        actors = list(reversed(self._actors))
        for a in actors:
            a.move()
            for other in actors:
                # reversed order, so actors drawn on top of others
                # (towards the end of the cycle) are checked first
                if other is not a and self.check_collision(a, other):
                        a.collide(other)
                        other.collide(a)
        self._count += 1

    def check_collision(self, a1: Actor, a2: Actor) -> bool:
        '''Check the two actors (args) for mutual collision (bounding-box
        collision detection). Return True if colliding, False otherwise
        '''
        x1, y1, w1, h1 = a1.position()
        x2, y2, w2, h2 = a2.position()
        return (y2 < y1 + h1 and y1 < y2 + h2
            and x2 < x1 + w1 and x1 < x2 + w2
            and a1 in self._actors and a2 in self._actors)

    def actors(self) -> list:
        '''Return a copy of the list of actors
        '''
        return list(self._actors)

    def size(self) -> (int, int):
        '''Return the size of the arena as a couple: (width, height)
        '''
        return (self._w, self._h)

    def count(self) -> int:
        '''Return the total count of ticks (or frames)
        '''
        return self._count
