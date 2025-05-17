import { Component, ViewChild } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { NgClass, NgIf } from '@angular/common';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Teacher } from '../models/teacher.model';
import { LanguageService } from '../language.service';
import { TeacherLanguageService } from '../languages/teacher.language';
import { ApiService } from '../api_services/services';

@Component({
  selector: 'app-add-teacher',
  standalone: true,
  imports: [FormsModule, NgClass, NgIf, MatSnackBarModule],
  templateUrl: './add-teacher.component.html',
  styleUrls: ['./add-teacher.component.css']
})
export class AddTeacherComponent {
  @ViewChild('teacherForm') teacherForm!: NgForm;

  teacher: Teacher = {
    teacher_id: '',
    first_name: '',
    last_name: '',
    contact_number: '',
    email: '',
    address: '',
    hire_date: '',
    specialization: '',
    status: 'Active'
  };

  isImportModalOpen = false;
  isDragging = false;
  selectedFile: File | null = null;

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

  getTranslation(key: string): string {
    return this.teacherLanguageService.getTranslation(key);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }

  onSubmit(): void {
    if (this.teacherForm.valid) {
      this.apiService.addTeacher(this.teacher).subscribe({
        next: (response) => {
          this.showSnackBar(this.getTranslation('teacher_added_success'));
          this.teacherForm.resetForm();
          this.teacher = {
            teacher_id: '',
            first_name: '',
            last_name: '',
            contact_number: '',
            email: '',
            address: '',
            hire_date: '',
            specialization: '',
            status: 'Active'
          };
        },
        error: (err) => {
          console.error('Error adding teacher:', err);
          this.showSnackBar(this.getTranslation('teacher_add_failed'));
        }
      });
    } else {
      this.showSnackBar(this.getTranslation('teacher_add_failed'));
    }
  }

  openImportModal(): void {
    this.isImportModalOpen = true;
  }

  closeImportModal(): void {
    this.isImportModalOpen = false;
    this.selectedFile = null;
    this.isDragging = false;
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
    const files = event.dataTransfer?.files;
    if (files && files.length > 0 && files[0].type === 'text/csv') {
      this.selectedFile = files[0];
    } else {
      this.showSnackBar(this.getTranslation('invalid_csv_file'));
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
  }

  importCsv(): void {
    if (this.selectedFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        const teachers = this.parseCsv(text);
        if (teachers.length > 0) {
          this.apiService.importTeachers(teachers).subscribe({
            next: (response) => {
              this.showSnackBar(this.getTranslation('csv_import_success'));
              this.closeImportModal();
            },
            error: (err) => {
              console.error('Error importing teachers:', err);
              this.showSnackBar(this.getTranslation('csv_import_failed'));
            }
          });
        } else {
          this.showSnackBar(this.getTranslation('csv_import_failed'));
        }
      };
      reader.readAsText(this.selectedFile);
    }
  }

  private parseCsv(data: string): Teacher[] {
    const teachers: Teacher[] = [];
    const rows = data.split('\n').slice(1); // Skip header
    rows.forEach((row) => {
      const [
        teacher_id,
        first_name,
        last_name,
        contact_number,
        email,
        address,
        hire_date,
        specialization,
        status
      ] = row.split(',').map((item) => item.trim());
      if (first_name && last_name) {
        teachers.push({
          teacher_id: teacher_id || '',
          first_name,
          last_name,
          contact_number: contact_number || '',
          email: email || '',
          address: address || '',
          hire_date: hire_date || '',
          specialization: specialization || '',
          status: status || 'Active'
        });
      }
    });
    return teachers;
  }
}