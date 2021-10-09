import { NgModule } from '@angular/core';
import { SharedModule } from 'src/app/shared/shared.module';
import { ListComponent } from './list.component';

@NgModule({
  declarations: [ListComponent],
  imports: [SharedModule]
})
export class ListModule { }
