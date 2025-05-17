import { Component, OnInit } from '@angular/core';
import { CommonModule, NgFor } from '@angular/common';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Teacher } from '../models/teacher.model';
import { LanguageService } from '../language.service';
import { TeacherLanguageService } from '../languages/teacher.language';
import { ApiService } from '../api_services/services';

@Component({
  selector: 'app-all-teachers',
  standalone: true,
  imports: [CommonModule, NgFor, MatSnackBarModule],
  templateUrl: './all-teachers.component.html',
  styleUrls: ['./all-teachers.component.css']
})
export class AllTeachersComponent implements OnInit {
  teachers: Teacher[] = [];

  constructor(
    public languageService: LanguageService,
    public teacherLanguageService: TeacherLanguageService,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {
    this.languageService.language$.subscribe(language => {
      this.teacherLanguageService.setLanguage(language);
    });
  }

  ngOnInit(): void {
    this.fetchTeachers();
  }

  getTranslation(key: string): string {
    return this.teacherLanguageService.getTranslation(key);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }

  private fetchTeachers(): void {
    this.apiService.getTeachers().subscribe({
      next: (teachers) => {
        this.teachers = teachers;
      },
      error: (err) => {
        console.error('Error fetching teachers:', err);
        this.showSnackBar(this.getTranslation('fetch_teachers_failed'));
      }
    });
  }

  editTeacher(teacher: Teacher): void {
    // For simplicity, update locally and send to API
    const updatedTeacher = { ...teacher }; // Shallow copy to avoid direct mutation
    this.apiService.updateTeacher(updatedTeacher).subscribe({
      next: (response) => {
        const index = this.teachers.findIndex(t => t.teacher_id === updatedTeacher.teacher_id);
        if (index !== -1) {
          this.teachers[index] = response || updatedTeacher; // Use API response if provided
        }
        this.showSnackBar(this.getTranslation('teacher_updated_success'));
      },
      error: (err) => {
        console.error('Error updating teacher:', err);
        this.showSnackBar(this.getTranslation('teacher_update_failed'));
      }
    });
  }

  deleteTeacher(teacher_id: string): void {
    if (confirm(this.getTranslation('confirm_delete'))) {
      this.apiService.deleteTeacher(teacher_id).subscribe({
        next: () => {
          this.teachers = this.teachers.filter(t => t.teacher_id !== teacher_id);
          this.showSnackBar(this.getTranslation('teacher_deleted_success'));
        },
        error: (err) => {
          console.error('Error deleting teacher:', err);
          this.showSnackBar(this.getTranslation('teacher_delete_failed'));
        }
      });
    }
  }
}