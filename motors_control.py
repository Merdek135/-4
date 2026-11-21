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
        self.left_motor.set_speed(left_speed)
        self.right_motor.set_speed(right_speed)

    def smooth_change_speed(self, target_left: float, target_right: float, step: float = 5.0) -> None:
        """Плавно изменяет скорость двигателей до заданных значений."""
        step = abs(step)

        while (
            abs(self.left_motor.speed - target_left) > step
            or abs(self.right_motor.speed - target_right) > step
        ):
            self._approach(self.left_motor, target_left, step)
            self._approach(self.right_motor, target_right, step)
            self.print_state()

        self.left_motor.set_speed(target_left)
        self.right_motor.set_speed(target_right)
        self.print_state()

    @staticmethod
    def _approach(motor: Motor, target: float, step: float) -> None:
        difference = target - motor.speed

        if abs(difference) <= step:
            motor.set_speed(target)
        else:
            direction = 1 if difference > 0 else -1
            motor.set_speed(motor.speed + direction * step)

    def print_state(self) -> None:
        print(
            f"Левый двигатель: {self.left_motor.speed:.1f}%, "
            f"правый двигатель: {self.right_motor.speed:.1f}%"
        )


def main() -> None:
    robot = RobotMotorsControl(
        left_motor=Motor("Левый"),
        right_motor=Motor("Правый"),
    )

    try:
        while True:
            command = input(
                "Введите команду (forward, backward, left, right, stop, exit): "
            ).strip().lower()

            if command == "forward":
                robot.smooth_change_speed(80, 80)
            elif command == "backward":
                robot.smooth_change_speed(-80, -80)
            elif command == "left":
                robot.smooth_change_speed(-50, 50)
            elif command == "right":
                robot.smooth_change_speed(50, -50)
            elif command == "stop":
                robot.stop()
                robot.print_state()
            elif command == "exit":
                robot.stop()
                print("Робот остановлен. Завершение работы.")
                break
            else:
                print("Неизвестная команда. Попробуйте ещё раз.")
    except KeyboardInterrupt:
        robot.stop()
        print("\nРобот остановлен.")


if __name__ == "__main__":
    main()
