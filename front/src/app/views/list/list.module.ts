import { NgModule } from '@angular/core';
import { SharedModule } from 'src/app/shared/shared.module';
import { ListComponent } from './list.component';
import { TableComponent } from './table/table.component';
import { MatTableModule } from '@angular/material/table';
import { ChartsModule } from 'ng2-charts';
@NgModule({
  declarations: [ListComponent, TableComponent],
  imports: [SharedModule, MatTableModule, ChartsModule]
})
export class ListModule { }
