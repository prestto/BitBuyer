import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ChartDataSets, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { CoinsService } from '../../shared/services/coins.service';
import { formatCoinHistory } from '../../shared/utils/currency';


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

  cleanDescription(description: string) {
    // remove commas between p tags
    let re = new RegExp('</p>, <p>', 'g');
    return description.replace(re, '</p> <p>')
  }

  constructor(
    private activatedRoute: ActivatedRoute,
    private coinService: CoinsService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe(params => {
      this.coinAbbreviation = params.get('coinAbbreviation');
      this.coin = this.coinService.getCoinDetail(this.coinAbbreviation)
        .subscribe(
          coin => {
            coin.description = this.cleanDescription(coin.description)
            this.tableChart = formatCoinHistory(coin)
            this.coin = coin
          },
          error => {
            console.error(error)
            this.router.navigate(['coins'])
          }
        )
    })
  }

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
      enabled: true,
      position: "nearest",
      intersect: false

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
