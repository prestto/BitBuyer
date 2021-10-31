import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TopBarModule } from './components/top-bar/top-bar.module';
import { MatToolbarModule } from '@angular/material/toolbar';
import { TopBarComponent } from './components/top-bar/top-bar.component';
import { CurrencyDirective } from './directives/currency';

@NgModule({
  declarations: [CurrencyDirective],
  imports: [CommonModule, MatToolbarModule, TopBarModule],
  exports: [TopBarComponent, CurrencyDirective]
})
export class SharedModule { }
