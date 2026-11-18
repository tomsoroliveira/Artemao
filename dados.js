// =====================================================================
//  DADOS DO SITE
//  Este é o único arquivo que precisa ser editado para atualizar os
//  textos e a galeria. Depois de salvar e enviar para o GitHub,
//  o site é publicado sozinho em alguns minutos.
//
//  Segurança: não coloque aqui nomes de participantes, telefones
//  pessoais ou qualquer dado de pessoas. O site mostra apenas objetos.
// =====================================================================

const SITE = {
  nome: "Artemão Laboratório Criativo",
  cidade: "Sorocaba, SP",
  // Texto da seção "Sobre o ateliê". Ajuste à vontade.
  sobre:
    "O Artemão é um laboratório criativo em Sorocaba. Reúne ateliê de produção " +
    "artística, design gráfico e oficinas de arte abertas a todos os públicos, " +
    "em que cada participante cria a própria peça.",
  // Endereço completo do Instagram do ateliê, começando com https://
  instagram: "https://www.instagram.com/artemao.laboratoriocriativo",
  // Botão "Baixar arquivo 3D" em cada peça. Troque para false para desligar.
  permitirDownload: true,
  // Licença das peças, mostrada junto ao botão de download e gravada no arquivo baixado
  // (para mudar o texto no arquivo, altere também LICENCA em tools/converter.py).
  licenca:
    "Artemão Laboratório Criativo. Uso pessoal e não comercial, citando o ateliê. " +
    "Para outros usos, fale com o ateliê.",
};

// ---------------------------------------------------------------------
//  OFICINAS (galerias)
//  A galeria é agrupada por oficina. A primeira da lista aparece
//  selecionada, então coloque sempre a mais recente no início.
//  O "id" usa só letras minúsculas, números e hífen.
//  O campo "data" é opcional. Exemplo de uma oficina de verdade:
//  { id: "sesc-15-11-2026", nome: "Sesc Sorocaba", data: "15/11/2026" },
// ---------------------------------------------------------------------
const OFICINAS = [
  { id: "pecas-do-atelie", nome: "Peças do ateliê" },
];

// ---------------------------------------------------------------------
//  PEÇAS
//  Para adicionar uma peça:
//    1. Crie a pasta  escaneamentos/<modelo>  com os 3 arquivos do KIRI
//       Engine (.obj, .mtl e .jpg).
//    2. Copie um bloco abaixo, cole na lista e troque os textos.
//       "id": nome único da peça (letras minúsculas, números e hífen).
//       "oficina": id de uma oficina da lista acima.
//       "modelo": nome da pasta em escaneamentos. Se for omitido, vale o "id".
//       Várias peças podem usar o mesmo modelo, como abaixo.
// ---------------------------------------------------------------------
const PECAS = [
  {
    id: "barco",
    oficina: "pecas-do-atelie",
    nome: "Barco",
    descricao: "Peça de madeira escaneada em 3D.",
    fotos: [],      // opcional. Ex.: ["fotos/barco-1.jpg"]
  },
  {
    id: "bob",
    oficina: "pecas-do-atelie",
    nome: "Bob",
    descricao: "Peça de madeira escaneada em 3D.",
    fotos: [],
  },
  {
    id: "instrumento",
    oficina: "pecas-do-atelie",
    nome: "Instrumento",
    descricao: "Peça de madeira escaneada em 3D.",
    fotos: [],
  },
];
