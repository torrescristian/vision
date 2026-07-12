# Hito A.0 - Tests Manuales

## Objetivo

Validar que la inicializacion base del proyecto funciona de punta a punta.

## Precondiciones

- Estar ubicado en la raiz del proyecto.
- Tener instalado uv.

## Casos

1. Verificar estructura del proyecto.

   Comando:

   find . -maxdepth 2 -type d | sort

   Resultado esperado:

   Existen las carpetas app, models, services, detectors, events, utils y tests.

2. Verificar ejecucion del programa principal.

   Comando:

   .venv/bin/python main.py

   Resultado esperado:

   Muestra en consola: Vision Engine inicializado

3. Verificar linter.

   Comando:

   .venv/bin/ruff check .

   Resultado esperado:

   All checks passed!

4. Verificar tipado.

   Comando:

   .venv/bin/pyright .

   Resultado esperado:

   0 errors.

5. Verificar tests.

   Comando:

   .venv/bin/pytest

   Resultado esperado:

   1 passed.

## Criterio de salida del hito

El Hito A.0 se considera completo cuando los 5 casos anteriores pasan sin errores.
