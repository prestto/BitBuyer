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

  constructor(
    private activatedRoute: ActivatedRoute,
    private coinService: CoinsService,
    private router: Router
  ) {
    this.activatedRoute.paramMap.subscribe(params => {
      console.log(params)
      this.coinAbbreviation = params.get('abbreviation');
      this.coin = this.coinService.getCoinDetail(this.coinAbbreviation)
        .subscribe(
          coin => this.coin = coin,
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
