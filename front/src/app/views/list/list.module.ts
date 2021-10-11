import { NgModule } from '@angular/core';
import { SharedModule } from 'src/app/shared/shared.module';
import { ListComponent } from './list.component';
import { TableComponent } from './table/table.component';
import { MatTableModule } from '@angular/material/table';

@NgModule({
  declarations: [ListComponent, TableComponent],
  imports: [SharedModule, MatTableModule]
})
export class ListModule { }
