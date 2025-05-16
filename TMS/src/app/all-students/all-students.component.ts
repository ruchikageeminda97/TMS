import { Component, OnInit } from '@angular/core';
import { NgFor } from '@angular/common';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Student } from '../models/student.model';
import { LanguageService } from '../language.service';
import { ApiService } from '../api_services/services';

@Component({
  selector: 'app-all-students',
  standalone: true,
  imports: [NgFor, MatSnackBarModule],
  templateUrl: './all-students.component.html',
  styleUrls: ['./all-students.component.css']
})
export class AllStudentsComponent implements OnInit {
  students: Student[] = [];

  constructor(
    public languageService: LanguageService,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.fetchStudents();
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }

  private fetchStudents(): void {
    this.apiService.getStudents().subscribe({
      next: (students) => {
        this.students = students;
      },
      error: (err) => {
        console.error('Error fetching students:', err);
        this.showSnackBar(this.getTranslation('fetch_students_failed'));
      }
    });
  }
}