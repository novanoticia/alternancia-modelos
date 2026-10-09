# Verificación online + ejemplo fechado (parte caduca del protocolo)

Este fichero respalda los Pasos 2 y 4 del skill. Es un **procedimiento de consulta más un
ejemplo fechado**, no una regla fija: los modelos nombrados abajo **caducarán**. Enrutar
siempre por rol (primario / secundario / fallback), verificar las restricciones vivas
online y sustituir por los modelos frontera vigentes. Leerlo solo al delegar de verdad.

Idea rectora: explotar las fortalezas de *varios* modelos frontera **honrando las
salvaguardas y la política de uso permitido de cada uno** — sin hardcodear, sin esquivar.

---

## 1. Verificar restricciones online (ANTES de enrutar)

Para cada modelo candidato, buscar en la web la política viva del proveedor y extraer:

- **(a) Permitido vs. bloqueado/redirigido** — qué temas maneja y cuáles se bloquean o se
  derivan a otro modelo.
- **(b) Cuota / ventana de disponibilidad** — ¿incluido por completo, limitado a un % de
  uso, o acotado a una ventana temporal?
- **(c) Destino de redirección** — cuando salta una salvaguarda, ¿a qué modelo va la petición?

**Patrones de búsqueda** (sustituir modelo/proveedor reales):
- `"<modelo> safeguards permitted use redirect"`
- `"<modelo> quota weekly usage limit availability window"`
- `"<proveedor> usage policy responsible scaling"`

**Fuentes de partida (ecosistema Anthropic, como ejemplo):** política del proveedor y
responsible scaling (`anthropic.com/responsible-scaling-policy`, `/roadmap`, `/updates`,
`anthropic.com/policy`) y la nota de lanzamiento/redespliegue del modelo concreto.

Sin acceso web: usar el ejemplo fechado de abajo **y registrar la suposición en la sección
de límites del entregable** — nunca presentar política caducada como hecho vigente.

---

## 2. Ejemplo fechado — verificado a 2026-07-06 (VERIFICAR de nuevo antes de confiar)

- **Primario = Opus 4.8** (modelo de continuidad). Capacidad frontera plena, sin ventana
  de inclusión estrecha → ejecuta el flujo completo (análisis + implementación) por
  defecto. De ahí la política **Opus-priority**: garantiza que el flujo no se atasca por
  una cuota o una ventana que se cierra.

- **Secundario = Fable 5** (especialista, selectivo). Solo tramos genuinamente difíciles,
  ambiguos y de varios pasos, cuando esté permitido y quede cuota. Restricciones conocidas:
  - Redesplegado el **2026-07-01** con un **clasificador de ciberseguridad reforzado**;
    las peticiones bloqueadas se **redirigen a Opus 4.8** y se notifica al usuario.
  - **Temas bloqueados/redirigidos:** ciberexplotación / descubrimiento de
    vulnerabilidades, QBRN (químico/biológico) y destilación de modelos. El clasificador,
    deliberadamente amplio, puede saltar incluso en **secure-coding/debugging rutinario**
    → en trabajo de seguridad, **esperar** redirecciones y tratarlas como normales.
  - **Cuota / ventana:** incluido hasta ~50% del límite semanal de uso **hasta el
    2026-07-07**; después, disponible vía créditos de uso. **Pasada esa fecha, asumir la
    ventana de inclusión cerrada salvo verificación online.** Gobernado por la Responsible
    Scaling Policy (ASL-3 / clasificadores QBRN).

**Consecuencia:** la ventana de Fable 5 se cierra *y* sus salvaguardas redirigen justo el
trabajo sensible a seguridad — por eso el primario por defecto es Opus 4.8 (máxima
continuidad) y el secundario entra solo en tramos duros y permitidos donde aporte valor.

---

## 3. Mapeo concreto (contexto de uso Claude / Cowork)

Lanzar subagentes con el override `model` de la herramienta Agent:

- primario  → `model: "opus"`  (ejemplo: Opus 4.8)
- secundario → `model: "fable"` (ejemplo: Fable 5)

En otros entornos, sustituir por el proveedor/modelos propios. Nombrar modelos aquí es
**configuración de enrutado / ejemplo fechado** — un contexto de uso compatible, no el
motor declarado del entregable — y por tanto no viola la restricción de nombrado (Paso 7
del skill).

---

## 4. Incorporar un modelo futuro (evitar que este fichero se pudra)

Para incorporar un modelo frontera nuevo: verificar su política viva (§1) y asignarle el
rol que mejor encaje — *más capaz + más continuo* → primario; *complementario o
especializado pero limitado por cuota/salvaguardas* → secundario. Después **actualizar o
borrar el ejemplo fechado de §2**. Los nombres de arriba son ilustración, no contrato.

---

## Fuentes (consultadas 2026-07-06)

- https://www.anthropic.com/news/redeploying-fable-5
- https://www.anthropic.com/responsible-scaling-policy
- https://www.anthropic.com/responsible-scaling-policy/roadmap
