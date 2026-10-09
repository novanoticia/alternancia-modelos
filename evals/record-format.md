# Registro de un par de evaluación

`scripts/compare_evals.py` clasifica un par según observaciones que tú aportas.
No ejecuta modelos, no puntúa respuestas, no calcula precios ni comprueba las fuentes
citadas. La calidad y las métricas deben proceder de evaluaciones y registros reales.

## Probar la herramienta

```sh
python scripts/compare_evals.py evals/examples/synthetic-pair.json
```

Ese archivo contiene **datos ficticios** y declara `synthetic: true`. Sirve para
demostrar el formato y probar el clasificador, no para demostrar que el plugin mejora
el trabajo. El resultado mantiene `source: synthetic`, incluso si clasifica el par
como `observed_benefit`.

## Registrar una comparación real

Crea un archivo distinto con la misma estructura y rellena los datos observados.
Usa `synthetic: false` únicamente para ejecuciones reales. No borres la marca del
ejemplo para convertir sus cifras en resultados. Los campos son obligatorios;
las medidas que no puedas observar se expresan como `null`, nunca como cero.

- `experiment_id`, `task_id`, `pair_id`: identificadores estables del experimento,
  tarea y repetición. Cada invocación compara exactamente un par.
- `policy`: umbrales fijados **antes de ejecutar**, no ajustados para favorecer un
  resultado. `min_quality_gain` debe superar `equivalence_margin`; ambos usan la
  escala de calidad de 0 a 100. Los porcentajes limitan el incremento admisible
  respecto a la referencia. Los límites absolutos son opcionales (`null`).
- `resource_metric`: `tokens` o `cost`. En modo `cost`, `policy.currency` debe
  identificar la moneda del presupuesto y coincidir con la de ambos registros.
  En modo `tokens`, usa `currency: null` en la política. Los tokens no equivalen
  automáticamente a dinero, y la comparación solo evalúa la métrica seleccionada.
- `runs.native` y `runs.plugin`: observaciones de cada condición. El `setup` debe
  coincidir en host y versión, modelo principal, esfuerzo, contexto, catálogo de
  modelos, herramientas, rúbrica y presupuesto. Los identificadores deben representar
  configuraciones archivadas e iguales, no solo etiquetas iguales.
- `native_delegation_allowed`: conserva `true` en las dos condiciones. Este comparador
  está dirigido a experimentos donde puede mantenerse disponible la delegación nativa;
  no admite como referencia una ejecución con delegación desactivada artificialmente.
- `quality`: puntuación de 0 a 100 según la misma rúbrica predefinida, o `null`.
  La herramienta no convierte opiniones en evidencia ni verifica quién puntuó.
- `completed` y `requirements_met`: ejecución terminada y cumplimiento de todos los
  requisitos obligatorios, respectivamente. Una puntuación alta no compensa un requisito
  incumplido. Una ejecución incompleta produce `inconclusive`.
- `wall_seconds`, `tokens`, `cost`, `calls`: totales del flujo, incluyendo principal,
  especialistas, reintentos y revisión. Usa números no negativos, enteros para tokens
  y llamadas, y `null` cuando falten. `currency` es obligatorio si se declara un coste.
- `models_observed`: solo identificadores confirmados; usa `[]` si no se conocen.
- `evidence`: referencias a resultados, pruebas, rúbricas y registros que permiten
  revisar las cifras. No incluyas secretos ni datos privados innecesarios. La herramienta
  no abre esas referencias ni acredita su autenticidad.

## Interpretar el resultado

| `status` | Significado para ese par |
| --- | --- |
| `observed_benefit` | Cumple una de las dos condiciones de mejora según datos y umbrales aportados. |
| `regression` | Incumple requisitos o límites absolutos, o pierde calidad más allá del margen aceptado. |
| `no_clear_benefit` | Datos comparables y suficientes, pero no satisfacen las condiciones de mejora. |
| `inconclusive` | Faltan observaciones o las condiciones/monedas no permiten comparar. |

En la segunda condición de mejora (calidad equivalente con menos recursos), el
clasificador exige reducir tiempo o la métrica de consumo elegida sin aumentar
la otra. En la primera permite los incrementos predefinidos para obtener más calidad.
También reconoce satisfacer los requisitos que la referencia incumplió, dentro
del incremento permitido. Los límites absolutos del usuario prevalecen siempre.

La salida distingue `synthetic` de `reported_observations` y fija `scope: single_pair`.
Un par no demuestra superioridad general ni significación estadística. Conserva todos
los pares, incluidos los desfavorables, y sigue el procedimiento de [evaluación](README.md).

La CLI devuelve código 0 para cualquier clasificación válida, incluido `regression`,
y código 2 para un archivo ilegible o un registro inválido. El código 0 solo significa
que pudo analizar el registro; **no significa que el plugin haya mejorado**.
