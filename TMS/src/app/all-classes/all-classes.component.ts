import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Class } from '../models/class.model'; // Assuming the interface is in a models folder
import { LanguageService } from '../language.service';
import { ClassLanguageService } from '../languages/class.language';

@Component({
  selector: 'app-all-classes',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './all-classes.component.html'
  // No styleUrl since styles are in global styles.css
})
export class AllClassesComponent {
  classes: Class[] = [
    {
      ClassID: 'CLS-001',
      className: 'Grade 10 Science',
      teacherID: 'TCH-001',
      teacherName: 'Alice Smith',
      date: '2025-04-15',
      time: '10:00 AM - 12:00 PM',
      subject: 'Science',
      fee: 1500,
      student: ['STD-001', 'STD-002', 'STD-003']
    },
    {
      ClassID: 'CLS-002',
      className: 'Grade 11 Math',
      teacherID: 'TCH-002',
      teacherName: 'Bob Johnson',
      date: '2025-04-16',
      time: '02:00 PM - 04:00 PM',
      subject: 'Math',
      fee: 2000,
      student: ['STD-004', 'STD-005']
    },
    {
      ClassID: 'CLS-003',
      className: 'Grade 12 English',
      teacherID: 'TCH-003',
      teacherName: 'Clara Williams',
      date: '2025-04-17',
      time: '09:00 AM - 11:00 AM',
      subject: 'English',
      fee: 1800,
      student: ['STD-006', 'STD-007', 'STD-008', 'STD-009']
    },
    {
      ClassID: 'CLS-001',
      className: 'Grade 10 Science',
      teacherID: 'TCH-001',
      teacherName: 'Alice Smith',
      date: '2025-04-15',
      time: '10:00 AM - 12:00 PM',
      subject: 'Science',
      fee: 1500,
      student: ['STD-001', 'STD-002', 'STD-003']
    },
    {
      ClassID: 'CLS-002',
      className: 'Grade 11 Math',
      teacherID: 'TCH-002',
      teacherName: 'Bob Johnson',
      date: '2025-04-16',
      time: '02:00 PM - 04:00 PM',
      subject: 'Math',
      fee: 2000,
      student: ['STD-004', 'STD-005']
    },
    {
      ClassID: 'CLS-003',
      className: 'Grade 12 English',
      teacherID: 'TCH-003',
      teacherName: 'Clara Williams',
      date: '2025-04-17',
      time: '09:00 AM - 11:00 AM',
      subject: 'English',
      fee: 1800,
      student: ['STD-006', 'STD-007', 'STD-008', 'STD-009']
    },
    {
      ClassID: 'CLS-001',
      className: 'Grade 10 Science',
      teacherID: 'TCH-001',
      teacherName: 'Alice Smith',
      date: '2025-04-15',
      time: '10:00 AM - 12:00 PM',
      subject: 'Science',
      fee: 1500,
      student: ['STD-001', 'STD-002', 'STD-003']
    },
    {
      ClassID: 'CLS-002',
      className: 'Grade 11 Math',
      teacherID: 'TCH-002',
      teacherName: 'Bob Johnson',
      date: '2025-04-16',
      time: '02:00 PM - 04:00 PM',
      subject: 'Math',
      fee: 2000,
      student: ['STD-004', 'STD-005']
    },
    {
      ClassID: 'CLS-003',
      className: 'Grade 12 English',
      teacherID: 'TCH-003',
      teacherName: 'Clara Williams',
      date: '2025-04-17',
      time: '09:00 AM - 11:00 AM',
      subject: 'English',
      fee: 1800,
      student: ['STD-006', 'STD-007', 'STD-008', 'STD-009']
    },
    {
      ClassID: 'CLS-001',
      className: 'Grade 10 Science',
      teacherID: 'TCH-001',
      teacherName: 'Alice Smith',
      date: '2025-04-15',
      time: '10:00 AM - 12:00 PM',
      subject: 'Science',
      fee: 1500,
      student: ['STD-001', 'STD-002', 'STD-003']
    },
    {
      ClassID: 'CLS-002',
      className: 'Grade 11 Math',
      teacherID: 'TCH-002',
      teacherName: 'Bob Johnson',
      date: '2025-04-16',
      time: '02:00 PM - 04:00 PM',
      subject: 'Math',
      fee: 2000,
      student: ['STD-004', 'STD-005']
    },
    {
      ClassID: 'CLS-003',
      className: 'Grade 12 English',
      teacherID: 'TCH-003',
      teacherName: 'Clara Williams',
      date: '2025-04-17',
      time: '09:00 AM - 11:00 AM',
      subject: 'English',
      fee: 1800,
      student: ['STD-006', 'STD-007', 'STD-008', 'STD-009']
    },
    {
      ClassID: 'CLS-001',
      className: 'Grade 10 Science',
      teacherID: 'TCH-001',
      teacherName: 'Alice Smith',
      date: '2025-04-15',
      time: '10:00 AM - 12:00 PM',
      subject: 'Science',
      fee: 1500,
      student: ['STD-001', 'STD-002', 'STD-003']
    },
    {
      ClassID: 'CLS-002',
      className: 'Grade 11 Math',
      teacherID: 'TCH-002',
      teacherName: 'Bob Johnson',
      date: '2025-04-16',
      time: '02:00 PM - 04:00 PM',
      subject: 'Math',
      fee: 2000,
      student: ['STD-004', 'STD-005']
    },
    {
      ClassID: 'CLS-003',
      className: 'Grade 12 English',
      teacherID: 'TCH-003',
      teacherName: 'Clara Williams',
      date: '2025-04-17',
      time: '09:00 AM - 11:00 AM',
      subject: 'English',
      fee: 1800,
      student: ['STD-006', 'STD-007', 'STD-008', 'STD-009']
    },
    {
      ClassID: 'CLS-001',
      className: 'Grade 10 Science',
      teacherID: 'TCH-001',
      teacherName: 'Alice Smith',
      date: '2025-04-15',
      time: '10:00 AM - 12:00 PM',
      subject: 'Science',
      fee: 1500,
      student: ['STD-001', 'STD-002', 'STD-003']
    },
    {
      ClassID: 'CLS-002',
      className: 'Grade 11 Math',
      teacherID: 'TCH-002',
      teacherName: 'Bob Johnson',
      date: '2025-04-16',
      time: '02:00 PM - 04:00 PM',
      subject: 'Math',
      fee: 2000,
      student: ['STD-004', 'STD-005']
    },
    {
      ClassID: 'CLS-003',
      className: 'Grade 12 English',
      teacherID: 'TCH-003',
      teacherName: 'Clara Williams',
      date: '2025-04-17',
      time: '09:00 AM - 11:00 AM',
      subject: 'English',
      fee: 1800,
      student: ['STD-006', 'STD-007', 'STD-008', 'STD-009']
    }
  ];

  constructor(
    public languageService: LanguageService,
    public classLanguageService: ClassLanguageService
  ) {
    // Sync language with sidebar toggle
    this.languageService.language$.subscribe(language => {
      this.classLanguageService.setLanguage(language);
    });
  }

  editClass(index: number): void {
    console.log('Edit class at index:', index);
  }

  deleteClass(index: number): void {
    if (confirm(this.classLanguageService.getTranslation('confirm_delete'))) {
      console.log('Delete class at index:', index);
    }
  }

  getTranslation(key: string): string {
    return this.classLanguageService.getTranslation(key);
  }
}

