# Adaptador: otros entornos

Copia la carpeta completa `alternancia-modelos/` del directorio `skills/` al lugar
que el cliente use para Agent Skills. Mantén `SKILL.md` y `references/` juntos.
Si acepta el estándar Agent Plugins, usa el paquete con `plugin.json`.

Un cliente que solo permite instrucciones puede aplicar el protocolo leyendo el
skill y sus referencias, pero eso no le añade herramientas de delegación.

Mapea únicamente capacidades existentes:

| Capacidad observada | Comportamiento |
| --- | --- |
| Subagentes con modelos seleccionables | Alternancia nativa selectiva. |
| Subagentes sin selección de modelo | Delegación, sin asegurar alternancia. |
| Sin subagentes | Ejecución con el modelo actual. |
| Servicio externo de inferencia ya autorizado | Usarlo solo si están autorizados el destino, los datos y el gasto; verificar el contrato de la herramienta. |

Este paquete no implementa ese servicio externo. No llama a APIs, no instala SDKs
ni obtiene claves. Una futura integración deberá proporcionar selección real de
modelos, límites verificables, estado de trabajos y uso observado. La ausencia de
esas funciones nunca justifica simular resultados.
