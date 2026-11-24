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
    def smooth_change_speed(self, target_left: float, target_right: float, step: float = 5.0) -> None:

        """Плавно изменяет скорость двигателей до заданных значений."""

        """Args:
            target_left: Целевая скорость левого двигателя (в %).
            target_right: Целевая скорость правого двигателя (в %).
            step: Шаг изменения скорости за одну итерацию (по умолчанию 5.0%).
        """
        # Гарантируем, что шаг изменения скорости всегда положительный,
        # даже если пользователь передал отрицательное число (например, -5.0)
        step = abs(step)

        # Повторяем цикл до тех пор, пока разница между текущей и целевой скоростью
        # хотя бы для одного из моторов превышает размер одного шага
        while (
            abs (self.left_motor.speed - target_left) > step
            or abs(self.right_motor.speed - target_right) > step
        ):
            # Сдвигаем скорость левого мотора на один шаг ближе к цели
            self._approach(self.left_motor, target_left, step)
            # Сдвигаем скорость правого мотора на один шаг ближе к цели
            self._approach(self.right_motor, target_right, step)
            # Выводим в консоль промежуточные значения скорости обоих моторов
            self.print_state()

        # Финальная доводка: когда до цели осталось меньше одного шага,
        # устанавливаем точные целевые значения, чтобы избежать погрешностей
        self.left_motor.set_speed(target_left)
        self.right_motor.set_speed(target_right)
        # Выводим финальное (достигнутое) состояние двигателей
        self.print_state()


    @staticmethod
    def _approach(motor: Motor, target: float, step: float) -> None:
        """Вспомогательный метод: делает ровно один шаг изменения скорости для одного мотора."""
        # Вычисляем разницу между желаемой и текущей скоростью.
        # Положительное число — нужно разгоняться, отрицательное — тормозить или ехать назад
        difference = target - motor.speed

        # Если оставшаяся разница меньше или равна шагу, сразу ставим целевую скорость,
        # чтобы не «проскочить» нужное значение
        if abs(difference) <= step:
            motor.set_speed(target)
        else:
            # Определяем знак изменения: +1 для увеличения скорости, -1 для уменьшения
            direction = 1 if difference > 0 else -1
            # Прибавляем или отнимаем один шаг от текущей скорости мотора
            motor.set_speed(motor.speed + direction * step)


    def print_state(self) -> None:
        """Выводит текущую скорость обоих двигателей с точностью до одного знака после запятой."""
        print(
            f"Левый двигатель: {self.left_motor.speed:.1f}%, "
            f"правый двигатель: {self.right_motor.speed:.1f}%"
        )


def main() -> None:
    """Основная функция: инициализирует робота и запускает цикл чтения команд."""
    # Создаём контроллер робота и передаём в него два объекта двигателей
    robot = RobotMotorsControl(
        left_motor=Motor("Левый"),
        right_motor=Motor("Правый"),
    )

    # Оборачиваем цикл в try...except для безопасной остановки моторов при прерывании (Ctrl+C)
    try:
        # Бесконечный цикл опроса команд пользователя из консоли
        while True:
            # Считываем ввод, убираем пробелы по краям (.strip()) и приводим к нижнему регистру (.lower())
            command = (
                input(
                    "Введите команду (forward, backward, left, right, stop, exit): "
                )
                .strip()
                .lower()
            )

            if command == "forward":
                # Движение вперёд: оба мотора плавно разгоняются до 80%
                robot.smooth_change_speed(80, 80)
            elif command == "backward":
                # Движение назад: оба мотора плавно раскручиваются в обратную сторону (-80%)
                robot.smooth_change_speed(-80, -80)
            elif command == "left":
                # Танковый разворот влево на месте: левое колесо назад (-50%), правое вперёд (50%)
                robot.smooth_change_speed(-50, 50)
            elif command == "right":
                # Танковый разворот вправо на месте: левое колесо вперёд (50%), правое назад (-50%)
                robot.smooth_change_speed(50, -50)
            elif command == "stop":
                # Экстренная остановка: мгновенно сбрасывает скорость без плавного замедления
                robot.stop()
                robot.print_state()
            elif command == "exit":
                # Останавливаем двигатели перед выходом и прерываем цикл через break
                robot.stop()
                print("Робот остановлен. Завершение работы.")
                break
            else:
                # Обработка опечаток или несуществующих команд
                print("Неизвестная команда. Попробуйте ещё раз.")

    # Перехватываем принудительную остановку скрипта с клавиатуры (Ctrl+C)
    except KeyboardInterrupt:
        # Аварийно глушим двигатели, чтобы робот не продолжал движение неуправляемо
        robot.stop()
        print("\nРобот остановлен.")


# Точка входа: функция main() запустится только если файл запущен напрямую,
# а не импортирован как модуль в другую программу
if __name__ == "__main__":
    main()
