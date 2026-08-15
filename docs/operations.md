# Operação

## Verificar o serviço

No painel do Render, consulte os logs do serviço `eaglercraft-survival`. O log deve mostrar o download do Paper, a instalação dos plugins e a mensagem de que o servidor terminou de iniciar. A porta interna deve ser a mesma informada pelo Render em `PORT`; ela é aplicada pelo `scripts/render-start.sh`.

## Diagnóstico de conexão

Se o cliente não conectar, confira se o serviço é do tipo **Web Service**, se está saudável e se o endereço usado é o hostname HTTPS do Render. O EaglerXServer Bukkit usa o listener do Paper, portanto não há uma segunda porta pública para configurar. Em uma instância recém-suspensa, aguarde o serviço voltar ao estado disponível antes de testar novamente.

Se a conexão abrir e cair durante uma atualização, isso é esperado para um serviço que reiniciou. O cliente deve reconectar. Se o erro persistir, reduza `VIEW_DISTANCE`, confira o uso de memória e valide se os dois JARs ainda correspondem às versões indicadas em `docs/plugin-checksums.txt`.

## Backup

O backup deve incluir todo o diretório `/data`, principalmente `world/`, `world_nether/`, `world_the_end/`, `plugins/LoginSecurity/` e `plugins/EaglercraftXServer/`. Faça a cópia antes de atualizar Paper ou qualquer plugin. O disco persistente não substitui uma cópia externa e não torna o servidor imune a exclusão acidental.

## Atualizações

Atualize uma versão por vez. Primeiro faça backup, depois altere a versão ou URL no `render.yaml`, confira a compatibilidade nas releases upstream e sincronize o Blueprint. Após o deploy, teste cadastro, login, alteração de senha e carregamento do mundo antes de permitir novos jogadores.

## Comandos de administração

A partir do console do Render, use os comandos Bukkit documentados para gerenciamento. Para ações de conta, prefira os comandos administrativos do LoginSecurity e não edite diretamente arquivos de senha. Nunca compartilhe logs que contenham IPs, nomes de jogadores ou dados de diagnóstico fora do necessário.
