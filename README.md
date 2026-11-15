# Galeria 3D Artemão

Site que mostra, em 3D, as peças de madeira criadas pelas crianças nas oficinas do
Artemão Laboratório Criativo (Sorocaba, SP). Projeto de extensão universitária do
curso CST em DevOps, desenvolvido por Wellington Eduardo de Oliveira.

Tudo o que o projeto usa é gratuito: KIRI Engine (escaneamento), GitHub (código e
automação) e GitHub Pages (hospedagem).

## Como funciona

1. A peça é escaneada com o aplicativo **KIRI Engine** (Android ou iPhone), no modo Photo Scan.
2. O aplicativo exporta três arquivos: `.obj`, `.mtl` e `.jpg`.
3. Os três arquivos são enviados para uma pasta dentro de `escaneamentos/`.
4. O GitHub converte os arquivos para o formato GLB, gera a imagem de capa e publica o site.
   Esse passo é automático e leva alguns minutos.
5. A família abre o site pelo QR code ou pelo link e gira a peça na tela.

## Estrutura do projeto

| Caminho | O que é |
|---|---|
| `index.html` | A página do site |
| `dados.js` | Textos do ateliê e lista de peças. É o arquivo que se edita no dia a dia |
| `escaneamentos/<id>/` | Arquivos exportados pelo KIRI Engine, uma pasta por peça |
| `fotos/` | Fotos opcionais das peças |
| `modelos/` | Modelos GLB e capas, gerados automaticamente. Não editar |
| `tools/converter.py` | Conversor de OBJ para GLB |
| `.github/workflows/publicar.yml` | Automação que converte e publica o site |

## Como adicionar uma peça

1. **Escaneie a peça** no KIRI Engine:
   - peça sobre uma mesa, com jornal ou toalha estampada por baixo;
   - boa luz, sem flash, sem mexer na peça;
   - 40 a 60 fotos em duas voltas (uma na altura da peça, outra de cima), com a peça ocupando boa parte da tela;
   - depois do processamento, use o recorte (crop) do aplicativo para deixar só a peça;
   - exporte com as opções extras desligadas.
2. **Escolha um id** para a peça, só com letras minúsculas, números e hífen. Exemplo: `carrinho-ana`.
3. **Envie os três arquivos** para a pasta `escaneamentos/<id>/`. No site do GitHub:
   *Add file* > *Upload files*, e digite `escaneamentos/<id>/` antes do nome do arquivo.
4. **Adicione a peça em `dados.js`**: copie um bloco da lista `PECAS`, cole no início e troque os textos.
   O campo `id` deve ser igual ao nome da pasta.
5. **Salve** (*Commit changes*). Em alguns minutos a peça aparece no site.

O andamento da publicação aparece na aba **Actions** do repositório. Um sinal verde
indica que o site foi publicado; um sinal vermelho indica erro, com a mensagem do
que falhou.

## Link direto e QR code de uma peça

Cada peça tem endereço próprio: `endereço-do-site/#peca-<id>`. Esse endereço pode ser
transformado em QR code para a família abrir a peça da criança diretamente.

## Privacidade

- Publicar apenas a peça, nunca o rosto da criança.
- Usar somente o primeiro nome, e apenas com autorização do responsável.
- Para remover uma peça, apague o bloco dela em `dados.js` e a pasta em `escaneamentos/`.

## Testar no computador (opcional)

Requer Python 3 instalado.

```
pip install numpy pillow
python tools/converter.py
python -m http.server 8000
```

Depois abra `http://localhost:8000` no navegador.
