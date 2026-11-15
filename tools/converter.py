"""Converte os escaneamentos do KIRI Engine (OBJ + MTL + JPG) em GLB para o site.

Para cada pasta dentro de "escaneamentos/", gera em "modelos/":
  <nome-da-pasta>.glb   modelo 3D que o site exibe
  <nome-da-pasta>.webp  imagem de capa usada no cartão da galeria

Uso (na raiz do projeto):  python tools/converter.py
Requisitos:                pip install numpy pillow
"""
import io
import json
import re
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "escaneamentos"
SAIDA = RAIZ / "modelos"
TEXTURA_MAX = 2048   # lado máximo da textura, em pixels
NOME_VALIDO = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")  # ids: letras minúsculas, números e hífen
CAPA = 640           # lado da imagem de capa, em pixels


def ler_obj(caminho):
    v, vt, vn, faces = [], [], [], []
    with open(caminho, encoding="utf-8", errors="ignore") as arq:
        for linha in arq:
            if linha.startswith("v "):
                v.append(linha.split()[1:4])
            elif linha.startswith("vt "):
                vt.append(linha.split()[1:3])
            elif linha.startswith("vn "):
                vn.append(linha.split()[1:4])
            elif linha.startswith("f "):
                cantos = []
                for parte in linha.split()[1:]:
                    campos = (parte.split("/") + ["", ""])[:3]
                    cantos.append([int(c) if c else 0 for c in campos])
                for i in range(1, len(cantos) - 1):  # divide polígonos em triângulos
                    faces.append([cantos[0], cantos[i], cantos[i + 1]])
    if not v or not faces:
        raise ValueError("o arquivo OBJ não tem vértices ou faces")
    v = np.array(v, dtype=np.float32)
    vt = np.array(vt, dtype=np.float32) if vt else None
    vn = np.array(vn, dtype=np.float32) if vn else None
    f = np.array(faces, dtype=np.int64).reshape(-1, 3)
    for coluna, total in ((0, len(v)), (1, len(vt) if vt is not None else 0), (2, len(vn) if vn is not None else 0)):
        negativos = f[:, coluna] < 0          # índices relativos do formato OBJ
        f[negativos, coluna] += total + 1
    return v, vt, vn, f


def achar_textura(pasta, obj):
    for mtl in pasta.glob("*.mtl"):
        for linha in mtl.read_text(encoding="utf-8", errors="ignore").splitlines():
            if linha.strip().lower().startswith("map_kd"):
                # usa só o nome do arquivo, para nunca ler fora da pasta da peça
                nome = Path(linha.split(None, 1)[1].strip().replace("\\", "/")).name
                if nome and (pasta / nome).is_file():
                    return pasta / nome
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        achados = sorted(pasta.glob(ext))
        if achados:
            return achados[0]
    return None


def montar_malha(v, vt, vn, f):
    cantos, inverso = np.unique(f, axis=0, return_inverse=True)
    indices = inverso.reshape(-1).astype(np.uint32)
    pos = v[cantos[:, 0] - 1]
    uv = None
    if vt is not None and (cantos[:, 1] > 0).all():
        uv = vt[cantos[:, 1] - 1].copy()
        uv[:, 1] = 1.0 - uv[:, 1]             # o GLB conta a altura da textura de cima para baixo
    if vn is not None and (cantos[:, 2] > 0).all():
        nrm = vn[cantos[:, 2] - 1].copy()
    else:                                     # sem normais no arquivo: calcula pelas faces
        tri = indices.reshape(-1, 3)
        fn = np.cross(pos[tri[:, 1]] - pos[tri[:, 0]], pos[tri[:, 2]] - pos[tri[:, 0]])
        nrm = np.zeros_like(pos)
        for k in range(3):
            np.add.at(nrm, tri[:, k], fn)
    tam = np.linalg.norm(nrm, axis=1, keepdims=True)
    tam[tam == 0] = 1
    return pos, (nrm / tam).astype(np.float32), uv, indices


