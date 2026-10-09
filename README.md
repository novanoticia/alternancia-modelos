# Alternancia de modelos

Plugin portable para ejecutar tareas con un modelo principal y delegar subtareas
a otros modelos **cuando aportan valor y el entorno lo permite**. Basado en el
skill de Claude aportado por el autor del repositorio.

Mantiene el contexto de la conversación, comprueba las capacidades disponibles,
acota las delegaciones y revisa los resultados antes de incorporarlos. No requiere
claves API, dependencias en ejecución ni un servicio externo.

## Objetivo

> Mejorar la calidad verificable de las tareas mediante la selección y coordinación
> de los modelos disponibles, delegando solo cuando el beneficio esperado justifique
> el tiempo y consumo adicionales, dentro de los límites definidos por el usuario.

La calidad es la prioridad predeterminada; el tiempo y el consumo son límites
ajustables. El usuario puede cambiar esa prioridad. El protocolo parte del resultado
buscado y sus criterios de aceptación, decide si conviene delegar, asigna las
subtareas y verifica el resultado conjunto.

El éxito se evalúa frente al comportamiento nativo sin el plugin: mejor calidad
con un incremento aceptable de recursos, o calidad equivalente con menos recursos.
Hasta medirlo, la mejora es una hipótesis. Consulta el
[objetivo y sus criterios de éxito](docs/objetivo.md).

Para registrar comparaciones, usa el [comparador local](evals/record-format.md).
Rechaza condiciones incompatibles y distingue mediciones ausentes de valores cero;
los ejemplos incluidos son sintéticos y no acreditan mejoras reales.

## Uso

Después de instalarlo, pide:

> Usa alternancia de modelos para revisar este proyecto. Prioriza calidad y delega
> solo las comprobaciones que aporten valor.

También puedes indicar «prioriza coste», «prioriza rapidez» o un límite concreto
de delegaciones. Por defecto se prioriza la calidad, con un presupuesto provisional
de hasta dos llamadas a especialistas, una activa a la vez y sin delegación
recursiva. Este límite es ajustable y no se presenta como óptimo. No consume esas
llamadas si la tarea puede resolverse directamente.

## Compatibilidad real

| Entorno | Instalación | Alternancia automática |
| --- | --- | --- |
| Claude Code | Marketplace o plugin local | Cuando la sesión admite subagentes y selección de modelo. |
| Claude/Cowork | Importación de plugin o skill, si la cuenta la ofrece | Según herramientas y permisos expuestos; no se presupone equivalencia con Code. |
| ChatGPT/Codex | Agent Plugins y marketplace del repositorio en clientes compatibles | Cuando la sesión expone delegación con selección de modelo. |
| Otros clientes Agent Skills | Carpeta del skill con sus referencias | Según las capacidades nativas del cliente. |
| Entorno sin delegación | Instrucciones del skill | Ejecuta la tarea en el modelo actual. |

El plugin no cambia el selector del modelo principal ni añade herramientas que
el cliente no tenga. Delegar al mismo modelo no se presenta como alternancia.
No garantiza el mínimo coste global ni un porcentaje de ahorro sin mediciones.

## Instalación en Claude Code

Desde Claude Code:

```text
/plugin marketplace add novanoticia/alternancia-modelos
/plugin install alternancia-modelos@alternancia-modelos-marketplace
```

Invoca `/alternancia-modelos:alternancia-modelos` seguido de tu tarea, o pide el
protocolo en lenguaje natural. Para probar una copia local desde este repositorio:

```sh
claude --plugin-dir ./plugins/alternancia-modelos
```

## Instalación en Codex

Con una versión de Codex que incluya `plugin marketplace` y `plugin add`:

```sh
codex plugin marketplace add novanoticia/alternancia-modelos
codex plugin add alternancia-modelos@alternancia-modelos-marketplace
```

Para instalar desde una copia local, sustituye `novanoticia/alternancia-modelos`
por la ruta del repositorio (o `.` si estás en su directorio).
Inicia una sesión nueva e invoca `$alternancia-modelos` o pide el protocolo por
su nombre. El catálogo está en `.agents/plugins/marketplace.json`.

## Instalación en ChatGPT

En clientes de escritorio que admitan marketplaces locales, abre la copia del
repositorio como proyecto, reinicia el cliente y busca **Alternancia de modelos**
en la fuente correspondiente del directorio de plugins. Instálalo e invócalo
desde una conversación nueva. Las rutas de importación y su disponibilidad
dependen de la cuenta y del cliente.

El paquete usa el [formato portable documentado por OpenAI](https://developers.openai.com/plugins/build/plugins).
Un repositorio público no equivale a una publicación en el directorio universal
de plugins. Si tu cliente solo acepta servidores MCP, este paquete no se instala
como un servidor: no incluye uno.

## Skill independiente y otros clientes

La carpeta `plugins/alternancia-modelos/skills/alternancia-modelos/` contiene un
skill autónomo. Copia **toda la carpeta**, incluidas sus referencias, al directorio
de skills que indique tu cliente. El ZIP de skill se genera con el comando de
empaquetado que aparece abajo y puede importarse donde se admitan ZIP de skills.

## Diseño

- Una única fuente del protocolo compartida por los clientes.
- Manifiesto portable más compatibilidad explícita con Claude y Codex.
- Roles resueltos durante la ejecución, sin generaciones o cuotas fijadas.
- Fallos operativos recuperables y negativas de seguridad tratados por separado.
- Registro de uso observado, sin inventar delegaciones ni modificar formatos cerrados.
- Agente especialista opcional para Claude, con modelo heredado por defecto y
  selección por invocación cuando la plataforma la permita.

Consulta [los cambios respecto al original](docs/origen.md),
[los escenarios de evaluación](evals/README.md) y
[las comprobaciones de publicación](docs/validacion.md).

## Desarrollo y empaquetado

Requiere Python 3.10 o posterior y PyYAML para validar el frontmatter; el plugin
instalado no necesita Python ni PyYAML.

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build.py
python scripts/compare_evals.py evals/examples/synthetic-pair.json
```

Se generan en `dist/` dos ZIP reproducibles: el plugin completo y el skill
independiente, con un archivo `SHA256SUMS`. El plugin no incorpora los scripts de
desarrollo, los tests ni el archivo histórico del skill original.

## Fuentes y alcance

- [Empaquetado de plugins de OpenAI](https://developers.openai.com/plugins/build/plugins).
- [Plugins de Claude Code](https://code.claude.com/docs/en/plugins-reference).
- [Subagentes de Claude Code](https://code.claude.com/docs/en/sub-agents).
- [Agent Skills](https://agentskills.io/specification).

La versión 1.2.0 es un protocolo de instrucciones, no un router de inferencia por
API. Usa la delegación del host y conserva una ejecución útil cuando no existe.

## Colaboradores

- **[novanoticia](https://github.com/novanoticia):** iniciativa, dirección del proyecto
  y aportación del skill original de Claude.
- **OpenAI Codex:** contribución asistida por IA a la adaptación multiplataforma,
  implementación, documentación, pruebas y preparación de la publicación.
