import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TopBarModule } from './components/top-bar/top-bar.module';
import { MatToolbarModule } from '@angular/material/toolbar';
import { TopBarComponent } from './components/top-bar/top-bar.component';

@NgModule({
  declarations: [],
  imports: [CommonModule, MatToolbarModule, TopBarModule],
  exports: [TopBarComponent]
})
export class SharedModule { }
