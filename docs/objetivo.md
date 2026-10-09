# Objetivo aprobado

> Mejorar la calidad verificable de las tareas mediante la selección y coordinación
> de los modelos disponibles, delegando solo cuando el beneficio esperado justifique
> el tiempo y consumo adicionales, dentro de los límites definidos por el usuario.

## Prioridad y alcance

La **calidad** es la prioridad predeterminada. El tiempo y el consumo son
restricciones ajustables, y el usuario puede cambiar la prioridad. El objetivo del
plugin es estable; el objetivo de cada tarea define qué resultado necesita el
usuario y qué significa hacerlo bien en ese caso.

El plugin debe:

1. Entender el resultado buscado y sus criterios de aceptación.
2. Evaluar si conviene delegar; continuar en el modelo actual cuando sea suficiente.
3. Asignar cada subtarea al modelo adecuado según capacidades disponibles,
   dificultad, contexto y restricciones.
4. Verificar el resultado conjunto mediante evidencias y criterios de aceptación,
   resolviendo discrepancias.
5. Medir su aportación frente a tareas equivalentes ejecutadas sin el plugin.

Usar más agentes o modelos no es una medida de éxito. Tampoco lo es reducir tokens
si se incumplen los requisitos de la tarea. La verificación se adapta al encargo:
pruebas para código, contraste de fuentes para afirmaciones y una rúbrica adecuada
para propuestas creativas.

## Criterio de éxito

El plugin aporta una mejora si obtiene:

- **Mejor calidad con un incremento aceptable de recursos**, o
- **Calidad equivalente con menos recursos**.

En ambos casos debe respetar los límites y requisitos del usuario. Los umbrales de
calidad, equivalencia y gasto aceptable se fijan antes de comparar, según la tarea.
No se impone una cifra universal sin evidencia.

La referencia es el mismo entorno **sin el plugin**, con su comportamiento nativo
de delegación disponible. Así se mide el valor añadido del protocolo, no solo la
diferencia entre uno y varios agentes. Si se desea una referencia estrictamente de
un solo agente, se añade como una condición aparte y se identifica como tal.

Consulta el [procedimiento de evaluación](../evals/README.md). Sin mediciones
comparables, la mejora sigue siendo una hipótesis. Las pruebas de empaquetado no
demuestran calidad de razonamiento, ahorro ni una asignación óptima de modelos.

## Decisiones provisionales

El máximo predeterminado de dos llamadas a especialistas y una simultánea es un
límite operativo heredado de la primera versión, no parte del objetivo ni una
regla óptima demostrada. Se conserva como valor ajustable hasta que las evaluaciones
justifiquen cambiarlo. Una petición con mayor presupuesto puede especificarlo.

Establecer este objetivo no inicia por sí mismo evaluaciones con modelos ni
autoriza gasto adicional. Cada evaluación real debe tener su alcance y presupuesto.
