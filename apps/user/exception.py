from pydantic_core import PydanticCustomError


def duplicate_username(name: str):
    return PydanticCustomError(
        "Duplicate data",
        f"Пользователь с именем {name} уже существует"  # noqa
    )


def incorrect_email(email: str):
    return PydanticCustomError(
        'Incorrect data',
        f'Email {email} некорректный'  # noqa
    )


incorrect_password = PydanticCustomError(
    "Incorrect data",
    "Некорректный пароль. Пароль должен содержать 8-100 символов, 1 латинскую "  # noqa
    "букву в верхнем и нижнем регистре и 1 спец символ"
)
