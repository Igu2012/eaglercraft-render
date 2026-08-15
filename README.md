# Eaglercraft Survival on Render

This project provides a base for hosting an **Eaglercraft survival server** on a Render web service, using Paper 1.12.2, EaglerXServer, and LoginSecurity. The repository is organized to connect directly to Render as a **Blueprint** through the `render.yaml` file at the repository root.

> **Important:** Nickname authentication is provided by the LoginSecurity plugin through in-game chat commands. On the first visit, a player uses `/register <password>`; on later visits, the player uses `/login <password>`. The system does not use a Mojang password and does not store passwords in plain text.

## How the project works

Render runs the Docker container based on `itzg/minecraft-server:java17`. The container downloads Paper 1.12.2 and automatically installs the pinned EaglerXServer, LoginSecurity, ViaVersion, ViaBackwards, and ViaRewind releases. Paper acts as the survival server, while EaglerXServer injects Eaglercraft WebSocket support into the same Bukkit/Paper server listener.

Render terminates TLS at the public endpoint and forwards the WebSocket connection to the container. The `scripts/render-start.sh` script reads Render's automatic `PORT` variable and exports it as `SERVER_PORT` before starting the container entrypoint. This keeps the Paper and EaglerXServer ports aligned with the port selected by Render without using unsupported interpolation in `render.yaml`.

LoginSecurity accounts, configuration files, the world, inventories, and other server data are stored under `/data`. Both included Blueprints use the free Render plan and intentionally do not declare a persistent disk. The filesystem is ephemeral, so accounts, worlds, and generated files can be lost after suspension, restart, or redeploy.

## Repository structure

| Path | Purpose |
| --- | --- |
| `render.yaml` | Primary free Blueprint that creates the Docker web service without a persistent disk. |
| `render-free.yaml` | Additional free testing Blueprint with a distinct service name. |
| `Dockerfile` | Uses the itzg container and installs the project's startup script. |
| `scripts/render-start.sh` | Converts Render's `PORT` into Minecraft's `SERVER_PORT`. |
| `config/server.properties` | Initial survival-world settings. |
| `config/plugins/EaglercraftXServer/` | TOML configuration for the Eaglercraft listener and server. |
| `config/plugins/LoginSecurity/` | Directory reserved for persistent LoginSecurity configuration. |
| `docs/` | Operations, diagnostics, and plugin hash notes. |
| `docs/plugin-checksums.txt` | URLs and SHA-256 hashes for the pinned JAR files. |

## Deploying with the Render Blueprint

First, create a GitHub repository and push all project files to the `main` branch. In the Render dashboard, choose **New → Blueprint**, connect the repository, and select either `render.yaml` or `render-free.yaml` as the Blueprint Path. Both files use the `free` plan and do not declare a persistent disk; their service names are different so they can be tested separately.

The free plan is intended for temporary testing. It may suspend the service after 15 minutes without inbound traffic, causing the next connection to take approximately one minute while the process starts again. The world, accounts, plugins, and generated configuration can be lost after suspension, restart, or redeploy. If you later need persistence, change the service to a paid plan and add a persistent disk mounted at `/data`.

After the first deployment, copy the HTTPS address shown by Render. In a compatible EaglercraftX client, add the server using the service address, normally `wss://YOUR-SERVICE-NAME.onrender.com`, without adding a public port. Render web services accept inbound WebSocket connections; if a particular client asks for an HTTP address, use the same hostname with `https://` for queries and the WebSocket address format required by that client version.

## Free testing mode

For a second temporary free test, create the Blueprint using `render-free.yaml`. In the Render Blueprint setup screen, set **Blueprint Path** to `render-free.yaml`, keep the branch as `main`, and deploy the Blueprint. This file also uses the `free` plan and deliberately does not declare a disk. You can use `render.yaml` for the primary free service or `render-free.yaml` for the separate test service.

The free Blueprints use a reduced Java profile with a 224 MB maximum heap, a 112 MB Metaspace cap, SerialGC, one active processor, and capped native-memory areas so the process has room under Render's 512 MB instance limit. They are suitable for checking whether the container starts and whether a small number of players can connect, register, and log in. They are not suitable for a persistent public survival server. Render may suspend a free web service after 15 minutes without inbound traffic, and local filesystem changes can be lost after suspension, restart, or redeploy. That means the world, accounts, plugins, and generated configuration may disappear.

## Player authentication flow

On the first visit, the nickname selected by the player does not yet exist on the server. LoginSecurity blocks access to the world and tells the player in chat to run `/register <password>`. After registration, the player can enter the survival world. On a later visit with the same nickname, the plugin blocks access until the player runs `/login <password>`.

