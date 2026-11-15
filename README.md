# Portfólio 3D Artemão

Site que mostra, em 3D, as peças criadas nas oficinas do Artemão Laboratório Criativo
(Sorocaba, SP), agrupadas por oficina. Projeto de extensão universitária do curso
CST em DevOps.

Tudo o que o projeto usa é gratuito: KIRI Engine (escaneamento), GitHub (código e
automação) e GitHub Pages (hospedagem).

## Como funciona

1. A peça é escaneada com o aplicativo **KIRI Engine** (Android ou iPhone), no modo Photo Scan.
2. O aplicativo exporta três arquivos: `.obj`, `.mtl` e `.jpg`.
3. Os três arquivos são enviados para uma pasta dentro de `escaneamentos/`.
4. O GitHub converte os arquivos para o formato GLB, gera a imagem de capa, faz as
   verificações de segurança e publica o site. Esse passo é automático e leva alguns minutos.
5. Qualquer pessoa abre o site pelo QR code ou pelo link, escolhe a oficina e gira a peça na tela.

## Estrutura do projeto

| Caminho | O que é |
|---|---|
| `index.html`, `estilo.css`, `app.js` | A página do site, sua aparência e seu funcionamento |
| `dados.js` | Textos do ateliê, lista de oficinas e lista de peças. É o arquivo que se edita no dia a dia |
| `escaneamentos/<id>/` | Arquivos exportados pelo KIRI Engine, uma pasta por peça |
| `fotos/` | Fotos opcionais das peças |
| `tools/converter.py` | Converte OBJ em GLB e gera as capas |
| `tools/montar_site.py` | Faz as verificações de segurança e monta a pasta publicada |
| `tools/requirements.txt` | Bibliotecas usadas, com versões fixas |
| `.github/workflows/publicar.yml` | Automação que converte, verifica e publica o site |
| `.github/dependabot.yml`, `SECURITY.md` | Verificação mensal de versões e contato para avisos de segurança |

As pastas `modelos/` e `_site/` são geradas automaticamente e não ficam no repositório.

## Como adicionar uma oficina

Em `dados.js`, copie um bloco da lista `OFICINAS`, cole **no início** da lista e troque os textos.
A primeira oficina da lista é a que aparece selecionada no site.

```
{ id: "sesc-15-11-2026", nome: "Sesc Sorocaba", data: "15/11/2026" },
```

O `id` usa só letras minúsculas, números e hífen. O campo `data` é opcional.
Para renomear uma das galerias de exemplo, troque o `nome` (e, se quiser, o `id`; nesse caso,
troque também o campo `oficina` das peças que apontam para ela).

## Como adicionar uma peça

1. **Escaneie a peça** no KIRI Engine:
   - peça sobre uma mesa, com jornal ou toalha estampada por baixo;
   - boa luz, sem flash, sem mexer na peça;
   - 40 a 60 fotos em duas voltas (uma na altura da peça, outra de cima), com a peça ocupando boa parte da tela;
   - depois do processamento, use o recorte (crop) do aplicativo para deixar só a peça;
   - exporte com as opções extras desligadas.
2. **Escolha um nome de modelo**, só com letras minúsculas, números e hífen. Exemplo: `carrinho-01`.
3. **Envie os três arquivos** para a pasta `escaneamentos/<modelo>/`. No site do GitHub:
   *Add file* > *Upload files*, arrastando a pasta da peça para dentro de `escaneamentos`.
4. **Adicione a peça em `dados.js`**: copie um bloco da lista `PECAS`, cole na lista e troque os textos.
   O campo `modelo` deve ser igual ao nome da pasta (se for omitido, vale o `id` da peça), e o campo
   `oficina` deve ser o `id` de uma oficina. Duas peças podem usar o mesmo modelo.
5. **Salve** (*Commit changes*). Em alguns minutos a peça aparece no site.

O andamento aparece na aba **Actions** do repositório. Sinal verde indica que o site foi
publicado. Sinal vermelho indica que a publicação foi interrompida; ao clicar na execução,
a mensagem diz o motivo, e o site anterior continua no ar.

## Download do arquivo 3D

Cada peça tem o botão **Baixar arquivo 3D**, que entrega o arquivo `.glb`. Para desligar o
botão em todo o site, em `dados.js` use `permitirDownload: false`. A licença das peças (uso pessoal e não comercial, citando o ateliê) aparece junto ao botão e
no rodapé, e também é gravada dentro do arquivo baixado. O texto fica em `licenca` (`dados.js`) e em
`LICENCA` (`tools/converter.py`). Combine com o ateliê qualquer mudança.

