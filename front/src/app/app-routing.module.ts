import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
// import { HeaderComponent } from './header/header.component';
// import { ListViewComponent } from './list-view/list-view.component';

// import { HeaderComponent } from './list-view/app.component';


const routes: Routes = [
//   {
//     path: 'coins',
//     component: ListViewComponent,
//   },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
