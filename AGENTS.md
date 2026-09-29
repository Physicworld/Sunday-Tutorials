# Sunday-Tutorials — Guía para agentes

## Flujo por tickets (YouTrack)

- Proyecto YouTrack: **STQ** (https://youtrack.sundaythequant.com). El ticket es la única memoria entre sesiones.
- Para trabajar un ticket, carga la skill `ticket-worker` (`skill://ticket-worker`) y usa el MCP `youtrack`.
- Buscar trabajo: `project: STQ State: Open sort by: priority`.
- Traspaso con comentario en el ticket y `State: Done` (o `Review` si el PR sigue abierto).

## Git

- Nunca trabajar en el checkout principal: un worktree por ticket (`git worktree add ../Sunday-Tutorials-<ID> -b <ID>-slug origin/main`).
- Commits `tipo(<ID>): mensaje`; push de la rama y PR contra `main` (no se empuja directo a `main`).
- Merge por PR con `gh pr merge --squash --delete-branch` solo si el CI está verde (el auto-merge no está disponible en GitHub Free). No hay etiqueta `deploy-ok`: el repo no despliega nada.
- No reescribir historial ni hacer `push --force`.
- El repo es **público**: nunca commitear secretos, datos personales, rutas privadas, venvs, builds, cachés, configuración de IDE ni videos (ver `.gitignore`).
