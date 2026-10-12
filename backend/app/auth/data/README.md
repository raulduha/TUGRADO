# Contraseñas comunes

`common_passwords.txt` sirve para rechazar contraseñas comunes (FR-001, AC-032).

- Fuente: [SecLists](https://github.com/danielmiessler/SecLists) (licencia MIT), archivos
  `Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt` y
  `xato-net-10-million-passwords-1000000.txt`, descargados el 2026-10-12.
- Procesamiento: unión de ambas listas, solo entradas ASCII de 12 a 128 caracteres (las más
  cortas ya se rechazan por longitud), en minúsculas, sin duplicados y ordenadas.
- La comparación se hace sobre la contraseña en minúsculas.
