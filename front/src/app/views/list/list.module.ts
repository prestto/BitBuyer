import { NgModule } from '@angular/core';
import { SharedModule } from 'src/app/shared/shared.module';
import { ListComponent } from './list.component';
import { TableComponent } from './table/table.component';
import { MatTableModule } from '@angular/material/table';
import { ChartsModule } from 'ng2-charts';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';


@NgModule({
  imports: [SharedModule, MatTableModule, ChartsModule, CommonModule, RouterModule],
  declarations: [ListComponent, TableComponent],
})
export class ListModule { }
