from math        import cos, sin, pi
from tkinter     import Canvas
from dataclasses import dataclass

from matrices import Matrix

@dataclass
class H2O:
    position: tuple
    rotation: int = 0

    o_size: int = 30
    h_size: int = 16

    rotation_rate: int = 1
    rotation_range: tuple = (-30, 30)

    velocity: tuple = (-1, 1)

    def __post_init__(self) -> None:
        self.start_rotation = self.rotation

    def render(self, canvas: Canvas) -> None:
        canvas.create_oval(self.position[0] - int(self.o_size / 2), self.position[1] - int(self.o_size / 2), self.position[0] + int(self.o_size / 2), self.position[1] + int(self.o_size / 2), width=1, fill="red")

        position = (Matrix([[-int(self.o_size / 2) - int(self.h_size / 2), 0]])@self.getRotationMatrix(30)).matrix[0]
        canvas.create_oval(self.position[0] + position[0] - int(self.h_size / 2), self.position[1] + position[1] - int(self.h_size / 2), self.position[0] + position[0] + int(self.h_size / 2), self.position[1] + position[1] + int(self.h_size / 2), width=1, fill="white")

        position = (Matrix([[int(self.o_size / 2) + int(self.h_size / 2), 0]])@self.getRotationMatrix(-30)).matrix[0]
        canvas.create_oval(self.position[0] + position[0] - int(self.h_size / 2), self.position[1] + position[1] - int(self.h_size / 2), self.position[0] + position[0] + int(self.h_size / 2), self.position[1] + position[1] + int(self.h_size / 2), width=1, fill="white")

    def update(self, canvas: Canvas) -> None:
        if self.rotation - self.start_rotation >= self.rotation_range[1] or self.rotation - self.start_rotation <= self.rotation_range[0]:
            self.rotation_rate = -self.rotation_rate

        self.rotation += self.rotation_rate

        if self.rectangle[0] <= 0 or self.rectangle[2] >= int(canvas["width"]):
            self.velocity = (-self.velocity[0], self.velocity[1])

        if self.rectangle[1] <= 0 or self.rectangle[3] >= int(canvas["height"]):
            self.velocity = (self.velocity[0], -self.velocity[1])

        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.render(canvas)


    def getRotationMatrix(self, angle: int) -> Matrix:
        angle = (angle + self.rotation) * pi / 180

        return Matrix([
            [cos(angle), -sin(angle)],
            [sin(angle),  cos(angle)],
        ])
    
    @property
    def rectangle(self) -> tuple:
        return (
            self.position[0] - self.h_size - int(self.o_size / 2),
            self.position[1] - self.h_size - int(self.o_size / 2),
            self.position[0] + self.h_size + int(self.o_size / 2),
            self.position[1] + self.h_size + int(self.o_size / 2)
        )
