# OpenClaw: cómo crear un agente — tutorial extensivo paso a paso

> Basado en la documentación oficial de OpenClaw.
> Fecha de preparación: 2026-03-26.

---

## Índice

1. [Qué es un agente en OpenClaw](#qué-es-un-agente-en-openclaw)
2. [Cómo está organizado OpenClaw](#cómo-está-organizado-openclaw)
3. [Requisitos previos](#requisitos-previos)
4. [Ruta recomendada de instalación y onboarding](#ruta-recomendada-de-instalación-y-onboarding)
5. [Crear tu primer agente](#crear-tu-primer-agente)
6. [Entender el workspace del agente](#entender-el-workspace-del-agente)
7. [Definir identidad y personalidad](#definir-identidad-y-personalidad)
8. [Conectar el agente a un canal](#conectar-el-agente-a-un-canal)
9. [Añadir bindings para enrutar mensajes](#añadir-bindings-para-enrutar-mensajes)
10. [Configurar `openclaw.json`](#configurar-openclawjson)
11. [Levantar y verificar el gateway](#levantar-y-verificar-el-gateway)
12. [Ejemplo completo de cero a funcionando](#ejemplo-completo-de-cero-a-funcionando)
13. [Ejemplo con varios agentes](#ejemplo-con-varios-agentes)
14. [Buenas prácticas](#buenas-prácticas)
15. [Errores comunes y troubleshooting](#errores-comunes-y-troubleshooting)
16. [Comandos de referencia rápida](#comandos-de-referencia-rápida)
17. [Fuentes oficiales](#fuentes-oficiales)

---

## Qué es un agente en OpenClaw

En OpenClaw, un **agente** es una unidad aislada con su propio:

- workspace
- identidad
- instrucciones
- sesiones
- estado de autenticación
- enrutado de mensajes

La documentación oficial describe `openclaw agents` como el sistema para gestionar agentes aislados con **workspace + auth + routing**. En la práctica, eso significa que cada agente puede comportarse como una “persona” distinta dentro del mismo Gateway.

### Qué implica esa separación

Si creas dos agentes, por ejemplo `coding` y `social`, puedes darles:

- tonos distintos
- reglas distintas
- cuentas de canal distintas
- sesiones distintas
- workspaces distintos

OpenClaw documenta además que cada agente obtiene su propio `agentDir` y su propio almacén de sesiones bajo:

```text
~/.openclaw/agents/<agentId>/sessions/
```

Eso evita mezclar conversaciones, credenciales y contexto entre agentes.

---

## Cómo está organizado OpenClaw

Antes de crear un agente, conviene entender la arquitectura general.

### Componentes principales

#### 1. Gateway
El **Gateway** es el proceso central. La documentación oficial lo presenta como la fuente de verdad para:

- sesiones
- routing
- conexiones de canales

#### 2. Workspace
El **workspace** es el directorio de trabajo principal del agente. OpenClaw lo usa como su `cwd` para herramientas y contexto.

#### 3. Canales
Los **canales** son las superficies de entrada y salida: WhatsApp, Telegram, Discord, iMessage y otros.

#### 4. Bindings
Los **bindings** conectan tráfico entrante de un canal o cuenta con un agente concreto.

---

## Requisitos previos

La documentación oficial recomienda empezar por el flujo de onboarding y señala que la personalización debe vivir fuera del repositorio principal, típicamente en:

- `~/.openclaw/openclaw.json`
- `~/.openclaw/workspace`

### Lo que debes tener preparado

- un sistema compatible: macOS, Linux o Windows/WSL2
- OpenClaw instalado
- acceso a terminal
- una API key o proveedor/modelo configurado durante el onboarding
- si vas a usar canales, las credenciales necesarias de cada canal

### Qué ruta conviene usar

OpenClaw tiene dos caminos de onboarding:

- **CLI onboarding**: recomendado para la mayoría de usuarios, servidores y setups con más control
- **macOS app onboarding**: interfaz guiada solo para macOS

La documentación dice explícitamente que **la mayoría de usuarios deberían empezar con el onboarding por CLI**.

---

## Ruta recomendada de instalación y onboarding

### Opción A: onboarding por CLI

Es la ruta más portable y la más cercana a cómo se documenta la automatización.

#### Instalar OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

En Windows:

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

#### Ejecutar onboarding

```bash
openclaw onboard
```

En muchos casos se usa también:

```bash
openclaw onboard --install-daemon
```

Este flujo configura auth, Gateway y canales opcionales.

### Opción B: usar `openclaw setup`

Si tu build o tu flujo no expone onboarding completo, la documentación oficial indica esta alternativa:

```bash
openclaw setup
openclaw channels login
openclaw gateway
```

### Dónde queda la personalización

OpenClaw recomienda conservar tu tailoring fuera del repo:

```text
~/.openclaw/openclaw.json
~/.openclaw/workspace
```

Eso facilita actualizar OpenClaw sin romper tu configuración.

---

## Crear tu primer agente

La forma más directa de crear un agente es:

```bash
openclaw agents add work
```

Ese comando crea un agente aislado. Si no indicas `--workspace`, OpenClaw puede lanzar el asistente/wizard según el flujo activo.

### Crear un agente con workspace explícito

```bash
openclaw agents add work --workspace ~/.openclaw/workspace-work
```

Esta forma es mejor cuando quieres:

- controlar la ubicación del workspace
- versionar el workspace con git
- separar claramente varios agentes

### Qué escribe OpenClaw al crear el agente

La documentación del wizard CLI indica que `openclaw agents add` escribe:

- `agents.list[]`
- opcionalmente `bindings`

Además, OpenClaw guarda las sesiones bajo:

```text
~/.openclaw/agents/<agentId>/sessions/
```

### Modelo, bind y modo no interactivo

La documentación de automatización CLI muestra que también puedes crear un agente con opciones como estas:

```bash
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.2 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

Esto es útil para scripts, despliegues repetibles o automatización.

---

## Entender el workspace del agente

El workspace no es una carpeta “decorativa”; es el corazón del agente.

La documentación oficial del runtime y del workspace explica que OpenClaw usa un único workspace como directorio de trabajo para herramientas y contexto.

### Archivos importantes del workspace

OpenClaw documenta estos archivos en la raíz del workspace:

#### `AGENTS.md`
Sirve para instrucciones operativas del agente y su uso de memoria.

Buen contenido para este archivo:

- prioridades
- reglas de trabajo
- límites operativos
- estilo de ejecución

#### `SOUL.md`
Define:

- persona
- tono
- límites

#### `USER.md`
Sirve para describir al usuario:

- cómo dirigirse a él
- idioma preferido
- contexto relevante

#### `IDENTITY.md`
Define:

- nombre
- vibe o tema
- emoji
- identidad general del agente

#### `TOOLS.md`
Sirve para notas sobre herramientas.

### Ejemplo realista de workspace

```text
~/.openclaw/workspace-work/
├── AGENTS.md
├── SOUL.md
├── USER.md
├── IDENTITY.md
├── TOOLS.md
├── HEARTBEAT.md
└── memory/
```

### Ejemplo de contenido

#### `AGENTS.md`

```md
# Reglas operativas

- Ayuda principalmente con ingeniería, documentación y automatización.
- Nunca ejecutes acciones destructivas sin confirmación explícita.
- Resume los cambios antes de aplicarlos.
- Prioriza respuestas en español.
```

#### `SOUL.md`

```md
# Personalidad

Eres un asistente técnico claro, preciso y calmado.
Evitas relleno y priorizas pasos accionables.
```

#### `USER.md`

```md
# Usuario

El usuario prefiere tutoriales detallados, ejemplos prácticos y comandos completos.
```

#### `IDENTITY.md`

```md
# Identity

name: WorkBot
emoji: "🤖"
theme: "technical operator"
```

### Versionar el workspace con git

La documentación oficial recomienda inicializar el workspace como repositorio si es nuevo:

```bash
cd ~/.openclaw/workspace-work
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"
```

Esto es una muy buena práctica porque te permite:

- deshacer cambios
- comparar versiones
- mover tu agente entre máquinas

---

## Definir identidad y personalidad

Una cosa es el contenido del workspace y otra es la identidad registrada en la configuración del agente.

### Cargar identidad desde `IDENTITY.md`

```bash
openclaw agents set-identity --workspace ~/.openclaw/workspace-work --from-identity
```

Según la documentación, `set-identity --from-identity` lee el archivo `IDENTITY.md` desde la raíz del workspace.

### Sobrescribir identidad por CLI

```bash
openclaw agents set-identity --agent work --name "WorkBot" --emoji "🤖"
```

### Qué campos escribe `set-identity`

OpenClaw documenta estos campos dentro de `agents.list[].identity`:

- `name`
- `theme`
- `emoji`
- `avatar`

### Ejemplo de configuración resultante

```json5
{
  agents: {
    list: [
      {
        id: "work",
        identity: {
          name: "WorkBot",
          theme: "technical operator",
          emoji: "🤖",
          avatar: "avatars/workbot.png"
        }
      }
    ]
  }
}
```

---

## Conectar el agente a un canal

Crear el agente no basta. Si quieres que reciba mensajes desde un canal, primero necesitas **una cuenta de canal**.

### Ejemplo con WhatsApp

```bash
openclaw channels login --channel whatsapp --account work
```

### Qué significa `--account`

Ese `accountId` sirve para identificar la cuenta del canal asociada al agente.

### Ejemplos típicos por canal

La documentación de multi-agent resume este patrón:

- **Discord**: un bot por agente
- **Telegram**: un bot por agente vía BotFather
- **WhatsApp**: un número enlazado por cuenta

### Alternativa simplificada

En algunos flujos de setup, OpenClaw usa simplemente:

```bash
openclaw channels login
```

Y luego el wizard te guía.

---

## Añadir bindings para enrutar mensajes

Esta parte es la más importante después de crear el agente.

Sin bindings, puedes tener el agente creado pero sin tráfico entrante.

### Añadir un binding explícito

```bash
openclaw agents bind --agent work --bind whatsapp:work
```

Otros ejemplos oficiales:

```bash
openclaw agents bind --agent work --bind telegram:ops
openclaw agents bind --agent work --bind discord:guild-a
```

### Ver bindings

```bash
openclaw agents bindings
openclaw agents bindings --agent work
openclaw agents list --bindings
```

### Qué pasa si omites `accountId`

También puedes enlazar solo por canal:

```bash
openclaw agents bind --agent work --bind telegram
```

La documentación indica que, si omites `accountId`, OpenClaw lo resuelve desde defaults del canal y hooks del plugin cuando están disponibles.

### Comportamiento del alcance del binding

OpenClaw documenta estas reglas:

- un binding sin `accountId` coincide con la cuenta por defecto del canal
- `accountId: "*"` funciona como fallback a nivel de canal
- si ya existía un binding por canal y luego añades uno con cuenta explícita, OpenClaw puede actualizarlo en lugar de duplicarlo

### Eliminar bindings

```bash
openclaw agents unbind --agent work --bind telegram:ops
openclaw agents unbind --agent work --all
```

---

## Configurar `openclaw.json`

OpenClaw lee la configuración central desde:

```text
~/.openclaw/openclaw.json
```

La documentación oficial recomienda empezar con `openclaw onboard` o `openclaw configure` si no quieres editar el archivo a mano.

### Configuración mínima documentada

```json5
// ~/.openclaw/openclaw.json
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } }
}
```

### Ojo con una pequeña inconsistencia documental

En la página de ejemplos aparece también un ejemplo mínimo con clave `agent` singular:

```json5
{
  agent: { workspace: "~/.openclaw/workspace" },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } }
}
```

Pero en la referencia principal de configuración y en la documentación de multi-agent la forma dominante y más consistente es `agents`. Para un tutorial actual orientado a agentes, es más seguro seguir el esquema con `agents`.

### Editar la configuración desde CLI

```bash
openclaw configure
openclaw config get agents.defaults.workspace
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config unset plugins.entries.brave.config.webSearch.apiKey
```

### Control de acceso por canal

La documentación explica que el acceso por DM se controla con `dmPolicy`.

Valores documentados:

- `pairing` — por defecto; remitentes desconocidos deben emparejarse
- `allowlist` — solo usuarios permitidos en `allowFrom`
- `open` — permite todo; requiere `allowFrom: ["*"]`
- `disabled` — ignora todos los DMs

### Ejemplo más completo para Telegram

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      allowFrom: ["tg:123"]
    }
  }
}
```

---

## Levantar y verificar el gateway

Con el agente creado, el canal autenticado y los bindings puestos, ya puedes levantar el Gateway.

### Arrancar manualmente

```bash
openclaw gateway --port 18789
```

### Reiniciar si ya estaba en marcha

```bash
openclaw gateway restart
```

### Verificaciones útiles

```bash
openclaw health
openclaw agents list --bindings
openclaw channels status --probe
```

### Qué deberías comprobar

- que el agente aparece en la lista
- que el binding está asociado al canal/cuenta correctos
- que el canal figura como conectado
- que el Gateway está sano

---

## Ejemplo completo de cero a funcionando

Este ejemplo crea un agente `work` con WhatsApp.

```bash
# 1) Instalar OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 2) Onboarding inicial
openclaw onboard --install-daemon

# 3) Crear un agente con workspace dedicado
openclaw agents add work --workspace ~/.openclaw/workspace-work

# 4) Crear/editar archivos del workspace
mkdir -p ~/.openclaw/workspace-work
nano ~/.openclaw/workspace-work/AGENTS.md
nano ~/.openclaw/workspace-work/SOUL.md
nano ~/.openclaw/workspace-work/USER.md
nano ~/.openclaw/workspace-work/IDENTITY.md

# 5) Cargar identidad desde IDENTITY.md
openclaw agents set-identity --workspace ~/.openclaw/workspace-work --from-identity

# 6) Login en el canal
openclaw channels login --channel whatsapp --account work

# 7) Enrutar el canal hacia el agente
openclaw agents bind --agent work --bind whatsapp:work

# 8) Arrancar el gateway
openclaw gateway --port 18789

# 9) Verificar estado
openclaw agents list --bindings
openclaw channels status --probe
openclaw health
```

---

## Ejemplo con varios agentes

Supón que quieres separar trabajo técnico y presencia social.

### Crear agentes

```bash
openclaw agents add coding --workspace ~/.openclaw/workspace-coding
openclaw agents add social --workspace ~/.openclaw/workspace-social
```

### Autenticar canales/cuentas separadas

```bash
openclaw channels login --channel telegram --account coding
openclaw channels login --channel discord --account social
```

### Hacer bindings

```bash
openclaw agents bind --agent coding --bind telegram:coding
openclaw agents bind --agent social --bind discord:social
```

### Resultado

- `coding` responde como agente técnico
- `social` responde como agente de comunicación
- cada uno tiene su propio workspace, sesiones y estilo

Este es precisamente el patrón que la documentación de multi-agent promueve: varias “personas” o roles aislados dentro de un único Gateway.

---

## Buenas prácticas

### 1. Un workspace por agente

No mezcles archivos de personalidad, memoria o herramientas entre agentes que tengan objetivos distintos.

### 2. Una cuenta por agente cuando el canal lo permita

Especialmente en Telegram, Discord o WhatsApp, esto simplifica mucho el routing mental y operativo.

### 3. Versiona el workspace con git

Te ahorra sustos cuando cambias instrucciones, memoria o identidad.

### 4. Usa `allowFrom` o políticas de DM restrictivas

No dejes el bot abierto sin control si va a tener herramientas o acceso sensible.

### 5. Mantén la personalización fuera del repo principal

OpenClaw lo recomienda explícitamente para que actualizar no rompa tu setup.

### 6. Comprueba bindings después de cada cambio

Un agente “no responde” muchas veces no significa que esté roto; significa que no quedó bien enlazado.

---

## Errores comunes y troubleshooting

### Error 1: “He creado el agente pero no responde”

Causa habitual:

- no has hecho `bind`
- el canal no está autenticado
- el Gateway no está corriendo

Qué revisar:

```bash
openclaw agents list --bindings
openclaw channels status --probe
openclaw health
```

### Error 2: “Los mensajes llegan al agente equivocado”

Suele pasar cuando:

- has usado bindings demasiado genéricos
- no has fijado `accountId`
- existe un binding fallback que captura más tráfico del que querías

Solución:

- inspecciona `openclaw agents bindings`
- usa bindings explícitos como `telegram:ops`
- elimina bindings sobrantes

### Error 3: “He mezclado sesiones o identidad entre agentes”

La documentación deja claro que cada agente debe tener su propio `agentDir` y almacén de sesiones. Evita reutilizar rutas de estado o workspaces sin querer.

### Error 4: “Quiero usarlo para varios usuarios no confiables”

La documentación de seguridad es clara: OpenClaw **no** se presenta como frontera de seguridad hostil multi-tenant. Si necesitas separar usuarios adversariales o con distinta confianza, la recomendación es separar:

- Gateway
- credenciales
- idealmente usuario del SO o host

### Error 5: “No sé si editar JSON o usar CLI”

Ruta recomendada:

- para empezar: `openclaw onboard` o `openclaw configure`
- para cambios concretos: `openclaw config get/set/unset`
- para escenarios avanzados: edición directa de `~/.openclaw/openclaw.json`

---

## Comandos de referencia rápida

### Crear agente

```bash
openclaw agents add work
openclaw agents add work --workspace ~/.openclaw/workspace-work
```

### Ver agentes y bindings

```bash
openclaw agents list
openclaw agents list --bindings
openclaw agents bindings
openclaw agents bindings --agent work
```

### Vincular y desvincular

```bash
openclaw agents bind --agent work --bind telegram:ops
openclaw agents unbind --agent work --bind telegram:ops
openclaw agents unbind --agent work --all
```

### Identidad

```bash
openclaw agents set-identity --workspace ~/.openclaw/workspace-work --from-identity
openclaw agents set-identity --agent work --name "WorkBot" --emoji "🤖"
```

### Canales

```bash
openclaw channels login
openclaw channels login --channel whatsapp --account work
openclaw channels status --probe
```

### Configuración

```bash
openclaw configure
openclaw config get agents.defaults.workspace
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config unset plugins.entries.brave.config.webSearch.apiKey
```

### Gateway y salud

```bash
openclaw gateway --port 18789
openclaw gateway restart
openclaw health
```

---

## Fuentes oficiales

Documentación oficial consultada para este tutorial:

- Onboarding Overview: https://docs.openclaw.ai/start/onboarding-overview
- Setup: https://docs.openclaw.ai/start/setup
- CLI `agents`: https://docs.openclaw.ai/cli/agents
- Multi-Agent Routing: https://docs.openclaw.ai/concepts/multi-agent
- Agent Workspace: https://docs.openclaw.ai/concepts/agent-workspace
- Configuration: https://docs.openclaw.ai/gateway/configuration
- Configuration Examples: https://docs.openclaw.ai/gateway/configuration-examples
- Security: https://docs.openclaw.ai/gateway/security
- CLI Setup Reference: https://docs.openclaw.ai/start/wizard-cli-reference

---

## Cierre

La secuencia mental correcta en OpenClaw es esta:

1. instalar
2. hacer onboarding o setup
3. crear el agente
4. definir su workspace
5. fijar identidad
6. autenticar canal
7. hacer binding
8. arrancar Gateway
9. verificar estado y routing

Si entiendes esa cadena, ya entiendes cómo “nace” un agente en OpenClaw.
