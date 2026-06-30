import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';

import { GameService } from '../../services/game.service';
import { Game } from '../../models/game';
import { Price } from '../../models/price';

@Component({
  selector: 'app-game-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-detail.html',
  styleUrls: ['./game-detail.css']
})
export class GameDetailComponent {

  game$: Observable<Game>;
  prices$: Observable<Price[]>;

  constructor(private route: ActivatedRoute,private gameService: GameService) {

    const gameId = Number(this.route.snapshot.paramMap.get('id'));

    this.game$ = this.gameService.getGameById(gameId);
    this.prices$ = this.gameService.getPricesByGameId(gameId);

  }

}