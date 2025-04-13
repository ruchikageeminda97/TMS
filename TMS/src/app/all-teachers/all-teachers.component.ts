import { Component } from '@angular/core';
import { CommonModule, NgFor } from '@angular/common';
import { Teacher } from '../models/teacher.model';
import { LanguageService } from '../language.service';
import { TeacherLanguageService } from '../languages/teacher.language';

@Component({
  selector: 'app-all-teachers',
  standalone: true,
  imports: [CommonModule,NgFor],
  templateUrl: './all-teachers.component.html',
  styleUrls: ['./all-teachers.component.css']
})
export class AllTeachersComponent {
  // Static data for design purposes
  teachers: Teacher[] = [
    {
      teacherID: 'TCH-001',
      firstName: 'Alice',
      lastName: 'Smith',
      gender: 'Female',
      contactNumber: '1234567890',
      address: '123 Elm St',
      subject: 'Science',
      educationLevel: 'Masters'
    },
    {
      teacherID: 'TCH-002',
      firstName: 'Bob',
      lastName: 'Johnson',
      gender: 'Male',
      contactNumber: '0987654321',
      address: '456 Oak St',
      subject: 'Math',
      educationLevel: 'Degree'
    },
    {
      teacherID: 'TCH-003',
      firstName: 'Clara',
      lastName: 'Williams',
      gender: 'Female',
      contactNumber: '5555555555',
      address: '789 Pine St',
      subject: 'English',
      educationLevel: 'PhD'
    },
    {
      teacherID: 'TCH-001',
      firstName: 'Alice',
      lastName: 'Smith',
      gender: 'Female',
      contactNumber: '1234567890',
      address: '123 Elm St',
      subject: 'Science',
      educationLevel: 'Masters'
    },
    {
      teacherID: 'TCH-002',
      firstName: 'Bob',
      lastName: 'Johnson',
      gender: 'Male',
      contactNumber: '0987654321',
      address: '456 Oak St',
      subject: 'Math',
      educationLevel: 'Degree'
    },
    {
      teacherID: 'TCH-003',
      firstName: 'Clara',
      lastName: 'Williams',
      gender: 'Female',
      contactNumber: '5555555555',
      address: '789 Pine St',
      subject: 'English',
      educationLevel: 'PhD'
    },
    {
      teacherID: 'TCH-001',
      firstName: 'Alice',
      lastName: 'Smith',
      gender: 'Female',
      contactNumber: '1234567890',
      address: '123 Elm St',
      subject: 'Science',
      educationLevel: 'Masters'
    },
    {
      teacherID: 'TCH-002',
      firstName: 'Bob',
      lastName: 'Johnson',
      gender: 'Male',
      contactNumber: '0987654321',
      address: '456 Oak St',
      subject: 'Math',
      educationLevel: 'Degree'
    },
    {
      teacherID: 'TCH-003',
      firstName: 'Clara',
      lastName: 'Williams',
      gender: 'Female',
      contactNumber: '5555555555',
      address: '789 Pine St',
      subject: 'English',
      educationLevel: 'PhD'
    },
    {
      teacherID: 'TCH-001',
      firstName: 'Alice',
      lastName: 'Smith',
      gender: 'Female',
      contactNumber: '1234567890',
      address: '123 Elm St',
      subject: 'Science',
      educationLevel: 'Masters'
    },
    {
      teacherID: 'TCH-002',
      firstName: 'Bob',
      lastName: 'Johnson',
      gender: 'Male',
      contactNumber: '0987654321',
      address: '456 Oak St',
      subject: 'Math',
      educationLevel: 'Degree'
    },
    {
      teacherID: 'TCH-003',
      firstName: 'Clara',
      lastName: 'Williams',
      gender: 'Female',
      contactNumber: '5555555555',
      address: '789 Pine St',
      subject: 'English',
      educationLevel: 'PhD'
    },
    {
      teacherID: 'TCH-001',
      firstName: 'Alice',
      lastName: 'Smith',
      gender: 'Female',
      contactNumber: '1234567890',
      address: '123 Elm St',
      subject: 'Science',
      educationLevel: 'Masters'
    },
    {
      teacherID: 'TCH-002',
      firstName: 'Bob',
      lastName: 'Johnson',
      gender: 'Male',
      contactNumber: '0987654321',
      address: '456 Oak St',
      subject: 'Math',
      educationLevel: 'Degree'
    },
    {
      teacherID: 'TCH-003',
      firstName: 'Clara',
      lastName: 'Williams',
      gender: 'Female',
      contactNumber: '5555555555',
      address: '789 Pine St',
      subject: 'English',
      educationLevel: 'PhD'
    }
  ];

  constructor(
    public languageService: LanguageService,
    public teacherLanguageService: TeacherLanguageService
  ) {
    // Sync language with sidebar toggle
    this.languageService.language$.subscribe(language => {
      this.teacherLanguageService.setLanguage(language);
    });
  }

  editTeacher(index: number): void {
    // Placeholder for edit functionality (non-functional for now)
    console.log('Edit teacher at index:', index);
  }

  deleteTeacher(index: number): void {
    // Show confirmation prompt for design purposes
    if (confirm(this.teacherLanguageService.getTranslation('confirm_delete'))) {
      console.log('Delete teacher at index:', index);
      // No actual deletion since we're using static data
    }
  }

  getTranslation(key: string): string {
    return this.teacherLanguageService.getTranslation(key);
  }
}