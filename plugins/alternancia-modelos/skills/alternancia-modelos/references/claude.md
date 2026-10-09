# Adaptador: Claude

## Claude Code

1. Comprueba la herramienta de agentes disponible y su esquema. En versiones que
   admiten selección por invocación, usa su parámetro `model` con un alias o ID
   admitido por esa sesión. No supongas que un alias de documentación está
   habilitado para esa cuenta, proveedor o versión.
2. Mantén la conversación principal como orquestador. Invoca un agente general
   adecuado o el agente del plugin `alternancia-modelos:especialista` cuando esté
   disponible. Incluye el contrato completo en el prompt de la llamada.
3. El agente incluido usa `model: inherit` como valor seguro por defecto. Para
   alternar, selecciona explícitamente otro modelo disponible por invocación si
   el entorno lo permite. Si se hereda el mismo, registra delegación sin alternancia.
4. Comprueba el modelo efectivo mediante los resultados o el estado de la tarea
   cuando estén disponibles. La configuración administrada, variables del
   entorno o una redirección pueden sustituir el modelo solicitado.
5. Si una configuración impide el override, respétala. No modifiques variables ni
   ajustes del usuario para eludirla. `/model` es un control del cliente; no
   escribas ese texto como si ejecutara un cambio desde una herramienta.

El skill se ejecuta en el contexto principal. No usa `context: fork` ni un modelo
fijo en su frontmatter, porque la decisión depende de la tarea y la sesión.

## Claude web y Cowork

La instalación de un skill/plugin y la disponibilidad de subagentes son cuestiones
distintas. Tras cargarlo, comprueba las herramientas expuestas realmente. Aplica
la misma selección nativa si existe; en caso contrario, ejecuta con el modelo
actual e informa del límite cuando proceda. No presupongas equivalencia con Code.

## Fuentes oficiales

- [Subagentes y selección de modelo](https://code.claude.com/docs/en/sub-agents)
- [Referencia del manifiesto](https://code.claude.com/docs/en/plugins-reference)
- [Instalación de plugins](https://code.claude.com/docs/en/discover-plugins)

Documentación consultada al preparar v1.0.0: 2026-10-09. La herramienta expuesta
en ejecución determina los parámetros utilizables, no esta fecha.
