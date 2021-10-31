import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CoinsService } from '../../shared/services/coins.service';
import { ChartDataSets, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { CoinDetail, FormattedCurrentPrice, CurrentPrices } from '../../shared/services/coin.model';
import { formatDate } from '@angular/common';


export interface TableChart {
  // TODO dedupe
  data: ChartDataSets[];
  labels: Label[];
  color: Color[];
}
@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss']
})
export class DetailComponent implements OnInit {
  coinAbbreviation: any
  error: any
  public chart: any = {};
  public coin: any;
  public tableChart: any;

  getColor(points: number[]) {
    // TODO dedupe
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

  cleanDescription(description: string) {
    // remove commas between p tags
    let re = new RegExp('</p>, <p>', 'g');
    return description.replace(re, '</p> <p>')
  }

  constructor(
    private activatedRoute: ActivatedRoute,
    private coinService: CoinsService,
    private router: Router
  ) {
    this.activatedRoute.paramMap.subscribe(params => {
      this.coinAbbreviation = params.get('coinAbbreviation');
      this.coin = this.coinService.getCoinDetail(this.coinAbbreviation)
        .subscribe(
          coin => {
            coin.description = this.cleanDescription(coin.description)
            this.tableChart = this.formatCoinHostory(coin)
            this.coin = coin
          },
          error => {
            console.error(error)
            this.router.navigate(['coins'])
          }
        )
    })
  }

  formatCoinHostory(coin: CoinDetail) {
    // convert coin history to a human readable format
    let labels: any[] = [];
    let points: any[] = [];

    // loop on all data points, converting dates
    for (let pricePoint of coin.coinprices_set) {
      labels.push(formatDate(pricePoint.time_close, 'Y-M-d', 'en-us'))
      points.push(pricePoint.rate_close)
    }

    // get color red (fall) or green (rise) from price 
    let color: Color[] = this.getColor(points)

    // add to typed object
    let tc: TableChart = {
      data: [{ data: points, label: 'Price ($)' },],
      labels: labels,
      color: color
    }
    return tc
  }

  ngOnInit(): void { }

  // chart
  labels: any[] = [];
  public lineChartType: ChartType = "line";
  public lineChartData: ChartDataSets[] = [{ data: [] },];
  public lineChartLabels: Label[] = this.labels;
  public lineChartLegend = true;
  public lineChartPlugins = [];
  public lineChartColors: Color[] = [
    {
      borderColor: 'rgba(255,0,0,0.3)',
      backgroundColor: 'rgba(255,0,0,0.3)',
    },
  ];

  public lineChartOptions: any = {
    responsive: true,
    maintainAspectRatio: false,
    legend: {
      display: false
    },
    tooltips: {
      enabled: true
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
          display: true //this will remove only the label
        },
        gridLines: {
          display: false
        }
      }],
      yAxes: [{
        ticks: {
          display: true //this will remove only the label
        },
        gridLines: {
          display: true
        }
      }]
    },
    elements: {
      line: {
        fill: true
      }
    }
  };
};
