import { Component, OnInit } from '@angular/core';
import { CommonModule, AsyncPipe } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../api_services/services';
import { Student } from '../models/student.model';
import { Payment } from '../models/payment.model'; 
import { Observable, of } from 'rxjs';
import { map, startWith, tap } from 'rxjs/operators';

@Component({
  selector: 'app-payment-details',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, MatSnackBarModule, AsyncPipe],
  templateUrl: './payment-details.component.html',
  styleUrl: './payment-details.component.css'
})
export class PaymentDetailsComponent implements OnInit {
  students: Student[] = [];
  payments: Payment[] = [];
  searchForm: FormGroup;
  filteredStudents: Observable<Student[]> = of([]);
  selectedStudent: Student | null = null;

  constructor(
    private apiService: ApiService,
    private fb: FormBuilder,
    private snackBar: MatSnackBar
  ) {
    this.searchForm = this.fb.group({
      searchInput: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.fetchStudents();
    this.fetchPayments();
    this.setupAutocomplete();
  }

  private fetchStudents(): void {
    this.apiService.getStudents().subscribe({
      next: (students) => {
        console.log('Fetched students:', students);
        this.students = students || [];
      },
      error: (err) => {
        console.error('Error fetching students:', err);
        this.showSnackBar('Failed to load students');
        this.students = [];
        this.filteredStudents = of([]);
      }
    });
  }

  private fetchPayments(): void {
    this.apiService.getPayments('string').subscribe({
      next: (payments) => {
        console.log('Fetched payments:', payments);
        this.payments = (payments || []).map((p: any) => ({
          payment_id: p.payment_id ?? '',
          student_id: p.student_id ?? '',
          class_id: p.class_id ?? '',
          amount: p.amount ?? 0,
          payment_date: p.payment_date ?? '',
          month: p.month ?? '',
          year: p.year ?? '',
          status: p.status ?? ''
        }));
      },
      error: (err) => {
        console.error('Error fetching payments:', err);
        this.showSnackBar('Failed to load payments');
        this.payments = [];
      }
    });
  }

  private setupAutocomplete(): void {
    this.filteredStudents = this.searchForm.get('searchInput')!.valueChanges.pipe(
      startWith(''),
      map(value => this.filterStudents(value || '')),
      tap(filtered => console.log('Filtered students:', filtered))
    );
  }

  private filterStudents(value: string): Student[] {
    if (!value) {
      return [];
    }
    const filterValue = value.toLowerCase();
    return this.students.filter(student =>
      student.first_name.toLowerCase().startsWith(filterValue)
    ) || [];
  }

  getStudentName(student: Student): string {
    return `${student.first_name} ${student.last_name}`;
  }

  onSearch(): void {
    if (this.searchForm.invalid && !this.selectedStudent) {
      this.showSnackBar('Please enter or select a student');
      return;
    }

    const searchValue = this.searchForm.get('searchInput')?.value;
    const student = this.selectedStudent || this.students.find(s =>
      s.first_name.toLowerCase() === searchValue.toLowerCase() ||
      `${s.first_name} ${s.last_name}`.toLowerCase() === searchValue.toLowerCase()
    );

    if (student) {
      console.log('Found student ID:', student.student_id);
      this.showSnackBar(`Found student: ${this.getStudentName(student)} (ID: ${student.student_id})`);
    } else {
      console.log('No student found for search:', searchValue);
      this.showSnackBar(`No student found for: ${searchValue}`);
    }
  }

  selectStudent(student: Student): void {
    this.selectedStudent = student;
    this.searchForm.get('searchInput')?.setValue(this.getStudentName(student));
    this.filteredStudents = of([]);
    // Filter and log payments for the selected student
    const studentPayments = this.payments.filter(payment => 
      payment.student_id.toLowerCase() === student.student_id.toLowerCase()
    );
    console.log(`Payments for ${this.getStudentName(student)} (ID: ${student.student_id}):`, studentPayments);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }
}