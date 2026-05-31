from dataclasses import dataclass
from enum import Enum, auto


class TokenKind(Enum):
    WHEN = auto()
    EVERY = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    DO = auto()
    END = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    TRUE = auto()
    FALSE = auto()
    ON = auto()
    OFF = auto()

    MODO = auto()
    COLOR = auto()

    SENSOR = auto()  # sensor_temp, sensor_luz, etc.
    ACTUATOR = auto()  # foco_entrada, aire_acondicionado, etc.
    ATTRIBUTE = auto()  # .estado, .brillo, etc. (incluye el punto)

    NUMBER = auto()  # 25, 80, 100, etc.
    TEMP = auto()  # 25°C
    PERCENT = auto()  # 80%
    LUX = auto()  # 600lux
    TIME_DURATION = auto()  # 30m, 10s, 1h
    HORA = auto()  # 22:00
    FECHA = auto()  # 21/04/2026
    STRING = auto()  # "texto"
    EMAIL = auto()  # alguien@dominio.com

    EQUAL = auto()  # ==
    NEGATE = auto()  # !=
    GREATER = auto()  # >
    LESSER = auto()  # <
    GREAT_EQUAL = auto()  # >=
    LESS_EQUAL = auto()  # <=
    ASSIGN = auto()  # =

    LPAREN = auto()  # (
    RPAREN = auto()  # )

    EOF = auto()
    ERROR = auto()


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    src: str
    row: int
    col: int

    def __repr__(self):
        return f"\033[92mToken\033[0m(\033[93m{self.kind.name}\033[0m, \033[96m'{self.src}'\033[0m, línea={self.row}, col={self.col})"


PALABRAS_RESERVADAS = {
    "when": TokenKind.WHEN,
    "every": TokenKind.EVERY,
    "if": TokenKind.IF,
    "then": TokenKind.THEN,
    "else": TokenKind.ELSE,
    "do": TokenKind.DO,
    "end": TokenKind.END,
    "and": TokenKind.AND,
    "or": TokenKind.OR,
    "not": TokenKind.NOT,
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
    "on": TokenKind.ON,
    "off": TokenKind.OFF,
}

PREFIJOS_SENSOR = (
    "sensor_temp",
    "sensor_luz",
    "sensor_movimiento",
    "sensor_humo",
    "sensor_humedad",
)

PREFIJOS_ACTUADOR = (
    "foco_",
    "aire_",
    "persiana_",
    "cerradura_",
    "reloj_",
    "altavoz_",
    "alarma_",
)

ATRIBUTOS_VALIDOS = {
    ".estado",
    ".brillo",
    ".color",
    ".modo",
    ".temp_obj",
    ".temp_act",
    ".posicion",
    ".hora",
    ".fecha",
    ".volumen",
    ".mute",
    ".mensaje",
    ".email_notif",
    ".activada",
}
