import { Component, ViewChild } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { Teacher } from '../models/teacher.model';
import { LanguageService } from '../language.service';
import { TeacherLanguageService } from '../languages/teacher.language';
import { NgClass, NgIf } from '@angular/common';

@Component({
  selector: 'app-add-teacher',
  standalone: true,
  imports: [FormsModule,NgClass,NgIf],
  templateUrl: './add-teacher.component.html',
  styleUrls: ['./add-teacher.component.css']
})
export class AddTeacherComponent {
  @ViewChild('teacherForm') teacherForm!: NgForm;

  // Static array to store teachers
  private teachers: Teacher[] = [];

  teacher: Teacher = {
    teacherID: '', // API would generate this; keeping it empty for now
    firstName: '',
    lastName: '',
    gender: '',
    contactNumber: '',
    address: '',
    subject: '',
    educationLevel: ''
  };

  isImportModalOpen = false;
  isDragging = false;
  selectedFile: File | null = null;

  constructor(
    public languageService: LanguageService,
    public teacherLanguageService: TeacherLanguageService
  ) {
    // Sync language with sidebar toggle
    this.languageService.language$.subscribe(language => {
      this.teacherLanguageService.setLanguage(language);
    });
  }

  onSubmit(): void {
    if (this.teacherForm.valid) {
      // Add teacher to static array
      this.teachers.push({ ...this.teacher });
      console.log('Teacher Added to Static Array:', this.teacher);
      console.log('Current Teachers List:', this.teachers);

      // Reset the form
      this.teacherForm.resetForm();
      this.teacher = {
        teacherID: '',
        firstName: '',
        lastName: '',
        gender: '',
        contactNumber: '',
        address: '',
        subject: '',
        educationLevel: ''
      };
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
    if (files && files.length > 0) {
      this.selectedFile = files[0];
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
      // Simulate CSV import with static data
      console.log('Simulating CSV Import for File:', this.selectedFile.name);

      const importedTeachers: Teacher[] = [
        {
          teacherID: '', // API would generate
          firstName: 'Alice',
          lastName: 'Smith',
          gender: 'Female',
          contactNumber: '1234567890',
          address: '123 Elm St',
          subject: 'Science',
          educationLevel: 'Masters'
        },
        {
          teacherID: '',
          firstName: 'Bob',
          lastName: 'Johnson',
          gender: 'Male',
          contactNumber: '0987654321',
          address: '456 Oak St',
          subject: 'Math',
          educationLevel: 'Degree'
        }
      ];

      // Add imported teachers to the static array
      this.teachers.push(...importedTeachers);
      console.log('Imported Teachers:', importedTeachers);
      console.log('Current Teachers List:', this.teachers);

      this.closeImportModal();
    }
  }

  getTranslation(key: string): string {
    return this.teacherLanguageService.getTranslation(key);
  }
}