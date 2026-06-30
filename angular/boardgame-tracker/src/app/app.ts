import { Component } from '@angular/core';
import { GameListComponent } from './components/game-list/game-list';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [GameListComponent],
  template: `<app-game-list></app-game-list>`
})
export class App {}