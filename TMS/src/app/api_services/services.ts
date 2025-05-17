import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { Student } from '../models/student.model';
import { Teacher } from '../models/teacher.model';
import { Class } from '../models/class.model';

export interface StatsCounts {
  students: number;
  teachers: number;
  subjects: number;
  classes: number;
  enrollments: number;
  teacher_assignments: number;
  payments: number;
  attendance: number;
  grades: number;
}

export interface Subject {
  subject_id: string;
  subject_name: string;
  description: string;
  level: string;
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl: string = 'http://127.0.0.1:8001';

  constructor(private http: HttpClient) {}

  private getUsername(): string {
    return localStorage.getItem('username') || '';
  }

  login(credentials: { username: string; password: string }): Observable<any> {
    const credentialsJson = JSON.stringify(credentials);
    return this.http
      .post(`${this.baseUrl}/login/`, credentialsJson, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          return throwError(() => new Error('Failed to login'));
        })
      );
  }

  register(user: { username: string; password: string; role: string; email: string }): Observable<any> {
    const userJson = JSON.stringify(user);
    return this.http
      .post(`${this.baseUrl}/register/`, userJson, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          console.error('Error registering user:', error);
          return throwError(() => new Error('Failed to register'));
        })
      );
  }

  addStudent(student: Student): Observable<any> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    const studentJson = JSON.stringify(student);
    return this.http
      .post(`${this.baseUrl}/students/?username=${encodeURIComponent(username)}`, studentJson, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          return throwError(() => new Error('Failed to add student'));
        })
      );
  }

  importStudents(students: Student[]): Observable<any> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    const studentsJson = JSON.stringify(students);
    return this.http
      .post(`${this.baseUrl}/students/import/?username=${encodeURIComponent(username)}`, studentsJson, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          return throwError(() => new Error('Failed to import students'));
        })
      );
  }

  getStudents(): Observable<Student[]> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    return this.http
      .get<Student[]>(`${this.baseUrl}/students/?username=${encodeURIComponent(username)}`, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          return throwError(() => new Error('Failed to fetch students'));
        })
      );
  }

  addTeacher(teacher: Teacher): Observable<any> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    const teacherJson = JSON.stringify(teacher);
    return this.http
      .post(`${this.baseUrl}/teachers/?username=${encodeURIComponent(username)}`, teacherJson, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          console.error('Error adding teacher:', error);
          return throwError(() => new Error('Failed to add teacher'));
        })
      );
  }

  importTeachers(teachers: Teacher[]): Observable<any> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    const teachersJson = JSON.stringify(teachers);
    return this.http
      .post(`${this.baseUrl}/teachers/import/?username=${encodeURIComponent(username)}`, teachersJson, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          console.error('Error importing teachers:', error);
          return throwError(() => new Error('Failed to import teachers'));
        })
      );
  }

  getTeachers(): Observable<Teacher[]> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    return this.http
      .get<Teacher[]>(`${this.baseUrl}/teachers/?username=${encodeURIComponent(username)}`, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          console.error('Error fetching teachers:', error);
          return throwError(() => new Error('Failed to fetch teachers'));
        })
      );
  }

  updateTeacher(teacher: Teacher): Observable<any> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    const teacherJson = JSON.stringify(teacher);
    return this.http
      .put(`${this.baseUrl}/teachers/${encodeURIComponent(teacher.teacher_id)}/?username=${encodeURIComponent(username)}`, teacherJson, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          console.error('Error updating teacher:', error);
          return throwError(() => new Error('Failed to update teacher'));
        })
      );
  }

  deleteTeacher(teacher_id: string): Observable<any> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    return this.http
      .delete(`${this.baseUrl}/teachers/${encodeURIComponent(teacher_id)}/?username=${encodeURIComponent(username)}`, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          console.error('Error deleting teacher:', error);
          return throwError(() => new Error('Failed to delete teacher'));
        })
      );
  }

  getStatsCounts(): Observable<StatsCounts> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    return this.http
      .get<StatsCounts>(`${this.baseUrl}/stats/counts?username=${encodeURIComponent(username)}`, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          console.error('Error fetching stats counts:', error);
          return throwError(() => new Error('Failed to fetch stats counts'));
        })
      );
  }

  addSubject(subject: Subject): Observable<any> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    const subjectJson = JSON.stringify(subject);
    return this.http
      .post(`${this.baseUrl}/subjects/?username=${encodeURIComponent(username)}`, subjectJson, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          console.error('Error adding subject:', error);
          return throwError(() => new Error('Failed to add subject'));
        })
      );
  }

  // getSubjects(): Observable<Subject[]> {
  //   const username = this.getUsername();
  //   if (!username) {
  //     return throwError(() => new Error('Username not found in local storage'));
  //   }
  //   return this.http
  //     .get<Subject[]>(`${this.baseUrl}/subjects/?username=${encodeURIComponent(username)}`, {
  //       headers: new HttpHeaders({
  //         'Content-Type': 'application/json',
  //       }),
  //     })
  //     .pipe(
  //       catchError((error) => {
  //         console.error('Error fetching subjects:', error);
  //         return throwError(() => new Error('Failed to fetch subjects'));
  //       })
  //     );
  // }

  addClass(classData: Class): Observable<any> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    const classJson = JSON.stringify(classData);
    return this.http
      .post(`${this.baseUrl}/classes/?username=${encodeURIComponent(username)}`, classJson, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          console.error('Error adding class:', error);
          return throwError(() => new Error('Failed to add class'));
        })
      );
  }
    getSubjects(): Observable<any> {
    const username = this.getUsername();
    if (!username) {
      return throwError(() => new Error('Username not found in local storage'));
    }
    return this.http
      .get<any>(`${this.baseUrl}/subjects/?username=${encodeURIComponent(username)}`, {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
      })
      .pipe(
        catchError((error) => {
          return throwError(() => new Error('Failed to fetch stats counts'));
        })
      );
  }

  getClasses(): Observable<Class[]> {
    const username = localStorage.getItem('username');
    if (!username) {
      throw new Error('Username not found in local storage');
    }
    return this.http.get<Class[]>(`${this.baseUrl}/classes/?username=${username}`);
  }

  // getTodayClasses
  getTodayClasses(): Observable<{ today_classes: any[], date: string }> {
    const day = localStorage.getItem('day');
    if (!day) {
      throw new Error('Day not found in local storage');
    }
    return this.http.get<{ today_classes: any[], date: string }>(`${this.baseUrl}/stats/today-classes?day=${day}`);
  }
}

 
