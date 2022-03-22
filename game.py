import math
from ball import Ball
from shapes import Rectangle
from turtle import Turtle, Screen
from timeit import default_timer as time
from extra_modules import Writer, Button, PauseButton, move, KeyHandler, bool_to_num

class BallPathCalculator:
    def __init__(self):
        self.x = None
        self.y = None

    def calculate_path(self, start_x, start_y, x_vel, y_vel, smaller, bigger, paddle, get_only=None):
        if get_only is 'first':
            return [[start_x + x_vel, start_y + y_vel]]

        path = []
        self.x = start_x
        self.y = start_y
        i = 0
        paddle_x = paddle.xcor()
        while not (self.x <= smaller or self.x >= bigger):
            self.x += x_vel
            self.y += y_vel

            if self.y <= -290 or self.y >= 290:
                y_vel *= -1

            if abs(paddle_x - self.x) <= 20:
                x_vel *= -1.01
                while abs(paddle_x - self.x) <= 20:
                    self.x += x_vel
                    self.y += y_vel
                    if self.y <= -290 or self.y >= 290:
                        y_vel *= -1

            if get_only is None:
                path.append([self.x, self.y])
            else:
                if get_only is i:
                    return [[self.x, self.y]]
            i += 1

        if get_only is 'last':
            return [[self.x, self.y]]
        return path

class BPC2:
    def __init__(self):
        self.x = None
        self.y = None

    def calculate_path(self, start_x, start_y, wall_x, x_vel, y_vel, smaller, bigger, paddle, get_only=None):
        if get_only is 'first':
            return [[start_x + x_vel, start_y + y_vel]]

        self.x = start_x
        self.y = start_y
        i = 0
        paddle_x = paddle.xcor()
        paddle_y = paddle.ycor()
        while not (self.x <= smaller or self.x >= bigger):
            self.x += x_vel
            self.y += y_vel

            if self.y <= -290 or self.y >= 290:
                y_vel *= -1

            if abs(round(self.x)) <= abs(wall_x + math.copysign(10, wall_x)):
                x_vel *= -1
                self.x = math.copysign(abs(wall_x + math.copysign(10, wall_x)), self.x)

            if abs(paddle_x - self.x) <= 20 and math.hypot(self.x - paddle_x, self.y - paddle_y) <= 50:
                x_vel *= -1.01
                while abs(paddle_x - self.x) <= 20 and math.hypot(self.x - paddle_x, self.y - paddle_y) <= 50:
                    self.x += x_vel
                    self.y += y_vel
                    if self.y <= -290 or self.y >= 290:
                        y_vel *= -1
                return [[self.x, self.y]]
            i += 1
        return [[self.x, self.y]]


