// fazer o pedido HTTP ao API
// Consumir GET /games
// Devolver a lista de jogos

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Game } from '../models/game';

@Injectable({
  providedIn: 'root'
})
export class GameService {
    private apiUrl = 'http://127.0.0.1:8000'; 

    constructor(private http: HttpClient) { }

    getGames(): Observable<Game[]> {
        return this.http.get<Game[]>(`${this.apiUrl}/games`);
    }

    getGameById(id: number): Observable<Game> {
        return this.http.get<Game>(`${this.apiUrl}/games/${id}`);
    }
}