The password should be different from the player's personal passwords and must not be shared. To change a password, use `/changepassword <current-password> <new-password>`. To end the current session, use `/logout`. Administrators can consult the LoginSecurity documentation for administrative commands and account recovery.

| Situation | Command |
| --- | --- |
| First-time registration | `/register <password>` |
| Sign in to an existing account | `/login <password>` |
| Change a password | `/changepassword <current-password> <new-password>` |
| End the current session | `/logout` |
| Remove your own account | `/unregister <current-password>` |

## Survival configuration

The initial values use survival mode, normal difficulty, enabled PVP, a maximum of 20 players, a reduced view distance of six chunks, and disabled spawn protection. These choices reduce resource and bandwidth usage for a small server. They can be changed through the corresponding variables in `render.yaml` or through the persistent `server.properties` file after the first boot.

EaglerXServer is configured with WebSocket compression, a dual-stack listener, and original-IP forwarding through the `X-Forwarded-For` header. TLS is not enabled inside the plugin because public TLS is terminated by Render before the connection reaches the container. EaglerXServer voice service remains disabled by default.

## Local Docker test

To test the project before deployment, install Docker and run the following command from the repository root:

```bash
docker build -t eaglercraft-survival .
docker run --rm -it \
  -p 25565:25565 \
  -e EULA=TRUE \
  -e TYPE=PAPER \
  -e VERSION=1.12.2 \
  -e PAPER_BUILD=1620 \
  -e MEMORY=224M \
  -e INIT_MEMORY=96M \
  -e MAX_MEMORY=224M \
  -e USE_AIKAR_FLAGS=false \
  -e SERVER_PORT=25565 \
  -e PORT=25565 \
  -v "$PWD/local-data:/data" \
  eaglercraft-survival
```

When the console reports that the server has finished starting, connect a local Java client to `localhost:25565` or use an Eaglercraft client that supports WebSocket connections at `ws://localhost:25565`. The first run may take longer because the container downloads Paper and the plugins. Do not place passwords, worlds, or private logs in GitHub.

## Security and maintenance

Plugin URLs are pinned to specific releases to reduce unexpected changes during deployment. The ViaVersion, ViaBackwards, and ViaRewind plugins provide the protocol translation recommended for EaglercraftX 1.8 clients connecting to the Paper 1.12.2 server. When updating a version, change the URL in the selected Blueprint, read the upstream release notes, and back up the server data before synchronizing the Blueprint. The server uses `online-mode=false` because Eaglercraft clients do not perform Mojang premium authentication; therefore, LoginSecurity is essential to prevent another person from using the same nickname.

These free Blueprints do not include a persistent disk. If you later add one to a paid service, remember that a persistent disk improves availability but is not a complete backup. Make regular copies of `/data`, especially before updates, version changes, or additional plugin installations. Never publish tokens, passwords, database files, private `server.properties` data, or credentials for external services.

## Known limitations

This project is a simple base for a small survival server. The free variant deliberately uses a low-memory Java profile with additional Metaspace headroom and should be limited to a small number of players. Render may restart instances, interrupt WebSocket connections during maintenance or deployments, and apply CPU, memory, and traffic limits according to the selected plan. Clients must reconnect after an interruption. The free variant is intended only for temporary testing and is not suitable for the persistence or scale required by a continuously running survival server.

LoginSecurity provides chat-based registration and login, not a graphical password screen in the Eaglercraft menu. If you need a custom graphical interface or external-database integration, you will need to develop a separate Bukkit plugin and review the authentication flow.

## References

[1]: https://render.com/docs/blueprint-spec "Render — Blueprint YAML Reference"
[2]: https://render.com/docs/websocket "Render — WebSockets on Render"
[3]: https://render.com/docs/free "Render — Deploy for Free"
[4]: https://render.com/docs/disks "Render — Persistent Disks"
[5]: https://github.com/lax1dude/eaglerxserver "lax1dude/eaglerxserver — EaglercraftXServer"
[6]: https://github.com/lenis0012/LoginSecurity "lenis0012/LoginSecurity — LoginSecurity"
[7]: https://docker-minecraft-server.readthedocs.io/en/latest/types-and-platforms/server-types/paper/ "itzg — Paper server type"
[8]: https://docker-minecraft-server.readthedocs.io/en/latest/mods-and-plugins/ "itzg — Working with mods and plugins"

Integration material prepared by **Manus AI**.
