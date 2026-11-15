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

As pastas `modelos/` e `_site/` são geradas automaticamente e não ficam no repositório.

## Como adicionar uma oficina

Em `dados.js`, copie um bloco da lista `OFICINAS`, cole **no início** da lista e troque os textos.
A primeira oficina da lista é a que aparece selecionada no site.

```
{ id: "sesc-15-11-2026", nome: "Sesc Sorocaba", data: "15/11/2026" },
```

O `id` usa só letras minúsculas, números e hífen.

## Como adicionar uma peça

1. **Escaneie a peça** no KIRI Engine:
   - peça sobre uma mesa, com jornal ou toalha estampada por baixo;
   - boa luz, sem flash, sem mexer na peça;
   - 40 a 60 fotos em duas voltas (uma na altura da peça, outra de cima), com a peça ocupando boa parte da tela;
   - depois do processamento, use o recorte (crop) do aplicativo para deixar só a peça;
   - exporte com as opções extras desligadas.
2. **Escolha um id** para a peça, só com letras minúsculas, números e hífen. Exemplo: `carrinho-01`.
3. **Envie os três arquivos** para a pasta `escaneamentos/<id>/`. No site do GitHub:
   *Add file* > *Upload files*, arrastando a pasta da peça para dentro de `escaneamentos`.
4. **Adicione a peça em `dados.js`**: copie um bloco da lista `PECAS`, cole na lista e troque os textos.
   O campo `id` deve ser igual ao nome da pasta, e o campo `oficina` deve ser o `id` de uma oficina.
5. **Salve** (*Commit changes*). Em alguns minutos a peça aparece no site.

O andamento aparece na aba **Actions** do repositório. Sinal verde indica que o site foi
publicado. Sinal vermelho indica que a publicação foi interrompida; ao clicar na execução,
a mensagem diz o motivo, e o site anterior continua no ar.

## Links diretos e QR code

- Oficina: `endereço-do-site/#oficina-<id>`
- Peça: `endereço-do-site/#peca-<id>`

Qualquer um desses endereços pode virar QR code.

## Segurança e privacidade

O site mostra apenas objetos. Não publica nomes, fotos de pessoas nem dados de participantes.

**O que o site faz**

- Não usa cookies, não tem formulários, não tem cadastro e não coleta dados de quem visita.
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
- Para remover uma peça, apague o bloco dela em `dados.js` e a pasta em `escaneamentos/`.

**Limite conhecido:** o GitHub Pages não permite configurar cabeçalhos de segurança do
servidor. Por isso a política de segurança fica dentro da página, e o site não tem como
impedir que outra página o exiba dentro de uma moldura. Como o site não tem login nem
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
