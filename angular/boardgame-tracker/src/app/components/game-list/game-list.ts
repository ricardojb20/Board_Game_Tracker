import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GameService } from '../../services/game.service';
import { Game } from '../../models/game';

import { Router } from '@angular/router';

@Component({
  selector: 'app-game-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-list.html',
  styleUrl: './game-list.css'
})
export class GameListComponent implements OnInit {

  games: Game[] = [];

  constructor(private gameService: GameService, private cdr: ChangeDetectorRef, private router: Router) {}

  ngOnInit(): void { // Fetch the list of games when the component initializes
  this.gameService.getGames().subscribe(data => {
    console.log(data);
    this.games = data;
    this.cdr.detectChanges(); // Trigger change detection after updating the games array to ensure the view is updated
    });
  }

  goToGame(game: Game) {
    this.router.navigate(['/games', game.id_game]); // Navigate to the game detail page
  }
}