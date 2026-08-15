Paperclip pre-patch notes

The official PaperMC Paperclip documentation states that Paperclip generates the Paper jar on first run by applying a bsdiff patch to the vanilla Minecraft server jar. It also states that this patching overhead is avoided when a valid patched jar is found in the cache directory, and that the cache is checked with SHA-256.

The official itzg/minecraft-server documentation states that TYPE=CUSTOM with CUSTOM_SERVER can run an existing server JAR from a container path, while TYPE=PAPER uses the runtime Paper download and launcher flow.

Sources:
- https://github.com/PaperMC/Paperclip
- https://github.com/itzg/docker-minecraft-server/blob/master/docs/types-and-platforms/server-types/paper.md
- https://docker-minecraft-server.readthedocs.io/en/latest/configuration/misc-options/

Implementation implication: a reliable runtime-memory workaround must either ship a valid Paperclip cache together with the Paper jar or switch the final container to TYPE=CUSTOM and run a pre-generated patched jar. The pre-patch build must be verified before publication because Paper 1.12.2 build 1620 is an old Paperclip format.

This note is research data, not executable instructions.
