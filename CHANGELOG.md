# Cambios

## 1.2.0 — 2026-10-09

- QW1: validación YAML segura, claves duplicadas rechazadas, identidad del skill y
  presencia del especialista verificadas; versiones inválidas producen errores legibles.
- QW2: generación temporal de artefactos y rechazo de destinos con enlaces simbólicos;
  una generación fallida conserva los ZIP anteriores.
- CM1: comparador local de pares nativo/plugin con umbrales previos, condiciones
  equivalentes, presupuestos, monedas y valores desconocidos explícitos.
- 29 pruebas automatizadas; ejemplos de evaluación identificados como sintéticos.
- PyYAML 6.0.3 como dependencia de desarrollo; el plugin instalado sigue sin requerir Python.

## 1.1.0 — 2026-10-09

- Objetivo explícito: mejorar calidad verificable justificando tiempo y consumo.
- Calidad como prioridad predeterminada y criterios de aceptación antes de delegar.
- Presupuesto de llamadas identificado como provisional y ajustable.
- Procedimiento de comparación con el host sin plugin, conservando delegación nativa.
- Separación entre una tarea completada y una mejora demostrada por mediciones.

## 1.0.0 — 2026-10-09

- Primera adaptación portable del skill original de alternancia de modelos.
- Paquetes para Agent Plugins, Claude Code y Codex, más skill independiente.
- Detección de capacidades, delegación selectiva y registro de uso real.
- Presupuesto de llamadas, criterios de coste/calidad/rapidez y recuperación.
- Documentación, escenarios de aceptación y empaquetado reproducible.
