from pathlib import Path
import tomllib

import yaml

ROOT = Path(__file__).resolve().parents[1]

with (ROOT / "render.yaml").open(encoding="utf-8") as handle:
    blueprint = yaml.safe_load(handle)
with (ROOT / "render-free.yaml").open(encoding="utf-8") as handle:
    free_blueprint = yaml.safe_load(handle)
with (ROOT / "render-paid.yaml").open(encoding="utf-8") as handle:
    paid_blueprint = yaml.safe_load(handle)

assert isinstance(blueprint, dict), "render.yaml precisa ser um objeto YAML"
services = blueprint.get("services")
assert isinstance(services, list) and services, "services precisa conter pelo menos um serviço"
service = services[0]
assert service.get("type") == "web", "o serviço principal deve ser web"
assert service.get("runtime") == "docker", "o serviço principal deve usar Docker"
assert service.get("plan") == "free", "render.yaml deve usar o plano free"
assert "disk" not in service, "render.yaml não deve declarar disco persistente"
assert service.get("numInstances") == 1, "o servidor survival deve usar uma instância"

env = {
    item["key"]: item.get("value", "")
    for item in service.get("envVars", [])
    if "key" in item
}
assert env.get("EULA") == "TRUE"
assert env.get("TYPE") == "PAPER"
assert env.get("VERSION") == "1.12.2"
plugins = env.get("PLUGINS", "")
assert "EaglerXServer.jar" in plugins
assert "LoginSecurity-Spigot-3.3.1.jar" in plugins
assert "ViaVersion-5.11.0.jar" not in plugins
assert "ViaBackwards-5.11.0.jar" not in plugins
assert "ViaRewind-4.1.3.jar" not in plugins
assert env.get("MEMORY") == "256M"
assert env.get("INIT_MEMORY") == "128M"
assert env.get("MAX_MEMORY") == "256M"
assert "MaxMetaspaceSize=96M" in env.get("JVM_OPTS", "")
assert "MaxDirectMemorySize=48M" in env.get("JVM_OPTS", "")
assert env.get("MALLOC_ARENA_MAX") == "1"
assert env.get("USE_AIKAR_FLAGS") == "false"
assert env.get("CLEAN_SERVER_LIBRARIES") == "false"
assert env.get("MAX_PLAYERS") == "8"
assert env.get("VIEW_DISTANCE") == "4"

free_services = free_blueprint.get("services")
assert isinstance(free_services, list) and free_services, "render-free.yaml precisa conter um serviço"
assert free_services[0].get("name") == "eaglercraft-survival-free", "render-free.yaml deve usar o nome eaglercraft-survival-free"
free_service = free_services[0]
assert free_service.get("type") == "web"
assert free_service.get("runtime") == "docker"
assert free_service.get("plan") == "free"
assert "disk" not in free_service, "a variante free não pode declarar disco persistente"
free_env = {
    item["key"]: item.get("value", "")
    for item in free_service.get("envVars", [])
    if "key" in item
}
assert free_env.get("MOTD") == "Eaglercraft Survival - Free Test"
assert free_env.get("MEMORY") == "256M"
assert free_env.get("INIT_MEMORY") == "128M"
assert free_env.get("MAX_MEMORY") == "256M"
assert free_env.get("MAX_PLAYERS") == "8"
assert free_env.get("VIEW_DISTANCE") == "4"
assert "MaxMetaspaceSize=96M" in free_env.get("JVM_OPTS", "")
assert "MaxDirectMemorySize=48M" in free_env.get("JVM_OPTS", "")
assert free_env.get("MALLOC_ARENA_MAX") == "1"
assert free_env.get("USE_AIKAR_FLAGS") == "false"
assert free_env.get("CLEAN_SERVER_LIBRARIES") == "false"
free_plugins = free_env.get("PLUGINS", "")
assert "EaglerXServer.jar" in free_plugins
assert "LoginSecurity-Spigot-3.3.1.jar" in free_plugins
assert "ViaVersion-5.11.0.jar" not in free_plugins
assert "ViaBackwards-5.11.0.jar" not in free_plugins
assert "ViaRewind-4.1.3.jar" not in free_plugins

paid_services = paid_blueprint.get("services")
assert isinstance(paid_services, list) and paid_services, "render-paid.yaml precisa conter um serviço"
paid_service = paid_services[0]
assert paid_service.get("type") == "web"
assert paid_service.get("runtime") == "docker"
assert paid_service.get("plan") == "standard"
assert paid_service.get("disk", {}).get("mountPath") == "/data"
assert paid_service.get("disk", {}).get("sizeGB") == 10
paid_env = {
    item["key"]: item.get("value", "")
    for item in paid_service.get("envVars", [])
    if "key" in item
}
paid_plugins = paid_env.get("PLUGINS", "")
assert "EaglerXServer.jar" in paid_plugins
assert "LoginSecurity-Spigot-3.3.1.jar" in paid_plugins
assert "ViaVersion-5.11.0.jar" in paid_plugins
assert "ViaBackwards-5.11.0.jar" in paid_plugins
assert "ViaRewind-4.1.3.jar" in paid_plugins
assert paid_env.get("MEMORY") == "1G"
assert paid_env.get("MAX_MEMORY") == "1G"

with (ROOT / "config/plugins/EaglercraftXServer/settings.toml").open("rb") as handle:
    settings = tomllib.load(handle)
with (ROOT / "config/plugins/EaglercraftXServer/listener.toml").open("rb") as handle:
    listener = tomllib.load(handle)
with (ROOT / "config/bukkit.yml").open(encoding="utf-8") as handle:
    bukkit = yaml.safe_load(handle)
with (ROOT / "config/spigot.yml").open(encoding="utf-8") as handle:
    spigot = yaml.safe_load(handle)
assert settings["server_name"] == "Eaglercraft Survival"
assert settings["http_websocket_compression_level"] == 1
assert listener["dual_stack"] is True
assert listener["forward_ip_header"] == "X-Forwarded-For"
assert bukkit["spawn-limits"] == {"monsters": 35, "animals": 8, "water-animals": 3, "ambient": 1}
assert bukkit["ticks-per"]["monster-spawns"] == 20
assert bukkit["ticks-per"]["animal-spawns"] == 400
spigot_default = spigot["world-settings"]["default"]
assert spigot_default["mob-spawn-range"] == 4
assert spigot_default["entity-activation-range"] == {"animals": 16, "monsters": 24, "misc": 8, "tick-inactive-villagers": False}
assert spigot_default["ticks-per"]["hopper-transfer"] == 8
assert spigot_default["nerf-spawner-mobs"] is False

for required in (
    "Dockerfile",
    "README.md",
    "render-free.yaml",
    "scripts/render-start.sh",
    "config/server.properties",
    "config/bukkit.yml",
    "config/spigot.yml",
    "config/plugins/EaglercraftXServer/settings.toml",
    "config/plugins/EaglercraftXServer/listener.toml",
):
    path = ROOT / required
    assert path.is_file(), f"arquivo ausente: {required}"

print("Blueprint e estrutura básica válidos.")
