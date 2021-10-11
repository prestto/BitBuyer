export interface Coin {
  id: number;
  name: string;
  abbreviation: string;
  icon: string;
  description: string;
}

export interface CoinResponse {
  count: number;
  next: string;
  previous: string;
  results: Coin[];
}
