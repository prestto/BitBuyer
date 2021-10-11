import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
// import { HeaderComponent } from './header/header.component';
import { ListComponent } from './views/list/list.component';


const routes: Routes = [
  {
    path: 'coins',
    component: ListComponent,
  },
  { path: '', redirectTo: 'coins', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
