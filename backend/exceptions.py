import datetime


class BaseError(Exception):
    eng: str
    ru: str

    def __init__(self, eng: str, ru: str) -> None:
        self.eng = eng
        self.ru = ru
        super().__init__(eng)


class ObjectNotFound(BaseError):
    def __init__(self, obj: type, obj_id_or_name: int | str):
        super().__init__(
            f"Object {obj.__name__} {obj_id_or_name=} not found",
            f"Объект {obj.__name__}  с идентификатором {obj_id_or_name} не найден",
        )


class AlreadyExists(BaseError):
    def __init__(self, obj: type, obj_id_or_name: int | str):
        super().__init__(
            f"Object {obj.__name__}, {obj_id_or_name=} already exists",
            f"Объект {obj.__name__} с идентификатором {obj_id_or_name=} уже существует",
        )


class MissingParameters(BaseError):
    def __init__(self, param_name: str):
        super().__init__(
            f"Missing parameter {param_name}",
            f"Параметр {param_name} отсутствует в запросе",
        )


class InvalidParameters(BaseError):
    def __init__(self, param_name: str):
        super().__init__(
            f"Invalid parameter {param_name}",
            f"Параметр {param_name} не корректен",
        )
