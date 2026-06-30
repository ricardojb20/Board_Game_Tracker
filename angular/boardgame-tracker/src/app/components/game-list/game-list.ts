import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GameService } from '../../services/game.service';
import { Game } from '../../models/game';

@Component({
  selector: 'app-game-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-list.html',
  styleUrl: './game-list.css'
})
export class GameListComponent implements OnInit {

  games: Game[] = [];

  constructor(private gameService: GameService) {}

  ngOnInit(): void {
  this.gameService.getGames().subscribe(data => {
    console.log(data);
    this.games = data;
    });
  }

  goToGame(game: Game) {
    console.log(game.id_game);
  }
}