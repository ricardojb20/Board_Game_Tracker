import {Component, OnInit, ChangeDetectorRef} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ActivatedRoute} from '@angular/router';

import {GameService} from '../../services/game.service';
import {Game} from '../../models/game';
import {Price} from '../../models/price';

@Component({
  selector: 'app-game-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-detail.html',
    styleUrls: ['./game-detail.css']
})
export class GameDetailComponent implements OnInit {
    game?: Game;
    prices: Price[] = [];

    constructor(
        private route: ActivatedRoute,
        private gameService: GameService,
        private cdr: ChangeDetectorRef
    ) {}

    ngOnInit(): void {
        const gameId = Number(this.route.snapshot.paramMap.get('id'));

        this.gameService.getGameById(gameId).subscribe((game) => {
            this.game = game;
            this.cdr.detectChanges();
        });

        this.gameService.getPricesByGameId(gameId).subscribe((prices) => {
            this.prices = prices;
            this.cdr.detectChanges();
        });
    }
}