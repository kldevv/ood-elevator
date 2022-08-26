from enums import ButtonType


class Button:
    def __init__(self, level: int, btype: ButtonType):
        self.btype = btype
        self.level = level
        self.active = False

    def click(self) -> None:
        raise NotImplementedError("Click is not implemented in base class!")

    def register(self, elevator) -> None:
        raise NotImplementedError("Register is not implemented in base class!")

    def reset(self) -> None:
        self.active = False


class InternalButton(Button):
    def __init__(self, level):
        self.elevator = None

        super().__init__(level, ButtonType.IN)

    def click(self) -> None:
        if self.elevator is None:
            raise AttributeError("Button is not registered!")

        if self.active:
            return

        self.active = self.elevator.request(self.level, self.btype)

    def register(self, elevator) -> None:
        self.elevator = elevator


class ExternalButton(Button):
    def __init__(self, level):
        self.elevators = []

        super().__init__(level, ButtonType.EX)

    def click(self) -> None:
        if not len(self.elevators):
            raise AttributeError("Button is not registered!")

        if self.active:
            return

        for e in self.elevators:
            if e.request(self.level, self.btype):
                self.active = True
                break

    def register(self, elevator) -> None:
        self.elevators.append(elevator)
