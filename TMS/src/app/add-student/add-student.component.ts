import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { LanguageService } from '../language.service';
import { ApiService } from '../api_services/services';
import { Student } from '../models/student.model';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

@Component({
  selector: 'app-add-student',
  standalone: true,
  imports: [FormsModule, CommonModule, MatSnackBarModule],
  templateUrl: './add-student.component.html',
  styleUrls: ['./add-student.component.css'],
})
export class AddStudentComponent {
  student: Student = {
    student_id: '',
    first_name: '',
    last_name: '',
    date_of_birth: '',
    gender: '',
    contact_number: '',
    email: '',
    address: '',
    enrollment_date: '',
    status: 'Active',
  };

  selectedFile: File | null = null;
  isDragging = false;
  isImportModalOpen = false;

  constructor(
    public languageService: LanguageService,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }

  openImportModal() {
    this.isImportModalOpen = true;
  }

  closeImportModal() {
    this.isImportModalOpen = false;
    this.selectedFile = null;
    this.isDragging = false;
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
    const files = event.dataTransfer?.files;
    if (files && files.length > 0 && files[0].type === 'text/csv') {
      this.selectedFile = files[0];
    } else {
      alert(this.getTranslation('invalid_csv_file'));
    }
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
  }

  importCsv() {
    if (this.selectedFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        const students = this.parseCsv(text);
        if (students.length > 0) {
          this.apiService.importStudents(students).subscribe({
            next: (response) => {
              this.showSnackBar(this.getTranslation('csv_import_success'));
              this.closeImportModal();
            },
            error: (err) => {
              console.error('Error importing students:', err);
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

  private parseCsv(data: string): Student[] {
    const students: Student[] = [];
    const rows = data.split('\n').slice(1);
    rows.forEach((row) => {
      const [
        student_id,
        first_name,
        last_name,
        date_of_birth,
        gender,
        contact_number,
        email,
        address,
        enrollment_date,
      ] = row.split(',').map((item) => item.trim());
      if (first_name && last_name) {
        students.push({
          student_id,
          first_name,
          last_name,
          date_of_birth,
          gender,
          contact_number,
          email,
          address,
          enrollment_date,
          status: 'Active',
        });
      }
    });
    return students;
  }

  onSubmit() {
    if (this.isFormValid()) {
      this.apiService.addStudent(this.student).subscribe({
        next: (response) => {
          this.showSnackBar(this.getTranslation('student_added_success'));
          this.resetForm();
        },
        error: (err) => {
          console.error('Error adding student:', err);
          this.showSnackBar(this.getTranslation('student_add_failed'));
        }
      });
    } else {
      this.showSnackBar(this.getTranslation('student_add_failed'));
    }
  }

  isFormValid(): boolean {
    return Object.values(this.student).every(
      (value) => value !== '' && value !== null
    );
  }

  resetForm() {
    this.student = {
      student_id: '',
      first_name: '',
      last_name: '',
      date_of_birth: '',
      gender: '',
      contact_number: '',
      email: '',
      address: '',
      enrollment_date: '',
      status: 'Active',
    };
  }
}