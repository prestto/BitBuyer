import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CoinsService } from '../../shared/services/coins.service';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss']
})
export class DetailComponent implements OnInit {
  coinAbbreviation: any
  coin: any
  error: any

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
            this.coin = coin
          },
          error => {
            console.error(error)
            this.router.navigate(['coins'])
          }
        )

    })
  }

  ngOnInit(): void {
  }
}
