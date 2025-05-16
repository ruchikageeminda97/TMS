import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { Student } from '../models/student.model';

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
          console.error('Error logging in:', error);
          return throwError(() => new Error('Failed to login'));
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
          console.error('Error adding student:', error);
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
          console.error('Error importing students:', error);
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
          console.error('Error fetching students:', error);
          return throwError(() => new Error('Failed to fetch students'));
        })
      );
  }
}