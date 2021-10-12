import { Component, OnInit } from '@angular/core';
import { ChartDataSets, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { Coin, PricePoint } from '../../../shared/services/coin.model';
import { CoinsService } from '../../../shared/services/coins.service';
import { formatDate } from '@angular/common';

let coinsDataSource: Coin[] = [];

export interface TableChart {
  data: ChartDataSets[];
  labels: Label[];
}

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  providers: [CoinsService]
})
export class TableComponent implements OnInit {
  displayedColumns = ['id', 'icon', 'name', 'graph']
  coinsDataSource = coinsDataSource;
  labels: any[] = [];
  points: any[] = [];
  testObj: any;
  public allCharts: any = {}
  constructor(
    private service: CoinsService
  ) {
    this.labels = []
  }

  formatCoinHostory(coin: Coin) {
    // convert coin history to a human readable format
    let labels: any[] = [];
    let points: any[] = [];

    // loop on all data points, converting dates
    for (let pricePoint of coin.coinprices_set) {
      labels.push(formatDate(pricePoint.time_open, 'Y-m-d', 'en-us'))
      points.push(pricePoint.rate_open)
    }

    // add to typed object
    let tc: TableChart = {
      data: [{ data: points, label: 'Series A' },],
      labels: labels
    }
    return tc
  }

  ngOnInit(): void {
    this.service.getCoins()
      .subscribe(
        coinResponse => {

          for (let coin of coinResponse.results) {
            // get the chart params in an accesible format
            let tableChart = this.formatCoinHostory(coin)
            this.allCharts[coin.abbreviation] = tableChart
          }
          this.coinsDataSource = coinResponse.results
          // this.coinsDataSource = coinResponse.results.filter(x => x.abbreviation === 'BTC')
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
