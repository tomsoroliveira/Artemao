"""Monta a pasta "_site", que é o que vai para o ar.

Só entram no site os arquivos listados aqui. Nada mais do repositório é publicado.
Antes de montar, o script faz verificações de segurança e interrompe a publicação
se encontrar algum problema.

Uso (na raiz do projeto, depois de tools/converter.py):  python tools/montar_site.py
"""
import hashlib
import re
import shutil
import sys
import urllib.request
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
SITE = RAIZ / "_site"
PAGINAS = ["index.html", "estilo.css", "app.js", "dados.js"]

# Visualizador 3D (biblioteca model-viewer, do Google). A versão é fixa e o arquivo
# é copiado para dentro do site, para que os visitantes não dependam de outros sites.
MV_VERSAO = "3.5.0"
MV_URL = f"https://cdn.jsdelivr.net/npm/@google/model-viewer@{MV_VERSAO}/dist/model-viewer.min.js"
# Impressão digital (SHA-256) esperada do arquivo. Quando preenchida, a publicação
# é interrompida se o arquivo baixado for diferente. O valor aparece no log da publicação.
MV_SHA256 = ""

FOTO_VALIDA = re.compile(r"^[A-Za-z0-9._-]+\.(jpg|jpeg|png|webp)$", re.IGNORECASE)
EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".webp"}
# Só estes formatos são abertos pela biblioteca de imagens (reduz a superfície de ataque).
FORMATOS_IMAGEM = ["JPEG", "PNG", "WEBP"]
GPS_IFD = 0x8825
# Padrões que não devem aparecer em dados.js: e-mail, CPF e chaves de acesso.
PADROES_SENSIVEIS = {
    "endereço de e-mail": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "número de CPF": re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"),
    "chave de acesso": re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,})"),
}


def tem_gps(caminho):
    try:
        with Image.open(caminho, formats=FORMATOS_IMAGEM) as img:
            return bool(img.getexif().get_ifd(GPS_IFD))
    except Exception:
        return False


def verificar():
    problemas = []
    for nome in PAGINAS:
        if not (RAIZ / nome).is_file():
            problemas.append(f"arquivo obrigatório ausente: {nome}")
    # 1. Fotos com localização (GPS) revelam onde foram tiradas.
    for pasta in ("fotos", "escaneamentos"):
        base = RAIZ / pasta
        if not base.exists():
            continue
        for arq in sorted(base.rglob("*")):
            if arq.is_file() and arq.suffix.lower() in EXTENSOES_IMAGEM and tem_gps(arq):
                problemas.append(f"{arq.relative_to(RAIZ)} contém localização (GPS). "
                                 "Remova a localização da foto e envie de novo.")
    # 2. Dados pessoais ou chaves em dados.js.
    dados = RAIZ / "dados.js"
    if dados.is_file():
        texto = dados.read_text(encoding="utf-8", errors="ignore")
        for descricao, padrao in PADROES_SENSIVEIS.items():
            if padrao.search(texto):
                problemas.append(f"dados.js parece conter {descricao}. Remova antes de publicar.")
    # 3. A página não pode ter código embutido nem carregar scripts de outros sites.
    pagina = RAIZ / "index.html"
    if pagina.is_file():
        html = pagina.read_text(encoding="utf-8", errors="ignore")
        if "Content-Security-Policy" not in html:
            problemas.append("index.html está sem a política de segurança (Content-Security-Policy).")
        for src in re.findall(r"<script\b[^>]*\bsrc=[\"']([^\"']+)[\"']", html, re.IGNORECASE):
            if re.match(r"^(https?:)?//", src):
                problemas.append(f"index.html carrega um script de outro site: {src}")
        if re.search(r"<script\b(?![^>]*\bsrc=)[^>]*>", html, re.IGNORECASE):
            problemas.append("index.html tem script embutido. Coloque o código em app.js.")
    return problemas


def baixar_visualizador(destino):
    with urllib.request.urlopen(MV_URL, timeout=60) as resposta:
        conteudo = resposta.read()
    digital = hashlib.sha256(conteudo).hexdigest()
    print(f"  model-viewer {MV_VERSAO}: {len(conteudo) / 1e6:.1f} MB, sha256 {digital}")
    if len(conteudo) < 100_000:
        raise RuntimeError("o arquivo do visualizador 3D veio incompleto")
    if MV_SHA256 and digital != MV_SHA256:
        raise RuntimeError("a impressão digital do visualizador 3D não confere com a esperada")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(conteudo)


def copiar_fotos():
    origem = RAIZ / "fotos"
    if not origem.exists():
        return 0
    total = 0
    for arq in sorted(origem.iterdir()):
        if not (arq.is_file() and FOTO_VALIDA.match(arq.name)):
            continue
        (SITE / "fotos").mkdir(exist_ok=True)
        with Image.open(arq, formats=FORMATOS_IMAGEM) as img:      # regravar a imagem descarta todos os metadados
            limpa = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB")
            limpa.thumbnail((1600, 1600), Image.LANCZOS)
            if arq.suffix.lower() in (".jpg", ".jpeg"):
                limpa.convert("RGB").save(SITE / "fotos" / arq.name, quality=85)
            else:
                limpa.save(SITE / "fotos" / arq.name)
        total += 1
    return total


def main():
    sem_download = "--sem-download" in sys.argv   # só para testes no computador
    print("Verificações de segurança:")
    problemas = verificar()
    if problemas:
        for p in problemas:
            print(f"  PROBLEMA: {p}")
        print("Publicação interrompida.")
        return 1
    print("  nenhum problema encontrado")

    print("Montando o site:")
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    for nome in PAGINAS:
        shutil.copy2(RAIZ / nome, SITE / nome)
    modelos = RAIZ / "modelos"
    (SITE / "modelos").mkdir()
    n_modelos = 0
    if modelos.exists():
        for arq in sorted(modelos.iterdir()):
            if arq.suffix.lower() in (".glb", ".webp"):
                shutil.copy2(arq, SITE / "modelos" / arq.name)
                n_modelos += arq.suffix.lower() == ".glb"
    n_fotos = copiar_fotos()
    if not sem_download:
        baixar_visualizador(SITE / "vendor" / "model-viewer.min.js")
    print(f"  {len(PAGINAS)} arquivos de página, {n_modelos} modelo(s) 3D, {n_fotos} foto(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
