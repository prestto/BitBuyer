import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Coin, CoinResponse, CoinDetail } from '../models/coin.model';

@Injectable({
  providedIn: 'root'
})
export class CoinsService {
  // observable
  coins$ = new Observable<Coin[]>();

  constructor(
    private _http: HttpClient
  ) {

  }

  getCoins(): Observable<CoinResponse> {
    const headers = new HttpHeaders()
      .set('content-type', 'application/json');
    return this._http.get<CoinResponse>(`${environment.apiUrl}/coins/`, { 'headers': headers })
  }

  getCoinDetail(coinId: number): Observable<CoinDetail> {
    const headers = new HttpHeaders()
      .set('content-type', 'application/json');
    return this._http.get<CoinDetail>(`${environment.apiUrl}/coins/${coinId}`, { 'headers': headers })
  }
}