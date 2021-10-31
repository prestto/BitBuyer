import { Directive, ElementRef } from '@angular/core';
import { CurrencyPipe } from '@angular/common';

@Directive({ selector: '[currencyX]' })
export class CurrencyDirective {
  constructor(el: ElementRef) {

  }
}
