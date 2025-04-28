import { Component } from '@angular/core';
import { Student } from '../models/student.model';
import { LanguageService } from '../language.service';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-all-students',
  standalone: true, 
  imports: [NgFor], 
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
    },
    {
      StudentID: 'S006',
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
      StudentID: 'S007',
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
      StudentID: 'S008',
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
      StudentID: 'S009',
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
      StudentID: 'S010',
      firstName: 'Kamal',
      lastName: 'Wijesinghe',
      dateOfBirth: '2006-01-18',
      gender: 'Male',
      contactNumber: '0723456789',
      email: 'kamal.w@example.com',
      address: '90 Beach Rd, Matara',
      enrollmentDate: '2023-05-15'
    },
    {
      StudentID: 'S011',
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
      StudentID: 'S012',
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
      StudentID: 'S013',
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
      StudentID: 'S014',
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
      StudentID: 'S015',
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
    // console.log('LanguageService in AllStudents:', this.languageService); 
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

 
}