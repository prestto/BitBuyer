import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Article, ArticleListResponse } from '../models/article.model'

@Injectable({
  providedIn: 'root'
})
export class ArticlesService {

  constructor(
    private _http: HttpClient
  ) { }

  getArticleList(coinId: number): Observable<ArticleListResponse> {
    const headers = new HttpHeaders()
      .set('content-type', 'application/json');
    return this._http.get<ArticleListResponse>(`${environment.apiUrl}/coins/${coinId}/articles`, { 'headers': headers })
  }
}
