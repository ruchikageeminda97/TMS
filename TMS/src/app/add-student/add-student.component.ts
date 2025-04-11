import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { LanguageService } from '../language.service'; 
import { Student } from '../models/student.model';


@Component({
  selector: 'app-add-student',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './add-student.component.html',
  styleUrls: ['./add-student.component.css'],
})
export class AddStudentComponent {
  student: Student = {
    StudentID:'',
    firstName: '',
    lastName: '',
    dateOfBirth: '',
    gender: '',
    contactNumber: '',
    email: '',
    address: '',
    enrollmentDate: '',
  };

  selectedFile: File | null = null;
  isDragging = false;
  isImportModalOpen = false;

  constructor(public languageService: LanguageService) {
    console.log('LanguageService in AddStudent:', this.languageService); 
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
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
        console.log('Imported Students:', students);
        // TODO: Send students to backend API
        alert(this.getTranslation('csv_import_success')); 
        this.closeImportModal();
      };
      reader.readAsText(this.selectedFile);
    }
  }

  private parseCsv(data: string): Student[] {
    const students: Student[] = [];
    const rows = data.split('\n').slice(1); 
    rows.forEach((row) => {
      const [
        StudentID,
        firstName,
        lastName,
        dateOfBirth,
        gender,
        contactNumber,
        email,
        address,
        enrollmentDate,
      ] = row.split(',').map((item) => item.trim());
      if (firstName && lastName) {
        students.push({
          StudentID,
          firstName,
          lastName,
          dateOfBirth,
          gender,
          contactNumber,
          email,
          address,
          enrollmentDate,
        });
      }
    });
    return students;
  }

  onSubmit() {
    if (this.isFormValid()) {
      console.log('Student Data:', this.student);
      alert(this.getTranslation('student_added_success')); 
      this.resetForm();
    }
  }

  isFormValid(): boolean {
    return Object.values(this.student).every(
      (value) => value !== '' && value !== null
    );
  }

  resetForm() {
    this.student = {
      StudentID:'',
      firstName: '',
      lastName: '',
      dateOfBirth: '',
      gender: '',
      contactNumber: '',
      email: '',
      address: '',
      enrollmentDate: '',
    };
  }
}