## Links diretos e QR code

- Oficina: `endereço-do-site/#oficina-<id>`
- Peça: `endereço-do-site/#peca-<id>`

Qualquer um desses endereços pode virar QR code.

## Segurança e privacidade

O site mostra apenas objetos. Não publica nomes, fotos de pessoas nem dados de participantes.

**O que o site faz**

- Não usa cookies, não tem formulários, não tem cadastro e não tem ferramentas de rastreamento
  nem estatísticas de acesso.
- Se for aberto dentro de uma moldura de outro site, não mostra o conteúdo (só um link para abrir direto).
- Força o uso de HTTPS em todos os arquivos.
- Carrega arquivos somente do próprio endereço. Nenhum script, fonte ou imagem vem de outros
  sites; o visualizador 3D é copiado para dentro do site na publicação, em versão fixa.
- Tem política de segurança de conteúdo (CSP) que bloqueia scripts embutidos e de terceiros.
- Trata todo texto de `dados.js` como texto puro e valida ids, fotos e links antes de usar.
- Abre links externos sem repassar informações da página de origem.

**O que a publicação verifica** (e interrompe se encontrar)

- Fotos com localização (GPS) nas pastas `fotos/` e `escaneamentos/`.
- E-mail, CPF ou chave de acesso em `dados.js`.
- Script embutido ou script de outro site em `index.html`, ou falta da política de segurança.

Além disso, as fotos publicadas são regravadas sem metadados, e só entram no site os
arquivos previstos em `tools/montar_site.py`.

**Cuidados de quem mantém o site**

- O repositório é público: tudo o que for enviado a ele pode ser visto por qualquer pessoa,
  inclusive o histórico. Não envie documentos, senhas nem fotos de pessoas.
- Ative a verificação em duas etapas na conta do GitHub (Settings > Password and authentication).
- Para o e-mail da conta não aparecer nas alterações: Settings > Emails > *Keep my email addresses private*.
- Em Settings > Pages, mantenha *Enforce HTTPS* marcado.
- **Cuidado com o fundo do escaneamento.** O modelo 3D captura tudo o que está na cena. Antes de
  publicar, use o recorte (crop) do KIRI e confira que não há rostos, documentos, telas ou
  ambientes de casa no modelo. Prefira escanear sobre jornal, toalha ou mesa lisa.
- Peças com download liberado podem ser copiadas e reutilizadas por qualquer pessoa.
- Para remover uma peça, apague o bloco dela em `dados.js` e a pasta em `escaneamentos/`.

**Proteção da conta e do repositório** (configurar uma vez, em Settings do repositório)

- *Code security*: ligar **Dependabot alerts**, **Dependabot security updates** e **Secret scanning**
  (com *Push protection*). O arquivo `.github/dependabot.yml` já agenda a verificação mensal das
  versões usadas pelo projeto; os avisos aparecem em *Pull requests*.
- *Rules > Rulesets > New branch ruleset*: nome `proteger-main`, *Enforcement* **Active**, alvo
  *Default branch*, marcar **Restrict deletions** e **Block force pushes**. Isso impede apagar a
  branch `main` ou reescrever o histórico por engano.
- *Actions > General*: em *Workflow permissions*, deixar **Read repository contents** e, em
  *Fork pull request workflows*, manter a exigência de aprovação para colaboradores externos.
- *Collaborators*: dar acesso só a quem precisa. Quem tiver acesso de escrita publica no site,
  então cada pessoa deve usar verificação em duas etapas.
- Guardar os códigos de recuperação da verificação em duas etapas em local seguro (fora do repositório).
- Se um dia um dado sensível for enviado por engano, apagar o arquivo não basta, pois ele continua
  no histórico: troque a senha ou chave envolvida e peça ajuda para limpar o histórico.

**Hospedagem:** o site em si não coleta nada, mas, como acontece com qualquer site, o GitHub
(que hospeda as páginas) registra os acessos em seus servidores, conforme a política de privacidade
dele. O ateliê não tem acesso a esses registros.

**Limite conhecido:** o GitHub Pages não permite configurar cabeçalhos de segurança do
servidor. Por isso a política de segurança fica dentro da página, e o site não tem como
impedir, no servidor, que outra página o exiba dentro de uma moldura; por isso a própria página se esconde nesse caso. Como o site não tem login nem
ações sensíveis, o risco é baixo.

## Testar no computador (opcional)

Requer Python 3.

```
pip install -r tools/requirements.txt
python tools/converter.py
python tools/montar_site.py
python -m http.server 8000 --directory _site
```

Depois abra `http://localhost:8000` no navegador.
