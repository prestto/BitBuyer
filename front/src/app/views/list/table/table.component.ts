import { Component, OnInit } from '@angular/core';
import { ChartDataSets, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { Coin, FormattedCurrentPrice } from '../../../shared/models/coin.model';
import { CoinsService } from '../../../shared/services/coins.service';
import { formatCoinHistory, formatCurrentPrice } from '../../../shared/utils/currency';

let coinsDataSource: Coin[] = [];

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  providers: [CoinsService]
})
export class TableComponent implements OnInit {
  displayedColumns = ['id', 'icon', 'name', 'close', 'change', 'graph']
  coinsDataSource = coinsDataSource;
  labels: any[] = [];
  points: any[] = [];
  testObj: any;
  public allCharts: any = {};
  public currentPrices: any = {};
  public isLoading = true;

  constructor(
    private service: CoinsService
  ) {
    this.labels = []
  }

  ngOnInit(): void {
    // get coin info
    this.service.getCoins()
      .subscribe(
        coinResponse => {

          for (let coin of coinResponse.results) {

            // get the chart params in an accesible format
            let tableChart = formatCoinHistory(coin)
            this.allCharts[coin.abbreviation] = tableChart

            // price change
            if (coin.currentprices) {
              let currentPrice: FormattedCurrentPrice = formatCurrentPrice(coin.currentprices)
              this.currentPrices[coin.abbreviation] = currentPrice
            }
          }
          this.isLoading = false
          this.coinsDataSource = coinResponse.results
        },
        error => {
          this.isLoading = false
        }
      )
  }

  // setup
  public lineChartType: ChartType = "line";
  public lineChartData: ChartDataSets[] = [{ data: [] },];
  public lineChartLabels: Label[] = this.labels;
  public lineChartOptions: any = {
    responsive: true,
    maintainAspectRatio: false,
    legend: {
      display: false
    },
    tooltips: {
      enabled: false
      // position: "nearest"
    },
    scales: {
      y: {
        type: 'linear',
        grace: '10%'
      },
      x: {
        type: 'timeseries',
      },
      xAxes: [{
        ticks: {
          display: false //this will remove only the label
        },
        gridLines: {
          display: false
        }
      }],
      yAxes: [{
        ticks: {
          display: false //this will remove only the label
        },
        gridLines: {
          display: false
        }
      }]
    },
    elements: {
      line: {
        fill: false
      }
    }
  };
  public lineChartColors: Color[] = [
    {
      borderColor: 'rgba(255,0,0,0.3)',
      backgroundColor: 'rgba(255,0,0,0.3)',
    },
  ];
  public lineChartLegend = true;
  public lineChartPlugins = [];

}
