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
      student_id: 'S001',
      first_name: 'John',
      last_name: 'Doe',
      date_of_birth: '2005-03-15',
      gender: 'Male',
      contact_number: '0712345678',
      email: 'john.doe@example.com',
      address: '123 Main St, Colombo',
      enrollment_date: '2023-01-10',
      status: 'Active'
    },
    {
      student_id: 'S002',
      first_name: 'Ama',
      last_name: 'Silva',
      date_of_birth: '2006-07-22',
      gender: 'Female',
      contact_number: '0778765432',
      email: 'ama.silva@example.com',
      address: '45 Park Rd, Kandy',
      enrollment_date: '2023-02-14',
      status: 'Active'
    },
    {
      student_id: 'S003',
      first_name: 'Ravi',
      last_name: 'Perera',
      date_of_birth: '2004-11-30',
      gender: 'Male',
      contact_number: '0761234567',
      email: 'ravi.perera@example.com',
      address: '78 Hill St, Galle',
      enrollment_date: '2023-03-20',
      status: 'Active'
    },
    {
      student_id: 'S004',
      first_name: 'Nimali',
      last_name: 'Fernando',
      date_of_birth: '2005-09-05',
      gender: 'Female',
      contact_number: '0759876543',
      email: 'nimali.fernando@example.com',
      address: '12 Lake Dr, Negombo',
      enrollment_date: '2023-04-01',
      status: 'Active'
    },
    {
      student_id: 'S005',
      first_name: 'Kamal',
      last_name: 'Wijesinghe',
      date_of_birth: '2006-01-18',
      gender: 'Male',
      contact_number: '0723456789',
      email: 'kamal.w@example.com',
      address: '90 Beach Rd, Matara',
      enrollment_date: '2023-05-15',
      status: 'Active'
    },
    {
      student_id: 'S006',
      first_name: 'John',
      last_name: 'Doe',
      date_of_birth: '2005-03-15',
      gender: 'Male',
      contact_number: '0712345678',
      email: 'john.doe@example.com',
      address: '123 Main St, Colombo',
      enrollment_date: '2023-01-10',
      status: 'Active'
    },
    {
      student_id: 'S007',
      first_name: 'Ama',
      last_name: 'Silva',
      date_of_birth: '2006-07-22',
      gender: 'Female',
      contact_number: '0778765432',
      email: 'ama.silva@example.com',
      address: '45 Park Rd, Kandy',
      enrollment_date: '2023-02-14',
      status: 'Active'
    },
    {
      student_id: 'S008',
      first_name: 'Ravi',
      last_name: 'Perera',
      date_of_birth: '2004-11-30',
      gender: 'Male',
      contact_number: '0761234567',
      email: 'ravi.perera@example.com',
      address: '78 Hill St, Galle',
      enrollment_date: '2023-03-20',
      status: 'Active'
    },
    {
      student_id: 'S009',
      first_name: 'Nimali',
      last_name: 'Fernando',
      date_of_birth: '2005-09-05',
      gender: 'Female',
      contact_number: '0759876543',
      email: 'nimali.fernando@example.com',
      address: '12 Lake Dr, Negombo',
      enrollment_date: '2023-04-01',
      status: 'Active'
    },
    {
      student_id: 'S010',
      first_name: 'Kamal',
      last_name: 'Wijesinghe',
      date_of_birth: '2006-01-18',
      gender: 'Male',
      contact_number: '0723456789',
      email: 'kamal.w@example.com',
      address: '90 Beach Rd, Matara',
      enrollment_date: '2023-05-15',
      status: 'Active'
    },
    {
      student_id: 'S011',
      first_name: 'John',
      last_name: 'Doe',
      date_of_birth: '2005-03-15',
      gender: 'Male',
      contact_number: '0712345678',
      email: 'john.doe@example.com',
      address: '123 Main St, Colombo',
      enrollment_date: '2023-01-10',
      status: 'Active'
    },
    {
      student_id: 'S012',
      first_name: 'Ama',
      last_name: 'Silva',
      date_of_birth: '2006-07-22',
      gender: 'Female',
      contact_number: '0778765432',
      email: 'ama.silva@example.com',
      address: '45 Park Rd, Kandy',
      enrollment_date: '2023-02-14',
      status: 'Active'
    },
    {
      student_id: 'S013',
      first_name: 'Ravi',
      last_name: 'Perera',
      date_of_birth: '2004-11-30',
      gender: 'Male',
      contact_number: '0761234567',
      email: 'ravi.perera@example.com',
      address: '78 Hill St, Galle',
      enrollment_date: '2023-03-20',
      status: 'Active'
    },
    {
      student_id: 'S014',
      first_name: 'Nimali',
      last_name: 'Fernando',
      date_of_birth: '2005-09-05',
      gender: 'Female',
      contact_number: '0759876543',
      email: 'nimali.fernando@example.com',
      address: '12 Lake Dr, Negombo',
      enrollment_date: '2023-04-01',
      status: 'Active'
    },
    {
      student_id: 'S015',
      first_name: 'Kamal',
      last_name: 'Wijesinghe',
      date_of_birth: '2006-01-18',
      gender: 'Male',
      contact_number: '0723456789',
      email: 'kamal.w@example.com',
      address: '90 Beach Rd, Matara',
      enrollment_date: '2023-05-15',
      status: 'Active'
    }
  ];

  constructor(public languageService: LanguageService) {}

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }
}