import { Component, OnInit } from '@angular/core';
import { CoinsService } from '../../../shared/services/coins.service';
import { Coin } from '../../../shared/services/coin.model';

let coinsDataSource: Coin[] = [];

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  providers: [CoinsService]
})
export class TableComponent implements OnInit {
  displayedColumns = ['id', 'icon', 'name']
  coinsDataSource = coinsDataSource

  constructor(
    private service: CoinsService
  ) { }

  ngOnInit(): void {
    this.service.getCoins()
      .subscribe(
        coinResponse => {
          this.coinsDataSource = coinResponse.results
        }
      )
  }

  getCoins() {
    console.log('click')

  }
}
