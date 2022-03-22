from math import hypot
from turtle import Turtle
from shapes import Rectangle


class Writer(Turtle):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.hideturtle()

    def write_text(self, text, font="Arial", size=8, textType="normal", color="black", x=None, y=None):
        if x is None:
            x = self.xcor()
        if y is None:
            y = self.ycor()
        self.goto(x, y)
        self.color(color)
        self.write(text, move=False, align="center", font=(font, size, textType))

class KeyHandler:
    def __init__(self, screen):
        self._screen = screen
        self._keys = []
        self._run = []
        screen.listen()

    def addkey(self, key, bind, wait=False):
        if self.update_bind(key, bind):
            return
        self._run.append([key, bind])
        if wait:
            self._run[len(self._run) - 1].append(False)

        def modify(operation):
            def func():
                if operation is 'add':
                    if self._keys.count(key) is 0:
                        self._keys.append(key)
                if operation is 'remove':
                    if self._keys.count(key) > 0:
                        self._keys.remove(key)
            return func
        self._screen.onkeypress(modify('add'), key)
        self._screen.onkeyrelease(modify('remove'), key)

    def update_bind(self, key, bind):
        for run in self._run:
            if run[0] is key:
                run[1] = bind
                return True
        return False

    def run(self, key=None):
        for run in self._run:
            if run[0] is key or key is None:
                if len(run) > 2:
                    if self._keys.count(run[0]) > 0:
                        if run[2] is False:
                            run[1]()
                        run[2] = True
                    else:
                        run[2] = False
                    continue
                if self._keys.count(run[0]) > 0:
                    run[1]()


class Button(Writer):
    def __init__(self, screen, position, width, height, text, onclick, color="gray", text_size=8, text_color="white"):
        position = list(position)
        super().__init__(position[0], position[1])
        self.goto(position[0] - (width / 2), position[1] - (height / 2))
        tracer = screen.tracer()
        screen.tracer(0)
        self.fillcolor(color)
        self.begin_fill()
        self.setx(self.xcor() + width)
        self.sety(self.ycor() + height)
        self.setx(self.xcor() - width)
        self.sety(self.ycor() - height)
        self.end_fill()
        self.should_check = True
        self.write_text(text, color=text_color, size=text_size, x=position[0], y=self.ycor() + (height / 4))
        screen.tracer(tracer)
        def click(x, y):
            if abs(x - position[0]) <= width / 2 and abs(y - position[1]) <= height / 2 and self.should_check:
                onclick(self)
        screen.onclick(click, add=True)

    def stop(self):
        self.should_check = False

class PauseButton(Button):
    def __init__(self, screen, x, y, width, height, bg_color, color):
        super().__init__(screen, (x, y), width, height, '', self.pause, bg_color)
        self.display = [
            Rectangle(x - (width / 4), y, (width / 3), height, color),
            Rectangle(x + (width / 4), y, (width / 3), height, color),
            Turtle(shape='triangle')
        ]
        self.display[2].penup()
        self.display[2].color(color)
        self.display[2].goto(x, y)
        self.display[2].ht()
        self.paused = False

    def pause(self, _arg1=None, _arg2=None, _arg3=None):
        self.paused = not self.paused
        if self.paused:
            self.display[0].ht()
            self.display[1].ht()
            self.display[2].st()
        else:
            self.display[0].st()
            self.display[1].st()
            self.display[2].ht()
        return self.paused

class PathCalculator:
    def __init__(self):
        self.x = None
        self.y = None

    def distance(self, other):
        return hypot(abs(other.xcor() - self.x), abs(other.ycor() - self.y))

    def calculate_path(self, start_x, start_y, x_vel, y_vel, func, end, get_only=None):
        if get_only is 'first':
            return [[start_x + x_vel, start_y + y_vel]]
        path = []
        self.x = start_x
        self.y = start_y
        i = 0
        while not end(self):
            self.x += x_vel
            self.y += y_vel
            result = func(self, x_vel, y_vel)
            x_vel = result[0]
            y_vel = result[1]
            if get_only is None:
                path.append([self.x, self.y])
            else:
                if get_only is i:
                    return [self.x, self.y]
            i += 1
        if get_only is 'last':
            return [self.x, self.y]
        return path


def move(thing, x_change, y_change, x_min=float('-inf'), x_max=float('inf'), y_min=float('-inf'), y_max=float('inf')):
    def func():
        thing.goto(thing.xcor() + x_change, thing.ycor() + y_change)
        if thing.xcor() < x_min:
            thing.setx(x_min)
        if thing.ycor() < y_min:
            thing.sety(y_min)
        if thing.xcor() > x_max:
            thing.setx(x_max)
        if thing.ycor() > y_max:
            thing.sety(y_max)
    return func

def bool_to_num(boolean):
    if boolean:
        return 1
    return 0

def typeof(value):
    return list(str(type(value)).split('\''))[1]
