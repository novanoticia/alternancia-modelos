# Adaptador: ChatGPT y Codex

El paquete contiene un manifiesto portable `plugin.json`, un manifiesto de
compatibilidad `.codex-plugin/plugin.json` y el skill compartido. El marketplace
del repositorio está en `.agents/plugins/marketplace.json`.

## Delegación nativa

1. Inspecciona las herramientas disponibles en esta sesión. Si hay creación de
   subagentes con selección de modelo, usa los nombres, enumeraciones y límites
   de ese esquema. No copies identificadores de Claude ni supongas un nombre
   universal para la herramienta.
2. Cuando exista `spawn_agent` con `model` y `fork_turns`, comprueba sus reglas:
   algunos entornos permiten override únicamente con `fork_turns: "none"`.
   En ese caso pasa de forma explícita el contrato y el contexto necesario.
   No envíes combinaciones de parámetros incompatibles ni dependas de herencia
   de contexto cuando has pedido un contexto vacío.
3. Si la interfaz expone roles configurados en lugar de un parámetro `model`, usa
   un rol ya configurado y comprueba qué modelo utiliza. No modifiques la
   configuración global ni el modelo principal para ejecutar este skill.
4. Si no hay selector de modelo, puede haber delegación al modelo heredado.
   Si no hay subagentes o no están permitidos, completa la tarea en el principal.
5. No uses herramientas de creación de chats para simular subagentes: pueden
   crear conversaciones visibles con un ciclo de vida distinto.

La invocación explícita de este skill pide delegación selectiva, pero no puede
anular prohibiciones del sistema, límites de cuenta ni permisos de la sesión.
No prometas compatibilidad universal entre ChatGPT web, Work, Codex CLI y la app.

## Instalación y distribución

Usa la vía de plugins/marketplaces que admita el cliente. Tener un repositorio
público no publica automáticamente el plugin en el directorio público de OpenAI.
Un entorno que solo admite MCP no ejecutará este skill por conectarlo como MCP:
este paquete no incluye un servidor ni un servicio de inferencia.

## Fuentes oficiales

- [Empaquetado e instalación](https://developers.openai.com/plugins/build/plugins)
- [Skills](https://developers.openai.com/codex/skills)
- [Subagentes](https://developers.openai.com/codex/subagents)

Documentación de empaquetado consultada: 2026-10-09. La compatibilidad de ejecución
se verifica con las herramientas de cada sesión.
