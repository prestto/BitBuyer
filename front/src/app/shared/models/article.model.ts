export interface Article {
  coin: number
  end_time: Date
  count: number
}

export interface ArticleListResponse {
  count: number;
  next: string;
  previous: string;
  results: Article[]
}