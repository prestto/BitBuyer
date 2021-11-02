import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ChartDataSets, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { Article } from '../../../shared/models/article.model';
import { ArticlesService } from '../../../shared/services/articles.service';
import { TableChart } from '../../../shared/models/chart.model';
import { formatDate } from '@angular/common';



@Component({
  selector: 'app-article-aggregates',
  templateUrl: './article-aggregates.component.html',
  styleUrls: ['./article-aggregates.component.scss']
})
export class ArticleAggregatesComponent implements OnInit {

  constructor(
    private articleService: ArticlesService,
    private activatedRoute: ActivatedRoute,

  ) { }

  public tableChart: any;
  public articles: Article[];
  coinAbbreviation: any;

  formatCoinHistory(articles: Article[]) {
    // convert coin history to a human readable format
    let labels: any[] = [];
    let points: any[] = [];

    // loop on all data points, converting dates
    for (let article of articles) {
      labels.push(article.end_time)
      points.push(article.count)
    }

    // add to typed object
    let tc: TableChart = {
      data: [{ data: points, label: '' },],
      labels: labels,
      color: [
        {
          borderColor: 'rgb(0, 110, 230,0.3)',
          backgroundColor: 'rgb(0, 110, 230, 0.3)',
        },
      ]
    }
    return tc
  }

  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe(params => {
      this.coinAbbreviation = params.get('coinAbbreviation');
      this.articleService.getArticleList(this.coinAbbreviation)
        .subscribe(
          articles => {
            // console.log(articles.results)
            this.articles = articles.results
            this.tableChart = this.formatCoinHistory(this.articles)
          },
          error => console.error(error)
        )
    })
  }


  // chart
  public labels: any[] = [];
  public lineChartType: ChartType = "line";
  public lineChartData: ChartDataSets[] = [{ data: [] },];
  public lineChartLabels: Label[] = this.labels;
  public lineChartLegend = true;
  public lineChartPlugins = [];

  public lineChartOptions: any = {
    responsive: true,
    maintainAspectRatio: false,
    legend: {
      display: false
    },
    tooltips: {
      enabled: true,
      position: "nearest",
      intersect: false,
      callbacks: {
        title: function (tooltipItem: any, data: any) {
          const dt = tooltipItem[0].xLabel
          return formatDate(dt, 'MMM-d H:M:S', 'en-us')
        },
      }
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
        type: 'time',
        time: {
          unit: 'day',
          unitStepSize: 1,
          displayFormats: {
            'millisecond': 'MMM DD',
            'second': 'MMM DD',
            'minute': 'MMM DD',
            'hour': 'MMM DD',
            'day': 'MMM DD',
            'week': 'MMM DD',
            'month': 'MMM DD',
            'quarter': 'MMM DD',
            'year': 'MMM DD',
          }
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
          display: false
        }
      }]
    },
    elements: {
      line: {
        fill: true
      }
    }
  };

}
