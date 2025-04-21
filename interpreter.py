import copy
from colorama import Fore, Back, Style
import time
class Vector2i:

    def __init__(self, x:int = 0, y:int = 0):
        self.x:int = x
        self.y:int = y
    def __add__(self, o):
        return Vector2i(self.x+o.x,self.y+o.y)
    def __str__(self):
        return f"({self.x},{self.y})"
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y  
    def __mul__(self, o):
        return Vector2i(self.x*o.x,self.y*o.y)

    def __hash__(self):
        return hash((self.x, self.y))  
class Interpreter:
    def __init__(self, code):
        self.code = code
        self.detectors = {} # Vector2i(0,0): Vector2i(1,0)
        self.rays = []
        self.commands = {
            '>': self.do_arrow_right,
            '^': self.do_arrow_up,
            'v': self.do_arrow_down,
            '<': self.do_arrow_left,

            '\\': self.do_back_slash,
            '/': self.do_slash,

            '#': self.do_destroy,
            '+': self.do_split,

            "$": self.do_emitter,

            '1': self.do_active_flip,
            '0': self.do_inactive_flip,

            "!": self.do_skip,
        }
    def print_visual(self):
        newcode = copy.deepcopy(self.code)
        for ray in self.rays:
            newcode[ray['pos'].x][ray['pos'].y] = Fore.YELLOW+"-"+Style.RESET_ALL
        newcode = self.reverse_array_operation(newcode)

        for row in newcode:
            print(*row, sep='')
        print("\n")
    def get_dir(self, letter):
        match letter:

            case "D":
                return  Vector2i(0,1)
            case "L":
                return  Vector2i(-1,0)
            case "U":
                return  Vector2i(0,-1)
            case _:
                return Vector2i(1,0)
    def check_detectors(self):
        for detector, dir in self.detectors.items():
            match self.code[detector.x-dir.x][detector.y-dir.y]:
                case "1":
                    ray = {"pos":detector, 'dir': dir}
                    ray["pos"] += ray['dir']
                    self.rays.append(ray)

    def get_detectors(self):
        for x, column in enumerate(self.code):
            for y, item in enumerate(column):
                pos = Vector2i(x,y)
                match item:
                    case "]":
                        self.detectors[pos] = Vector2i(-1,0)
                    case "[":
                        self.detectors[pos] = Vector2i(1,0)
                    case "u":
                        self.detectors[pos] = Vector2i(0,-1)
                    case "n":
                        self.detectors[pos] = Vector2i(0,1)
                if pos in self.detectors.keys() and self.code[pos.x-self.detectors[pos].x][pos.y-self.detectors[pos].y] == "1":
                    ray = {"pos":Vector2i(x,y), 'dir': self.detectors[pos]}
                    ray["pos"] += ray['dir']
                    self.rays.append(ray)
    def reverse_array_operation(self,code):
        height = len(code[0]) if code else 0
        width = len(code)
        reversed_code = [['' for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                reversed_code[y][x] = code[x][y]

        return reversed_code
    def run(self):
        self.get_detectors()
        for x, column in enumerate(self.code):
            for y, item in enumerate(column):
                if item == "*":
                    if x+1 < len(self.code):
                        ray = {"pos":Vector2i(x, y), 'dir': Vector2i(1,0)}
                        ray['dir'] = self.get_dir(self.code[x+1][y])
                        ray["pos"] += ray['dir']
                        self.rays.append(ray)
        while len(self.rays) > 0:

            rays_copy = copy.copy(self.rays)
            for ray in rays_copy:
                ray['pos'] = Vector2i(ray['pos'].x % len(self.code), ray['pos'].y % len(self.code[0]))
                inst = self.code[ray['pos'].x][ray['pos'].y]
                
                #print(inst)
                if inst in self.commands:
                    self.commands[inst](ray)

                #check for collision with other rays
                for r in rays_copy:
                    if ((ray['pos'] + ray['dir']) == r['pos']) and r in self.rays and ray in self.rays :
                        if self.code[r['pos'].x][r['pos'].y] not in "$":
                            self.rays.remove(r)
                        self.rays.remove(ray)
                ray['pos'] += ray['dir']
            self.check_detectors()
            self.print_visual()
            #time.sleep(0.1)
    def do_emitter(self, ray):
        
        if ray in self.rays:
            self.rays.remove(ray)
        ray = {"pos":Vector2i(ray['pos'].x, ray['pos'].y), 'dir': Vector2i(1,0)}
        ray['dir'] = self.get_dir(self.code[ray['pos'].x+1][ray['pos'].y])
        ray["pos"] += ray['dir']
        self.rays.append(ray)
        
    def do_arrow_left(self, ray): # <
        if ray['dir'].y > 0:
            self.do_slash(ray)
            return
        if ray['dir'].y < 0:
            self.do_back_slash(ray)
            return
        if ray['dir'].x < 0:
            ray['dir'].x *= -1
            return
    def do_arrow_right(self, ray): # >
        if ray['dir'].y < 0:
            self.do_slash(ray)
            return
        if ray['dir'].y > 0:
            self.do_back_slash(ray)
            return
        if ray['dir'].x > 0:
            ray['dir'].x *= -1
            return
    def do_arrow_up(self, ray): # ^
        if ray['dir'].x > 0:
            self.do_slash(ray)
            return
        if ray['dir'].x < 0:
            self.do_back_slash(ray)
            return
        if ray['dir'].y < 0:
            ray['dir'].y *= -1
            return
    def do_arrow_down(self, ray): # v
        if ray['dir'].x < 0:
            self.do_slash(ray)
            return
        if ray['dir'].x > 0:
            self.do_back_slash(ray)
            return
        if ray['dir'].y > 0:
            ray['dir'].y *= -1
            return
    def do_slash(self, ray):
        ray['dir'] = Vector2i(-ray['dir'].y, -ray['dir'].x)
    def do_back_slash(self, ray):
        ray['dir'] = Vector2i(ray['dir'].y, ray['dir'].x)
    def do_destroy(self,ray):
        
        self.rays.remove(ray)
    def do_split(self, ray):
        original_dir = ray['dir']
        if original_dir.x != 0:
            offset_a = Vector2i(0, -1)
            offset_b = Vector2i(0, 1)
        else:
            offset_a = Vector2i(-1, 0)
            offset_b = Vector2i(1, 0)

        # it may seem over the top removing a ray and also creating one at the same time, but this is to sync them
        self.rays.append({
            'pos': ray['pos'] + offset_b,
            'dir': original_dir
        })
        self.rays.append({
            'pos': ray['pos'] + offset_a,
            'dir': original_dir
        })
        self.rays.remove(ray)
    def do_skip(self, ray):
        ray['pos'] += ray['dir']
        
    def do_active_flip(self, ray):
        self.code[ray['pos'].x][ray['pos'].y] = '0'
    def do_inactive_flip(self, ray):
        self.code[ray['pos'].x][ray['pos'].y] = '1'

