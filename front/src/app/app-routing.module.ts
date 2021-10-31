import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListComponent } from './views/list/list.component';
import { DetailComponent } from './views/detail/detail.component';


const routes: Routes = [
  { path: 'coins', component: ListComponent },
  { path: 'coins/:coinAbbreviation', component: DetailComponent },
  { path: '', redirectTo: 'coins', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
