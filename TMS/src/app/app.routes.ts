import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { AddStudentComponent } from './add-student/add-student.component';
import { AllStudentsComponent } from './all-students/all-students.component';
import { AddTeacherComponent } from './add-teacher/add-teacher.component';
import { AllTeachersComponent } from './all-teachers/all-teachers.component';
import { AddClassComponent } from './add-class/add-class.component';
import { AllClassesComponent } from './all-classes/all-classes.component';
import { StuEnrollComponent } from './stu-enroll/stu-enroll.component';
import { Subject } from 'rxjs';
import { SubjectComponent } from './subject/subject.component';

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

       // class
      { path: 'addsubject', component: SubjectComponent },
      { path: 'addclass', component: AddClassComponent },
      { path: 'allclasses', component: AllClassesComponent},
      { path: 'stu_enroll', component: StuEnrollComponent},





    ]
  }
]; 