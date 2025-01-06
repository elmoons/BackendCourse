class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class UserWithThisEmailAlreadyRegistered(NabronirovalException):
    detail = "Пользователь с таким email уже зарегистрирован"


class NoSuchRoomException(NabronirovalException):
    detail = "Номера не существует"


class CheckInDateLaterOutDate(NabronirovalException):
    detail = "Дата выезда не может быть раньше или равна дате заезда"
