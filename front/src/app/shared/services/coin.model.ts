import { DeclarationListEmitMode } from "@angular/compiler";

export interface PricePoint {
  time_open: Date;
  rate_open: Date;
  coin_id: number;
}

export interface Coin {
  id: number;
  name: string;
  abbreviation: string;
  icon: string;
  description: string;
  price_history: PricePoint[];
}

export interface CoinResponse {
  count: number;
  next: string;
  previous: string;
  results: Coin[];
}