def preparar_textura(caminho):
    img = Image.open(caminho).convert("RGB")   # regravar a imagem descarta metadados (EXIF, GPS)
    if max(img.size) > TEXTURA_MAX:
        img.thumbnail((TEXTURA_MAX, TEXTURA_MAX), Image.LANCZOS)
    saida = io.BytesIO()
    img.save(saida, "JPEG", quality=85)
    return img, saida.getvalue()


def alinhar(dados, enchimento=b"\0"):
    return dados + enchimento * ((4 - len(dados) % 4) % 4)


# Texto gravado dentro de cada arquivo GLB. Mantenha igual ao campo "licenca" de dados.js.
LICENCA = "Artemão Laboratório Criativo. Uso pessoal e não comercial, citando o ateliê."


def gravar_glb(destino, pos, nrm, uv, indices, jpeg):
    partes = [pos.tobytes(), nrm.tobytes(), indices.tobytes()]
    alvos = [34962, 34962, 34963]
    atributos = {"POSITION": 0, "NORMAL": 1}
    acessores = [
        {"bufferView": 0, "componentType": 5126, "count": len(pos), "type": "VEC3",
         "min": pos.min(0).tolist(), "max": pos.max(0).tolist()},
        {"bufferView": 1, "componentType": 5126, "count": len(nrm), "type": "VEC3"},
        {"bufferView": 2, "componentType": 5125, "count": len(indices), "type": "SCALAR"},
    ]
    material = {"name": "peca", "doubleSided": True,
                "pbrMetallicRoughness": {"metallicFactor": 0, "roughnessFactor": 1}}
    gltf = {"asset": {"version": "2.0", "generator": "tools/converter.py", "copyright": LICENCA},
            "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0, "name": "peca"}]}
    if uv is not None and jpeg:
        partes += [uv.astype(np.float32).tobytes(), jpeg]
        alvos += [34962, None]
        atributos["TEXCOORD_0"] = 3
        acessores.append({"bufferView": 3, "componentType": 5126, "count": len(uv), "type": "VEC2"})
        material["pbrMetallicRoughness"]["baseColorTexture"] = {"index": 0}
        gltf["textures"] = [{"source": 0, "sampler": 0}]
        gltf["samplers"] = [{"magFilter": 9729, "minFilter": 9987}]
        gltf["images"] = [{"bufferView": 4, "mimeType": "image/jpeg"}]
    else:
        material["pbrMetallicRoughness"]["baseColorFactor"] = [0.72, 0.52, 0.32, 1]  # tom de madeira
    vistas, binario = [], b""
    for parte, alvo in zip(partes, alvos):
        vista = {"buffer": 0, "byteOffset": len(binario), "byteLength": len(parte)}
        if alvo:
            vista["target"] = alvo
        vistas.append(vista)
        binario += alinhar(parte)
    gltf.update({"meshes": [{"primitives": [{"attributes": atributos, "indices": 2, "material": 0}]}],
                 "materials": [material], "accessors": acessores, "bufferViews": vistas,
                 "buffers": [{"byteLength": len(binario)}]})
    texto = alinhar(json.dumps(gltf, separators=(",", ":")).encode(), b" ")
    with open(destino, "wb") as arq:
        arq.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(texto) + 8 + len(binario)))
        arq.write(struct.pack("<I4s", len(texto), b"JSON") + texto)
        arq.write(struct.pack("<I4s", len(binario), b"BIN\0") + binario)


