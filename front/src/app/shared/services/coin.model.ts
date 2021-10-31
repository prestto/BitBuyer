import { DeclarationListEmitMode } from "@angular/compiler";

export interface PricePoint {
  time_close: Date;
  rate_close: Date;
  coin_id: number;
}

export interface Coin {
  id: number;
  name: string;
  abbreviation: string;
  icon: string;
  description: string;
  coinprices_set: PricePoint[];
  currentprices: CurrentPrices;
}

export interface CurrentPrices {
  coin_id: number
  rate_close: number
  rate_open: number
  time_period_end: Date
}

export interface CoinResponse {
  count: number;
  next: string;
  previous: string;
  results: Coin[];
}

export interface CoinDetail {
  id: number;
  name: string;
  abbreviation: string;
  description: string;
  coinprices_set: PricePoint[];
}

export interface FormattedCurrentPrice {
  change: string;
  current: string;
  date: Date;
}
