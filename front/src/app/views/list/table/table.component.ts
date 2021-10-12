import { Component, OnInit } from '@angular/core';
import { ChartDataSets, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { Coin } from '../../../shared/services/coin.model';
import { CoinsService } from '../../../shared/services/coins.service';

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

  // setup
  public lineChartType: ChartType = "line";
  public lineChartData: ChartDataSets[] = [
    { data: [65, 59, 80, 81, 56, 55, 40], label: 'Series A' },
  ];
  public lineChartLabels: Label[] = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
  public lineChartOptions: any = {
    responsive: true,
  };
  public lineChartColors: Color[] = [
    {
      borderColor: 'black',
      backgroundColor: 'rgba(255,0,0,0.3)',
    },
  ];
  public lineChartLegend = true;
  public lineChartPlugins = [];

}
