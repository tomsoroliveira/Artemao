// =====================================================================
//  DADOS DO SITE
//  Este é o único arquivo que precisa ser editado para atualizar os
//  textos e a galeria. Depois de salvar e enviar para o GitHub,
//  o site é publicado sozinho em alguns minutos.
// =====================================================================

const SITE = {
  nome: "Artemão Laboratório Criativo",
  cidade: "Sorocaba, SP",
  // Texto da seção "Sobre o ateliê". Ajuste à vontade.
  sobre:
    "O Artemão é um laboratório criativo em Sorocaba. Reúne ateliê de produção " +
    "artística, design gráfico e oficinas de arte, incluindo oficinas de recreação " +
    "em que as crianças criam as próprias peças de madeira.",
  // WhatsApp com código do país e DDD, só números. Ex.: "5515999998888".
  // Deixe "" para não mostrar o botão de WhatsApp.
  whatsapp: "",
  instagram: "https://www.instagram.com/artemao.laboratoriocriativo",
};

// ---------------------------------------------------------------------
//  PEÇAS DA GALERIA
//  Cada peça é um bloco entre chaves. Para adicionar uma peça:
//    1. Crie a pasta  escaneamentos/<id>  com os 3 arquivos do KIRI Engine
//       (.obj, .mtl e .jpg).
//    2. Copie um bloco abaixo, cole no início da lista e troque os textos.
//       O "id" deve ser igual ao nome da pasta: só letras minúsculas,
//       números e hífen, sem espaços nem acentos.
//  Privacidade: use apenas o primeiro nome da criança, e somente com
//  autorização do responsável. Nunca publique foto do rosto.
// ---------------------------------------------------------------------
const PECAS = [
  {
    id: "foguete-teste",
    nome: "Foguete",
    autor: "",                    // primeiro nome da criança. Ex.: "Ana"
    idade: "",                    // opcional. Ex.: "7 anos"
    oficina: "Teste do projeto",  // nome da oficina
    data: "15/11/2026",
    descricao:
      "Primeiro escaneamento feito para testar o projeto. Será substituído pelas peças das oficinas.",
    fotos: [],                    // opcional. Ex.: ["fotos/foguete-1.jpg"]
    teste: true,                  // apague esta linha nas peças de verdade
  },
];
