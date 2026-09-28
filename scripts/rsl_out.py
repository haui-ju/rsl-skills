"""Contrato de salida de los scripts RSL: la última línea es siempre `OK: …` o `ERROR: …`.

OK -> exit 0 · ERROR -> exit 1 (2 si es un uso incorrecto). Las líneas de detalle
(tablas, `  - …`, `WARN …`) van antes. Nunca se muestra un traceback.
"""
from __future__ import annotations

import sys
from typing import Callable

_closed = False


class Fail(Exception):
    """Aborta el script con `ERROR: msg. fix`."""

    def __init__(self, msg: str, fix: str | None = None, code: int = 1):
        super().__init__(msg)
        self.msg, self.fix, self.code = msg, fix, code


def _line(prefix: str, msg: str, tail: str | None) -> None:
    global _closed
    msg = " ".join(str(msg).split()).rstrip(". ")
    tail = " ".join(str(tail).split()).rstrip(". ") if tail else None
    print(f"{prefix}: {msg}." + (f" {tail}." if tail else ""), flush=True)
    _closed = True


def ok(msg: str, next_step: str | None = None) -> int:
    _line("OK", msg, f"Próximo paso: {next_step}" if next_step else None)
    return 0


def error(msg: str, fix: str | None = None, code: int = 1) -> int:
    _line("ERROR", msg, fix)
    return code


def run(main: Callable[[list[str]], int], argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    try:
        code = main(argv)
    except Fail as e:
        code = error(e.msg, e.fix, e.code)
    except SystemExit as e:
        if isinstance(e.code, str):
            code = error(e.code.removeprefix("error: ").removeprefix("error:"))
        else:
            code = e.code or 0
    except KeyboardInterrupt:
        code = error("interrumpido por el usuario")
    except PermissionError as e:
        code = error(f"sin permiso para escribir o leer {e.filename or 'un archivo'}", "revisa los permisos (chmod u+w) o el dueño del archivo")
    except OSError as e:
        code = error(f"error del sistema de archivos en {e.filename or 'un archivo'}: {e.strerror or e}", "revisa la ruta, el espacio en disco y los permisos")
    except Exception as e:  # noqa: BLE001
        code = error(f"fallo interno ({type(e).__name__}): {e}", "reporta el caso con rsl-qa-destroy")
    if not _closed:
        code = ok("terminado") if code == 0 else error("terminó con errores (ver detalle arriba)", code=code or 1)
    sys.exit(code)
