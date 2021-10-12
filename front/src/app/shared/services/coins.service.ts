import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Coin, CoinResponse } from './coin.model';

@Injectable({
  providedIn: 'root'
})
export class CoinsService {

  // private coinsSource = new Subject<Coin[]>();

  // observable
  coins$ = new Observable<Coin[]>();
  // coins$ = []

  constructor(
    private _http: HttpClient
  ) {

  }

  getCoins(): Observable<CoinResponse> {
    return this._http.get<CoinResponse>(`${environment.apiUrl}/coins/`)
  }
}