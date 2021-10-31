import { Component, OnInit } from '@angular/core';
import { ChartDataSets, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { Coin, CurrentPrices } from '../../../shared/services/coin.model';
import { CoinsService } from '../../../shared/services/coins.service';
import { formatDate } from '@angular/common';

let coinsDataSource: Coin[] = [];

export interface TableChart {
  data: ChartDataSets[];
  labels: Label[];
  color: Color[];
}

export interface FormattedCurrentPrice {
  change: string;
  current: string;
  date: Date;
}

function toFixed(x: any) {
  // Shamelessly stolen from here:
  // https://stackoverflow.com/questions/1685680/how-to-avoid-scientific-notation-for-large-numbers-in-javascript
  if (Math.abs(x) < 1.0) {
    var e = parseInt(x.toString().split('e-')[1]);
    if (e) {
      x *= Math.pow(10, e - 1);
      x = '0.' + (new Array(e)).join('0') + x.toString().substring(2);
    }
  } else {
    var e = parseInt(x.toString().split('+')[1]);
    if (e > 20) {
      e -= 20;
      x /= Math.pow(10, e);
      x += (new Array(e + 1)).join('0');
    }
  }
  return x;
}

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

  constructor(
    private service: CoinsService
  ) {
    this.labels = []
  }
  getColor(points: number[]) {
    // get color red (fall) or green (rise) from price 
    let color: Color[];
    if (points[0] > points[points.length - 1]) {
      // red, as prices decreased
      color = [
        {
          borderColor: 'rgba(255,0,0,0.3)',
          backgroundColor: 'rgba(255,0,0,0.3)',
        },
      ]
    }
    else {
      // green, as prices increased
      color = [
        {
          borderColor: 'rgba(0,255,0,0.3)',
          backgroundColor: 'rgba(0,255,0,0.3)',
        },
      ]
    }
    return color
  }

  formatCoinHostory(coin: Coin) {
    // convert coin history to a human readable format
    let labels: any[] = [];
    let points: any[] = [];

    // loop on all data points, converting dates
    for (let pricePoint of coin.coinprices_set) {
      labels.push(formatDate(pricePoint.time_close, 'Y-m-d', 'en-us'))
      points.push(pricePoint.rate_close)
    }

    // get color red (fall) or green (rise) from price 
    let color: Color[] = this.getColor(points)

    // add to typed object
    let tc: TableChart = {
      data: [{ data: points, label: 'Series A' },],
      labels: labels,
      color: color
    }
    return tc
  }

  roundToString(num: number, dp: number) {
    let multiple: number = dp * 10
    let rounded: number = Math.round(num * multiple) / multiple
    // necessary to avoid JS exponential number representations
    // yikes
    if (rounded == 0 && num < 0.001 && num > 0) {
      return toFixed(num)
    }
    else if (rounded == 0) {
      return num.toPrecision(dp)
    }
    else {
      return rounded.toString()
    }
  }

  formatCurrentPrice(currentPrice: CurrentPrices) {
    let percentageChange = 100 - (currentPrice.rate_open / currentPrice.rate_close) * 100
    let change = this.roundToString(percentageChange, 2)

    let fcp: FormattedCurrentPrice = {
      change: `${change}%`,
      current: this.roundToString(currentPrice.rate_close, 2),
      date: currentPrice.time_period_end
    }
    return fcp
  };

  ngOnInit(): void {
    // get coin info
    this.service.getCoins()
      .subscribe(
        coinResponse => {

          for (let coin of coinResponse.results) {

            // get the chart params in an accesible format
            let tableChart = this.formatCoinHostory(coin)
            this.allCharts[coin.abbreviation] = tableChart

            // price change
            if (coin.currentprices) {
              let currentPrice: FormattedCurrentPrice = this.formatCurrentPrice(coin.currentprices)
              this.currentPrices[coin.abbreviation] = currentPrice
            }
          }
          this.coinsDataSource = coinResponse.results
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
