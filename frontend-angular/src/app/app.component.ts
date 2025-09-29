import { Component, OnInit } from '@angular/core';
import { PetService } from './services/pet.service';
import { Pet, PetCreate, Servico, ServicoCreate } from './models/pet.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  pets: Pet[] = [];
  busca = '';
  especieFiltro = '';
  
  // Formulário de cadastro
  novoPet: PetCreate = { nome: '', especie: 'Cachorro', tutor: '' };
  mostrarFormulario = false;
  
  // Modal de serviços
  petSelecionado: Pet | null = null;
  servicos: Servico[] = [];
  novoServico: ServicoCreate = { descricao: '' };
  mostrarModalServicos = false;
  mostrarFormularioServico = false;

  constructor(private petService: PetService) {}

  ngOnInit() {
    this.carregarPets();
  }

  carregarPets() {
    this.petService.listarPets(this.busca, this.especieFiltro).subscribe(
      pets => this.pets = pets
    );
  }

  filtrarPets() {
    this.carregarPets();
  }

  cadastrarPet() {
    if (this.novoPet.nome && this.novoPet.tutor) {
      this.petService.criarPet(this.novoPet).subscribe(() => {
        this.carregarPets();
        this.novoPet = { nome: '', especie: 'Cachorro', tutor: '' };
        this.mostrarFormulario = false;
      });
    }
  }

  excluirPet(pet: Pet) {
    if (confirm(`Tem certeza que deseja excluir ${pet.nome}?`)) {
      this.petService.excluirPet(pet.id).subscribe(() => {
        this.carregarPets();
      });
    }
  }

  abrirHistorico(pet: Pet) {
    this.petSelecionado = pet;
    this.mostrarModalServicos = true;
    this.carregarServicos();
  }

  carregarServicos() {
    if (this.petSelecionado) {
      this.petService.listarServicos(this.petSelecionado.id).subscribe(
        servicos => this.servicos = servicos
      );
    }
  }

  adicionarServico() {
    if (this.petSelecionado && this.novoServico.descricao) {
      this.petService.adicionarServico(this.petSelecionado.id, this.novoServico).subscribe(() => {
        this.carregarServicos();
        this.novoServico = { descricao: '' };
        this.mostrarFormularioServico = false;
      });
    }
  }

  fecharModal() {
    this.mostrarModalServicos = false;
    this.mostrarFormularioServico = false;
    this.petSelecionado = null;
    this.servicos = [];
  }

  formatarData(data: string): string {
    return new Date(data).toLocaleString('pt-BR');
  }
}