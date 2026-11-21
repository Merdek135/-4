"""Простой симулятор управления двигателями робота."""

from dataclasses import dataclass


@dataclass
class Motor:
    name: str
    speed: float = 0.0

    def set_speed(self, speed: float) -> None:
        """Устанавливает скорость двигателя в диапазоне от -100 до 100."""
        self.speed = max(-100.0, min(100.0, speed))


class RobotMotorsControl:
    def __init__(self, left_motor: Motor, right_motor: Motor) -> None:
        self.left_motor = left_motor
        self.right_motor = right_motor

    def stop(self) -> None:
        self.left_motor.set_speed(0)
        self.right_motor.set_speed(0)

    def move(self, left_speed: float, right_speed: float) -> None:
        self.right_motor.set_speed(right_speed)
