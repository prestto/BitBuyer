import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from 'src/app/shared/shared.module';
import { DetailComponent } from './detail.component';
import { ChartsModule } from 'ng2-charts';
import { ArticleAggregatesComponent } from './article-aggregates/article-aggregates.component';


@NgModule({
  declarations: [DetailComponent, ArticleAggregatesComponent],
  imports: [
    CommonModule,
    SharedModule,
    ChartsModule,
  ]
})
export class DetailModule { }
