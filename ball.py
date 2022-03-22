import math
from turtle import Turtle


class Ball(Turtle):
    def __init__(self, x=0, y=0, color="white"):
        super().__init__()
        self.penup()
        self.goto(x, y)
        self.color(color)
        self.shape('circle')
        self.x_vel = 1
        self.y_vel = 1
        self.def_x = x
        self.def_y = y

    def new_round(self):
        self.goto(self.def_x, self.def_y)
        self.x_vel = math.copysign(1, self.x_vel) * -1
        self.y_vel = 1

    def touching(self, paddles):
        shapes = list(map(lambda item1: list(map(lambda item2: item2 * 20, list(item1.shapesize()))), paddles))
        return (
                (
                 abs(paddles[0].xcor() - self.xcor()) <= shapes[0][1]
                 and
                 self.distance(paddles[0]) <= shapes[0][0] / 2
                )
                or
                (
                 abs(paddles[1].xcor() - self.xcor()) <= shapes[1][1]
                 and
                 self.distance(paddles[1]) <= shapes[1][0] / 2
                )
               )

    def ball_logic(self, paddles):
        bounced = False
        needed_x = self.xcor() + self.x_vel
        needed_y = self.ycor() + self.y_vel
        self.goto(self.xcor() + self.x_vel, self.ycor() + self.y_vel)
        if abs(self.ycor()) >= 290:
            self.y_vel *= -1
        if self.touching(paddles):
            bounced = True
            self.x_vel *= -1.01
            while self.touching(paddles):
                self.goto(self.xcor() + self.x_vel, self.ycor() + self.y_vel)
                if abs(self.ycor()) >= 290:
                    self.y_vel *= -1
        else:
            self.goto(needed_x, needed_y)
        return bounced
