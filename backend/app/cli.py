"""Comandos de administración.

Crear o promover un administrador (no hay registro público de administradores):
    uv run python -m app.cli create-admin --email admin@ejemplo.cl
La contraseña se pide por consola, o se lee de ADMIN_PASSWORD (uso no interactivo).
"""

import argparse
import getpass
import os
import sys

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from app.auth.email import ConsoleEmailSender
from app.auth.passwords import PasswordPolicyError
from app.auth.service import AuthError, AuthService, normalize_email
from app.clock import utc_now
from app.config import get_settings
from app.db import get_engine
from app.persistence.auth_models import UserAccountRow


def _read_password() -> str:
    if os.environ.get("ADMIN_PASSWORD"):
        return os.environ["ADMIN_PASSWORD"]
    first = getpass.getpass("Contraseña: ")
    if getpass.getpass("Repite la contraseña: ") != first:
        raise SystemExit("Las contraseñas no coinciden")
    return first


def create_admin(email: str, engine: Engine | None = None) -> int:
    settings = get_settings()
    with Session(engine or get_engine()) as db:
        exists = db.scalars(
            select(UserAccountRow.id).where(UserAccountRow.email == normalize_email(email))
        ).first()
        password = None if exists else _read_password()
        service = AuthService(
            db=db,
            policy=settings.auth_policy(),
            clock=utc_now,
            email_sender=ConsoleEmailSender(),
            frontend_base_url=settings.frontend_base_url,
        )
        try:
            _, created = service.create_administrator(email, password)
        except (AuthError, PasswordPolicyError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    print("Administrador creado." if created else "Cuenta existente promovida a administrador.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    commands = parser.add_subparsers(dest="command", required=True)
    admin = commands.add_parser("create-admin", help="Crea o promueve un administrador")
    admin.add_argument("--email", required=True)
    args = parser.parse_args(argv)
    if args.command == "create-admin":
        return create_admin(args.email)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