screen = Screen()
screen.bgcolor('black')
screen.title('Pong')
screen.setup(width=800, height=600)
screen.tracer(0)
PADDLE_SPEED = 2
buttons = []  # allows the function below to access this array
buttons.clear()
def start(players):
    def func(button=None):
        if button is not None:
            for button in buttons:
                button.clear()
                button.stop()

        paddles = [Rectangle(-350, 0, 20, 100), Rectangle(350, 0, 20, 100)]
        handler = KeyHandler(screen)
        calculator = BallPathCalculator()
        if players is 2:
            handler.addkey('W', move(paddles[0], 0, PADDLE_SPEED, y_min=-250, y_max=250))
            handler.addkey('w', move(paddles[0], 0, PADDLE_SPEED, y_min=-250, y_max=250))
            handler.addkey('S', move(paddles[0], 0, -PADDLE_SPEED, y_min=-250, y_max=250))
            handler.addkey('s', move(paddles[0], 0, -PADDLE_SPEED, y_min=-250, y_max=250))

        if players is not 0:
            handler.addkey('Up', move(paddles[1], 0, PADDLE_SPEED, y_min=-250, y_max=250))
            handler.addkey('Down', move(paddles[1], 0, -PADDLE_SPEED, y_min=-250, y_max=250))
        scores = [0, 0]
        ball = Ball()

        writer = Writer()
        for y in range(280, -280, -16):
            writer.write_text('|', x=0, y=y, size=8, color="white")
        writer.write_text('|', x=0, y=-280, size=8, color="white")

        writer = Writer()
        writer.write_text(0, x=-50, y=200, size=50, color="white")
        writer.write_text(0, x=50, y=200, size=50, color="white")

        pause_button = PauseButton(screen, 375, 275, 25, 25, 'black', 'gray')
        handler.addkey('space', pause_button.pause, True)
        
        def calculate_ball_path(b, mini, maxi, p):
            return calculator.calculate_path(
                b.xcor(),
                b.ycor(),
                b.x_vel,
                b.y_vel,
                mini,
                maxi,
                p,
                'last'
            )

        c1 = None
        c2 = None
        match_result = None
        def tiebreaker():
            ball.reset()
            ball.ht()
            balls = [Ball(), Ball()]
            balls[0].x_vel = 1
            balls[1].x_vel = -1
            balls[0].setx(-210)
            balls[1].setx(210)
            d1 = None
            d2 = None
            c = BPC2()
            if players is not 2:
                d1 = 150

            if players is 0:
                d2 = 150

            walls_x = [-200, 200]
            bounces = [[], []]
            bounces_to_delete = []
            turtles = [Turtle(), Turtle()]
            for turd in turtles:
                turd.ht()
                turd.pencolor('white')
            hex_color = '0123456789abcdef'
            while True:
                if pause_button.paused:
                    handler.run('space')
                    screen.update()
                    continue
                tm = time()

                bounced = [balls[0].ball_logic(paddles), balls[1].ball_logic(paddles)]

                if bounced[0] and walls_x[0] < 0:
                    walls_x[0] += 1

                if bounced[1] and walls_x[1] > 0:
                    walls_x[1] -= 1

                if players is not 2 and bounced[0]:
                    d1 = c.calculate_path(
                        balls[0].xcor(),
                        balls[0].ycor(),
                        walls_x[0],
                        balls[0].x_vel,
                        balls[0].y_vel,
                        -340,
                        0,
                        paddles[0],
                        'last'
                    )[0][1]

                if players is 0 and bounced[1]:
                    d2 = c.calculate_path(
                        balls[1].xcor(),
                        balls[1].ycor(),
                        walls_x[1],
                        balls[1].x_vel,
                        balls[1].y_vel,
                        0,
                        340,
                        paddles[1],
                        'last'
                    )[0][1]

                if balls[0].xcor() >= walls_x[0] - 10:
                    balls[0].setx(walls_x[0] - 10)
                    bounces[0].append([balls[0].ycor(), 2, 15])
                    balls[0].x_vel *= -1

                if balls[1].xcor() <= walls_x[1] + 10:
                    balls[1].setx(walls_x[1] + 10)
                    bounces[1].append([balls[1].ycor(), 2, 15])
                    balls[1].x_vel *= -1

                for bounce in bounces_to_delete:
                    bounces[bounce[0]].pop(bounce[1])
                bounces_to_delete.clear()

                for i in range(len(bounces)):
                    turtles[i].clear()
                    turtles[i].setx(walls_x[i])
                    for bounce in bounces[i]:
                        if bounce[2] < 0:
                            bounces_to_delete.append([i, bounces[i].index(bounce)])
                            continue

                        turtles[i].penup()
                        turtles[i].sety(bounce[0] + (bounce[1] / 2))
                        turtles[i].pencolor(f'#{hex_color[math.floor(bounce[2])] * 3}')
                        turtles[i].pendown()
                        turtles[i].sety(bounce[0] - (bounce[1] / 2))
                        if bounce[1] < 50:
                            bounce[1] += 1
                        else:
                            bounce[2] -= 1 / 5

                if balls[0].xcor() <= -410 or balls[1].xcor() >= 410:
                    if balls[0].xcor() <= -410 and balls[1].xcor() >= 410:
                        return 'Tie'
                    n = bool_to_num(balls[0].xcor() >= 410) - bool_to_num(balls[1].xcor() <= -410)
                    n += bool_to_num(n is -1) + 1
                    if players is 0:
                        return f'CPU {n} wins'
                    if n is 1 and players is 1:
                        return 'CPU wins'
                    return f'Player{n} wins'

                if d1 is not None:
                    move(paddles[0], 0, math.copysign(PADDLE_SPEED, d1 - paddles[0].ycor()), y_min=-250, y_max=250)()

                if d2 is not None:
                    move(paddles[1], 0, math.copysign(PADDLE_SPEED, d2 - paddles[1].ycor()), y_min=-250, y_max=250)()

                handler.run()
                screen.update()
                while time() - tm < 0.005:
                    pass
        while True:
            if pause_button.paused:
                handler.run('space')
                screen.update()
                continue
            t = time()

            ball.ball_logic(paddles)
            
            if players is not 2:
                c1 = calculate_ball_path(ball, -340, 390, paddles[1])[0][1]

            if players is 0:
                c2 = calculate_ball_path(ball, -390, 340, paddles[0])[0][1]

            if abs(ball.xcor()) >= 410:
                result = bool_to_num(ball.xcor() >= 410) - bool_to_num(ball.xcor() <= -410)
                result += bool_to_num(result is -1)
                scores[abs(result - 1)] += 1
                if abs(ball.x_vel) > 45:
                    scores[result] += 1
                ball.new_round()
                writer.clear()
                writer.write_text(scores[0], x=-50, y=200, size=50, color="white")
                writer.write_text(scores[1], x=50, y=200, size=50, color="white")
                if scores[0] is 7 and scores[1] is 7:
                    match_result = tiebreaker()

                if scores[0] is 7:
                    if players is 0:
                        match_result = 'CPU 1 wins'
                    if players is 1:
                        match_result = 'CPU wins'
                    if players is 2:
                        match_result = 'Player 1 wins'

                if scores[1] is 7:
                    if players is 0:
                        match_result = 'CPU 2 wins'
                    if players is 1:
                        match_result = 'You win'
                    if players is 2:
                        match_result = 'Player 2 wins'

            if match_result is not None:
                match_result += '!'
                break

            if c1 is not None:
                move(paddles[0], 0, math.copysign(PADDLE_SPEED, c1 - paddles[0].ycor()), y_min=-250, y_max=250)()

            if c2 is not None:
                move(paddles[1], 0, math.copysign(PADDLE_SPEED, c2 - paddles[1].ycor()), y_min=-250, y_max=250)()

            handler.run()
            screen.update()
            while time() - t < 0.005:
                pass
        for turtle in screen.turtles():
            turtle.reset()
            turtle.ht()
        Writer(0, 0).write_text(match_result, size=50, color="white", y=-50 / 2)
        screen.exitonclick()
    return func

buttons = [
    Button(screen, (0, -100), 75, 40, 'watch', start(0), 'white', 15, 'black'),
    Button(screen, (-100, 0), 100, 40, '1 player', start(1), 'white', 15, 'black'),
    Button(screen, (100, 0), 100, 40, '2 players', start(2), 'white', 15, 'black')
]

while buttons[0].should_check and buttons[1].should_check and buttons[2].should_check:
    screen.update()
