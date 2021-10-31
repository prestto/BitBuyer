import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from 'src/app/shared/shared.module';
import { DetailComponent } from './detail.component';
import { ChartsModule } from 'ng2-charts';


@NgModule({
  declarations: [DetailComponent],
  imports: [
    CommonModule,
    SharedModule,
    ChartsModule,
  ]
})
export class DetailModule { }
