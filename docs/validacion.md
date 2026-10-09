# Validación de v1.0.0

Comprobaciones realizadas el 2026-10-09:

- Validador local: correcto.
- Cinco pruebas de empaquetado: correctas.
- Claude Code 2.1.295: manifiesto del plugin, marketplace y directorio de agentes
  aceptados por `claude plugin validate`, sin advertencias.
- No se ha probado la alternancia en vivo ni se han consumido llamadas a modelos.

Codex CLI 0.159.0-alpha.3 está disponible en el entorno de construcción. Los
comandos de instalación documentados se contrastaron con su ayuda integrada. El
primer intento de lectura del paquete mediante app-server no llegó a cargar el
plugin porque el directorio de estado del entorno es de solo lectura. Esto no
acredita ni un fallo del paquete ni su aceptación por el cargador de Codex.

## Comprobaciones automatizadas

`python scripts/validate.py` comprueba la estructura del paquete, identidad y
versiones de manifiestos, destinos del marketplace, referencias locales del skill
y ausencia de enlaces simbólicos en el contenido distribuido. Es una validación
del contrato usado por este proyecto, no un sustituto de todos los validadores
oficiales ni una prueba de comportamiento de los modelos.

`python -m unittest discover -s tests -v` verifica que el empaquetado conserva las
referencias y manifiestos, excluye el archivo histórico y es reproducible. Incluye
casos negativos de referencias rotas, versiones divergentes y enlaces simbólicos.

`python scripts/build.py` ejecuta la validación y construye los dos ZIP. Ambos
contienen un único directorio raíz `alternancia-modelos/`.

## Prueba de aceptación por cliente

1. Instala el plugin en una sesión de prueba y comprueba que aparece el skill.
2. Ejecuta una tarea trivial: no debe delegar innecesariamente.
3. Ejecuta una tarea que se beneficie de un especialista con un modelo disponible.
4. Comprueba la llamada real y el modelo efectivo si el host lo informa.
5. Verifica la reintegración contra una fuente o prueba independiente.
6. Comprueba que una tarea con salida JSON estricta no recibe texto adicional.

Usa [los escenarios](../evals/README.md) para ampliar la aceptación. Una estructura
válida no acredita alternancia en vivo. La capacidad depende de la versión del
cliente, la cuenta, los modelos y las herramientas expuestas en esa sesión.

No se incluyen resultados fabricados de ejecuciones multi-modelo. Las pruebas
automáticas de archivos y empaquetado no llaman a modelos ni consumen cuotas.
