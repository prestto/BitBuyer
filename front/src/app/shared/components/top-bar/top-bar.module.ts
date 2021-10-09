import { NgModule } from '@angular/core';
import { TopBarComponent } from './top-bar.component';
import { MatToolbarModule } from '@angular/material/toolbar';

@NgModule({
  declarations: [TopBarComponent],
  imports: [MatToolbarModule],
  exports: [TopBarComponent]
})
export class TopBarModule { }
