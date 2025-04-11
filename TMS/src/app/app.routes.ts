import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { AddStudentComponent } from './add-student/add-student.component';
import { AllStudentsComponent } from './all-students/all-students.component';
import { AddTeacherComponent } from './add-teacher/add-teacher.component';
import { AllTeachersComponent } from './all-teachers/all-teachers.component';

export const routes: Routes = [
  { path: '', component: LoginComponent }, 
  { path: 'login', component: LoginComponent }, 
  { 
    path: '',
    component: SidebarComponent,
    children: [
      { path: 'dashboard', component: DashboardComponent },

      // student 
      { path: 'addstudent', component: AddStudentComponent },
      { path: 'allstudent', component: AllStudentsComponent },

      // teacher
      { path: 'addteacher', component: AddTeacherComponent },
      { path: 'allteacher', component: AllTeachersComponent },

       // teacher
      //  { path: 'addteacher', component: AddTeacherComponent },
      //  { path: 'allteacher', component: AllTeachersComponent },




    ]
  }
]; 