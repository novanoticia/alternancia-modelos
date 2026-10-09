---
name: alternancia-modelos
description: >
  Protocolo de ejecución que orquesta varios modelos frontera por roles — razonador
  primario, secundario especialista y fallback = primario — aplicable a cualquier tarea
  sin cambiar su contenido: verificación online de salvaguardas y cuotas antes de delegar,
  delegación solo como escalada, respeto absoluto a las salvaguardas (una redirección es
  normal, no un error), contrato de subagente, reintegración con re-verificación y
  model-usage log. Extraído del sistema de orquestación de github-plugin-analyzer-ia-v4.
  Actívalo con "/alternancia-modelos", "usa alternancia de modelos", "orquesta modelos",
  "ejecuta con orquestación de modelos", "delega en varios modelos", "aplica el protocolo
  multi-modelo", o cuando el usuario pida ejecutar una tarea o prompt con alternancia de
  modelos. También se activa si un prompt incluye una sección de "alternancia de modelos"
  o "protocolo de ejecución multi-modelo" y pide seguirla.
---

# Alternancia de Modelos — protocolo de orquestación por roles

Aplicar este protocolo **a la tarea en curso**: gobierna **cómo** se ejecuta (qué modelo
corre qué tramo), nunca **qué** produce. No alterar el contenido, formato ni criterios del
prompt anfitrión; añadirle solo esta disciplina de ejecución.

**Idioma:** toda la salida cara al usuario en español.

## Paso 0 — Comprobar el entorno (gate)

Verificar si existe un mecanismo de subagentes con selección de modelo (p. ej. la
herramienta Agent de Claude Code / Cowork con override `model`). Si **no** existe:
**degradación elegante** — ejecutar toda la tarea en el modelo actual y declararlo en la
sección de límites del entregable. Nunca simular una delegación que no ocurrió (ni
inventar un model-usage log).

## Paso 1 — Roles, no nombres de producto

Enrutar por **rol**, nunca por nombre fijo de modelo — los nombres caducan, los roles no:

- **Razonador primario (por defecto para todo el flujo).** El modelo más capaz que además
  maximice la *continuidad*: el menos propenso a agotar cuota, cerrar su ventana de
  disponibilidad o sufrir una redirección por salvaguardas a mitad de tarea. Ejecuta
  análisis **e** implementación por defecto.
- **Secundario / especialista (selectivo).** Un modelo frontera complementario, invocado
  **solo** para los tramos más difíciles, ambiguos y de varios pasos — y solo cuando está
  permitido, le queda cuota y aporta valor de razonamiento claro.
- **Fallback = primario.** Si el secundario es bloqueado, redirigido por sus propias
  salvaguardas o agota cuota/ventana, ese tramo continúa en el primario **sin detener el
  flujo**.

## Paso 2 — Verificar restricciones online (antes de enrutar y ante cualquier bloqueo)

Las restricciones de los modelos cambian rápido. Antes de delegar, leer
**`references/ejemplo-fechado.md`** y seguir su procedimiento: buscar en la web, para cada
modelo candidato, (a) temas permitidos vs. bloqueados/redirigidos, (b) cuota y ventana de
disponibilidad, (c) destino de la redirección cuando salta una salvaguarda.

Sin acceso web: usar el ejemplo fechado del fichero de referencia **y declarar la
suposición en la sección de límites** — nunca presentar política posiblemente caducada
como hecho vigente.

## Paso 3 — Delegar solo como escalada

Si una sola pasada basta, **no delegar** (*mind your own footprint*). Delegar cuando se
cumpla al menos una condición:

- la superficie de alto valor excede lo que cabe en una pasada con profundidad;
- el nivel de esfuerzo pedido es alto (revisión o diseño profundo) sobre un objeto no trivial;
- hay que analizar o comparar muchas partes a la vez.

## Paso 4 — Reglas de enrutado (prioridad de continuidad)

- Por defecto, **todo el flujo corre en el primario**.
- Escalar al secundario solo tramos **acotados, permitidos y de alto valor**.
- Cualquier bloqueo / redirección / agotamiento de cuota → el tramo cae al primario sin
  parar el flujo.
- No cambiar de modelo sin valor claro.
- **Nunca esquivar una salvaguarda.** Si un tema legítimo (p. ej. análisis de seguridad o
  secure-coding) dispara un clasificador, aceptar la redirección y continuar en el modelo
  que el proveedor asigne. Las salvaguardas se honran, no se derrotan: una redirección es
  comportamiento normal, no un error.

## Paso 5 — Contrato no negociable del subagente

Todo subagente hereda el protocolo, no un folio en blanco:

1. Recibe las **reglas y el método completos** del prompt anfitrión; no puede colapsar
   pasos ni saltarse la verificación propia de la tarea.
2. Recibe su **alcance exacto**: qué sección/eje y qué material posee.
3. **Forma de salida:** resultados ya etiquetados según los criterios del prompt anfitrión
   (severidad, confianza, evidencia — o los equivalentes de la tarea), anclados a fuente
   concreta (`archivo:línea`, `función()`, sección, dato). Sin ancla, el resultado se
   descarta.
4. **NO redacta el entregable final** ni inventa secciones: devuelve material crudo al
   orquestador.

## Paso 6 — Reintegración

Fusionar lo devuelto por los subagentes y **repetir la pasada de autoverificación sobre el
conjunto combinado** (deduplicar, resolver contradicciones entre subagentes, recalibrar
confianzas) antes de redactar el entregable único. La delegación jamás elude la
verificación final del prompt anfitrión.

## Paso 7 — Registro y transparencia

- Mantener un **model-usage log** breve: qué tramo corrió en qué modelo y por qué
  (valor / bloqueo / redirección / cuota).
- Divulgar en la sección de límites del entregable qué partes se delegaron, más el log.
  Si el entregable no tiene sección de límites, añadir una breve al final.
- **Restricción de nombrado:** en la salida cara al usuario nunca nombrar un modelo
  concreto como "el motor" del razonamiento; los nombres solo pueden aparecer como
  configuración de enrutado o como contextos de uso compatibles. Describir lo delegado
  como "análisis delegado a un proceso de razonamiento auxiliar".

## Recordatorios finales

- Este protocolo se **compone** con el prompt anfitrión; ante conflicto sobre el
  contenido del entregable, manda el prompt anfitrión; sobre el enrutado de modelos,
  manda este protocolo.
- Leer `references/ejemplo-fechado.md` **solo cuando se vaya a delegar de verdad** —
  contiene el procedimiento de verificación online, el ejemplo fechado con nombres
  concretos, el mapeo `model` para Claude/Cowork y cómo incorporar modelos futuros.
