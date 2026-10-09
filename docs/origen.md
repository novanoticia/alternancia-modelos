# Procedencia y adaptación

Fuente: `alternancia-modelos.zip`, aportado por el usuario para crear este proyecto.
Los dos documentos originales se conservan sin modificaciones en `upstream/`.
Son un archivo histórico: no se instalan ni se cargan como instrucciones activas.
La huella del ZIP original se registra en `upstream/SHA256SUMS`.

El original propone principal, especialista y respaldo; delegación selectiva;
contrato de subagente; reintegración; y registro de uso. La adaptación conserva
esas ideas y añade:

1. Detección explícita de capacidades para Claude, ChatGPT/Codex y otros clientes.
2. Prioridades de calidad, coste o rapidez y un presupuesto de llamadas acotado.
3. Diferenciación entre cuota, fallos de transporte y negativas por seguridad.
4. Cuota de cuenta y modelo efectivo como datos desconocidos cuando no se observan.
5. Compatibilidad con respuestas de formato cerrado y tareas creativas.
6. Respeto del idioma del encargo y de las instrucciones de mayor prioridad.
7. Prevención de efectos duplicados al recuperar trabajos con timeout.

El ejemplo fechado del original contiene asignaciones concretas y afirmaciones
sobre ventanas de uso. No se adopta como catálogo vigente ni como fuente de cuota
real. Tampoco se declara falso: simplemente queda fuera de la configuración y se
sustituye por comprobaciones actuales de cada sesión.

La creación de este repositorio no constituye una ejecución del protocolo de
alternancia. Los originales se han leído como material para editar y empaquetar.
