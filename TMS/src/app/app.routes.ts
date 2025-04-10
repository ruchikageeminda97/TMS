import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { AddStudentComponent } from './add-student/add-student.component';
import { AllStudentsComponent } from './all-students/all-students.component';

export const routes: Routes = [
  { path: '', component: LoginComponent }, // Default route to login
  { path: 'login', component: LoginComponent }, // Explicit login route
  { 
    path: '', // Empty path for SidebarComponent as layout
    component: SidebarComponent,
    children: [
      { path: 'dashboard', component: DashboardComponent }, // /dashboard
      { path: 'addstudent', component: AddStudentComponent }, // /addstudent
      { path: 'allstudent', component: AllStudentsComponent } // /addstudent

    ]
  }
];