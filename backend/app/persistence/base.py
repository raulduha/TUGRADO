from sqlalchemy import CheckConstraint, Enum, MetaData
from sqlalchemy.orm import DeclarativeBase

# Nombres de constraints deterministas para que Alembic genere migraciones estables.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def enum_column(enum_cls: type) -> Enum:
    # Se guarda el valor (`in_progress`), no el nombre del miembro. La restricción CHECK se
    # declara aparte con `enum_check` para que Alembic no la duplique.
    return Enum(
        enum_cls,
        native_enum=False,
        create_constraint=False,
        length=40,
        values_callable=lambda e: [m.value for m in e],
    )


def enum_check(column: str, enum_cls: type, name: str) -> CheckConstraint:
    values = ", ".join(f"'{m.value}'" for m in enum_cls)
    return CheckConstraint(f"{column} IN ({values})", name=name)
