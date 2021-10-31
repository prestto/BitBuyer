import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from 'src/app/shared/shared.module';
import { DetailComponent } from './detail.component';


@NgModule({
  declarations: [DetailComponent],
  imports: [
    CommonModule,
    SharedModule
  ]
})
export class DetailModule { }
