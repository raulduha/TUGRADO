"""Error de negocio común a todos los módulos: un código estable y un mensaje para el usuario.

`app/api/errors.py` lo traduce a HTTP en un solo lugar.
"""


class AppError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
