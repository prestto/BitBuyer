import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ListModule } from './list/list.module';
import { DetailModule } from './detail/detail.module';


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    ListModule,
    DetailModule
  ]
})
export class ViewsModule { }
