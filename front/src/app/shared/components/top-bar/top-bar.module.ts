import { NgModule } from '@angular/core';
import { TopBarComponent } from './top-bar.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [TopBarComponent],
  imports: [MatToolbarModule, RouterModule],
  exports: [TopBarComponent]
})
export class TopBarModule { }
