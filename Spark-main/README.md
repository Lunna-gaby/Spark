# ReservaEdu / Spark — Cloudflare Workers + D1

Sistema de reservas de equipamentos pedagógicos. Esta versão mantém as telas enviadas e usa um Worker JavaScript com banco persistente D1. Não é necessário instalar Python para publicar esta versão.

## Publicar pelo PowerShell

Instale Node.js LTS. Extraia o ZIP e abra o PowerShell dentro da pasta Spark-main (a pasta que contém package.json e wrangler.jsonc).

```powershell
npm install
npx wrangler login
npx wrangler d1 create spark-db
```

O último comando retorna um `database_id`. Copie esse identificador para `wrangler.jsonc`, substituindo `COLE_AQUI_O_DATABASE_ID`. Se o banco spark-db já existir, use `npx wrangler d1 list` para obter seu ID; não crie outro banco nem apague o existente.

```powershell
npm run db:remote
npx wrangler secret put ADMIN_PASSWORD
npm run deploy
```

Ao executar `secret put`, digite uma senha forte para a direção. Não coloque a senha no GitHub. O deploy retorna a URL `https://spark.<sua-conta>.workers.dev`.

Acesse a URL, crie uma reserva e abra “Reservas realizadas”. O navegador solicitará usuário `admin` e a senha configurada. Listagem de reservas, exclusão e alteração de status exigem esse acesso. A tela pública de criação não exige login. Para encerrar o acesso administrativo, feche a sessão do navegador; em computadores compartilhados use uma janela privada e feche-a ao terminar.

## Publicar com o repositório GitHub

O repositório original está em https://github.com/Lunna-gaby/Spark. Envie os arquivos deste pacote para o repositório com uma conta que tenha permissão de escrita, preservando a estrutura da pasta e incluindo package-lock.json. Não envie node_modules, .wrangler, .dev.vars ou senhas.

Antes da primeira publicação pelo painel, crie o banco, preencha seu ID e aplique a migração pelos comandos acima. Em Workers & Pages, crie/importa um Worker pelo repositório (não use upload de site estático):

- Diretório raiz: raiz do repositório, onde está package.json.
- Comando de build: deixe vazio, pois não há compilação de frontend.
- Comando de deploy: `npx wrangler deploy`.
- Binding D1: `DB`, com o banco `spark-db` (declarado no wrangler.jsonc).
- Secret do Worker: `ADMIN_PASSWORD`.

O Worker precisa do banco e da senha antes de ser usado. Nas alterações futuras de schema, aplique as novas migrações antes de publicar o código correspondente.

## Desenvolvimento local

```powershell
npm run db:local
```

Crie `.dev.vars` com `ADMIN_PASSWORD=uma-senha-local` e execute:

```powershell
npm run dev
npm test
```

O teste automatizado usa o SQLite integrado ao Node.js 24 ou superior. O banco local de desenvolvimento é separado do remoto.

## O que foi corrigido

- A configuração antiga iniciava Django, com um app `reservas` ausente, embora o sistema estivesse em main.py com FastAPI.
- worker.js é agora o ponto de entrada. Os arquivos Python foram preservados como referência e não participam da publicação.
- Telas HTML servidas pela binding ASSETS; APIs com os mesmos caminhos das telas originais.
- SQL persistente no D1, com campos de horário e status, validação e índice de disponibilidade.
- Cadastro inicial: 2 projetores, 5 notebooks, 3 caixas de som e 4 microfones, conforme o script original. Ajuste esses totais ao acervo real antes do uso.
- Impedimento de reservas acima da quantidade de unidades em horários sobrepostos, inclusive ao reativar uma reserva.
- Correção do template JavaScript e da função de alteração de status; escape de conteúdo inserido nos cartões.
- Proteção das informações dos alunos e dos controles da direção com senha.

O reservas.db enviado tem zero equipamentos e zero reservas, e uma tabela de reservas antiga sem horários/status. Nenhum registro de aluno foi migrado porque não havia registros no arquivo. O SQLite original foi preservado; ele não é o banco utilizado na Cloudflare. Se houver outro banco com dados reais, faça uma migração específica antes do uso: não envie esse arquivo antigo por cima de um D1 em uso.

## Verificação e limites

Testes automatizados cobrem as telas e a sintaxe dos scripts, criação/listagem, limite de unidades, horários consecutivos, cancelamento, reativação, exclusão, datas inválidas e acesso administrativo. O deploy real depende de autenticação na sua conta Cloudflare; este pacote não confirma uma publicação remota.

A API de equipamentos retorna JSON, como no projeto original. A criação pública de reservas não verifica a matrícula nem tem proteção contra spam; para disponibilização ampla, acrescente verificação de identidade ou Turnstile. O acesso administrativo utiliza uma única conta da direção, não contas individuais por pessoa.

Documentação: https://developers.cloudflare.com/workers/static-assets/ e https://developers.cloudflare.com/d1/reference/migrations/
