import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

import { GameService } from '../../services/game.service';
import { Game } from '../../models/game';

@Component({
  selector: 'app-game-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-list.html',
  styleUrl: './game-list.css'
})
export class GameListComponent {

  games$: Observable<Game[]>;

  constructor(private gameService: GameService,private router: Router) {
    this.games$ = this.gameService.getGames();
  }

  goToGame(game: Game) {
    this.router.navigate(['/games', game.id_game]);
  }

}