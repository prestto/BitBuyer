import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Article } from '../../../shared/models/article.model';
import { ArticlesService } from '../../../shared/services/articles.service';


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

  public articles: Article[];
  coinAbbreviation: any;

  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe(params => {
      this.coinAbbreviation = params.get('coinAbbreviation');
      this.articleService.getArticleList(this.coinAbbreviation)
        .subscribe(
          articles => {
            // console.log(articles.results)
            this.articles = articles.results
          },
          error => console.error(error)
        )
    })
  }

}
