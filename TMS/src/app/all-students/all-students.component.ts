import { Component } from '@angular/core';
import { Student } from '../models/student.model';
import { LanguageService } from '../language.service';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-all-students',
  standalone: true, // Ensure standalone is true
  imports: [NgFor], // No additional imports needed for now
  templateUrl: './all-students.component.html',
  styleUrls: ['./all-students.component.css']
})
export class AllStudentsComponent {
  students: Student[] = [
    {
      StudentID: 'S001',
      firstName: 'John',
      lastName: 'Doe',
      dateOfBirth: '2005-03-15',
      gender: 'Male',
      contactNumber: '0712345678',
      email: 'john.doe@example.com',
      address: '123 Main St, Colombo',
      enrollmentDate: '2023-01-10'
    },
    {
      StudentID: 'S002',
      firstName: 'Ama',
      lastName: 'Silva',
      dateOfBirth: '2006-07-22',
      gender: 'Female',
      contactNumber: '0778765432',
      email: 'ama.silva@example.com',
      address: '45 Park Rd, Kandy',
      enrollmentDate: '2023-02-14'
    },
    {
      StudentID: 'S003',
      firstName: 'Ravi',
      lastName: 'Perera',
      dateOfBirth: '2004-11-30',
      gender: 'Male',
      contactNumber: '0761234567',
      email: 'ravi.perera@example.com',
      address: '78 Hill St, Galle',
      enrollmentDate: '2023-03-20'
    },
    {
      StudentID: 'S004',
      firstName: 'Nimali',
      lastName: 'Fernando',
      dateOfBirth: '2005-09-05',
      gender: 'Female',
      contactNumber: '0759876543',
      email: 'nimali.fernando@example.com',
      address: '12 Lake Dr, Negombo',
      enrollmentDate: '2023-04-01'
    },
    {
      StudentID: 'S005',
      firstName: 'Kamal',
      lastName: 'Wijesinghe',
      dateOfBirth: '2006-01-18',
      gender: 'Male',
      contactNumber: '0723456789',
      email: 'kamal.w@example.com',
      address: '90 Beach Rd, Matara',
      enrollmentDate: '2023-05-15'
    }
  ];

  constructor(public languageService: LanguageService) {
    console.log('LanguageService in AllStudents:', this.languageService); // Debug
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

  editStudent(student: Student) {
    console.log('Edit student:', student);
    // TODO: Implement edit functionality (e.g., open a modal or navigate to edit page)
  }

  deleteStudent(studentId: string) {
    if (confirm(this.getTranslation('confirm_delete'))) { 
      this.students = this.students.filter(student => student.StudentID !== studentId);
      console.log('Deleted student with ID:', studentId);
    }
  }
}