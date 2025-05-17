import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { Student } from '../models/student.model';
import { Teacher } from '../models/teacher.model';

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
}