def gravar_capa(destino, pos, uv, indices, textura):
    """Desenha uma vista da peça (pontos coloridos pela textura) com fundo transparente."""
    tri = indices.reshape(-1, 3)
    a, b, c = pos[tri[:, 0]], pos[tri[:, 1]], pos[tri[:, 2]]
    area = np.linalg.norm(np.cross(b - a, c - a), axis=1)
    if area.sum() == 0:
        return
    rng = np.random.default_rng(0)
    n = 2_500_000
    t = rng.choice(len(tri), n, p=area / area.sum())
    r1, r2 = rng.random(n), rng.random(n)
    fora = r1 + r2 > 1
    r1[fora], r2[fora] = 1 - r1[fora], 1 - r2[fora]
    r3 = 1 - r1 - r2
    p = a[t] * r1[:, None] + b[t] * r2[:, None] + c[t] * r3[:, None]
    if uv is not None and textura is not None:
        u = uv[tri[t, 0]] * r1[:, None] + uv[tri[t, 1]] * r2[:, None] + uv[tri[t, 2]] * r3[:, None]
        tex = np.asarray(textura)
        alt, larg = tex.shape[:2]
        cor = tex[np.clip((u[:, 1] * alt).astype(int), 0, alt - 1),
                  np.clip((u[:, 0] * larg).astype(int), 0, larg - 1)]
    else:
        cor = np.tile(np.array([184, 133, 82], np.uint8), (n, 1))
    p = p - (pos.min(0) + pos.max(0)) / 2
    giro, inclinacao = 0.6, 0.45
    cg, sg, ci, si = np.cos(giro), np.sin(giro), np.cos(inclinacao), np.sin(inclinacao)
    x = p[:, 0] * cg + p[:, 2] * sg
    z = -p[:, 0] * sg + p[:, 2] * cg
    y = p[:, 1] * ci - z * si
    fundo = p[:, 1] * si + z * ci
    escala = max(np.abs(x).max(), np.abs(y).max()) / 0.46
    px = ((x / escala + 0.5) * CAPA).astype(int)
    py = ((0.5 - y / escala) * CAPA).astype(int)
    ok = (px >= 0) & (px < CAPA) & (py >= 0) & (py < CAPA)
    ordem = np.argsort(fundo[ok])
    img = np.zeros((CAPA, CAPA, 4), np.uint8)
    img[py[ok][ordem], px[ok][ordem], :3] = cor[ok][ordem]
    img[py[ok][ordem], px[ok][ordem], 3] = 255
    Image.fromarray(img, "RGBA").save(destino, "WEBP", quality=82)


def converter_pasta(pasta):
    if not NOME_VALIDO.match(pasta.name):
        raise ValueError("nome de pasta inválido: use só letras minúsculas, números e hífen")
    objs = sorted(pasta.glob("*.obj"))
    if not objs:
        print(f"  {pasta.name}: nenhum arquivo .obj encontrado, pasta ignorada")
        return False
    v, vt, vn, f = ler_obj(objs[0])
    pos, nrm, uv, indices = montar_malha(v, vt, vn, f)
    caminho_textura = achar_textura(pasta, objs[0])
    textura, jpeg = (None, None)
    if caminho_textura is not None and uv is not None:
        textura, jpeg = preparar_textura(caminho_textura)
    gravar_glb(SAIDA / f"{pasta.name}.glb", pos, nrm, uv, indices, jpeg)
    gravar_capa(SAIDA / f"{pasta.name}.webp", pos, uv, indices, textura)
    tamanho = (SAIDA / f"{pasta.name}.glb").stat().st_size / 1e6
    print(f"  {pasta.name}: {len(indices) // 3} triângulos, {tamanho:.1f} MB"
          + ("" if jpeg else " (sem textura: usando tom de madeira)"))
    return True


def main():
    SAIDA.mkdir(exist_ok=True)
    pastas = sorted(p for p in ENTRADA.iterdir() if p.is_dir()) if ENTRADA.exists() else []
    if not pastas:
        print("Nenhuma pasta em 'escaneamentos/'. Nada para converter.")
        return 0
    print(f"Convertendo {len(pastas)} escaneamento(s):")
    erros = 0
    for pasta in pastas:
        try:
            converter_pasta(pasta)
        except Exception as erro:  # uma pasta com problema não impede as outras
            erros += 1
            print(f"  {pasta.name}: ERRO - {erro}")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
