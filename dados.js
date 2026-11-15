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
  // WhatsApp do ateliê com código do país e DDD, só números. Ex.: "5515999998888".
  // Deixe "" para não mostrar o botão de WhatsApp.
  whatsapp: "",
  // Endereço completo do Instagram do ateliê, começando com https://
  instagram: "https://www.instagram.com/artemao.laboratoriocriativo",
};

// ---------------------------------------------------------------------
//  OFICINAS
//  A galeria é agrupada por oficina. A primeira da lista aparece
//  selecionada, então coloque sempre a mais recente no início.
//  O "id" usa só letras minúsculas, números e hífen.
// ---------------------------------------------------------------------
const OFICINAS = [
  {
    id: "teste-15-11-2026",
    nome: "Teste do projeto",
    data: "15/11/2026",
  },
  // Exemplo de uma oficina de verdade:
  // { id: "sesc-15-11-2026", nome: "Sesc Sorocaba", data: "15/11/2026" },
];

// ---------------------------------------------------------------------
//  PEÇAS
//  Para adicionar uma peça:
//    1. Crie a pasta  escaneamentos/<id>  com os 3 arquivos do KIRI Engine
//       (.obj, .mtl e .jpg).
//    2. Copie um bloco abaixo, cole na lista e troque os textos.
//       "id" deve ser igual ao nome da pasta (letras minúsculas, números
//       e hífen). "oficina" deve ser o id de uma oficina da lista acima.
// ---------------------------------------------------------------------
const PECAS = [
  {
    id: "foguete-teste",
    oficina: "teste-15-11-2026",
    nome: "Foguete",
    descricao:
      "Primeiro escaneamento, feito para testar o projeto. Será substituído pelas peças das oficinas.",
    fotos: [],      // opcional. Ex.: ["fotos/foguete-1.jpg"]
    teste: true,    // apague esta linha nas peças de verdade
  },
];
