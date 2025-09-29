export interface Pet {
  id: number;
  nome: string;
  especie: string;
  tutor: string;
  criado_em: string;
}

export interface PetCreate {
  nome: string;
  especie: string;
  tutor: string;
}

export interface Servico {
  id: number;
  pet_id: number;
  descricao: string;
  data: string;
}

export interface ServicoCreate {
  descricao: string;
}