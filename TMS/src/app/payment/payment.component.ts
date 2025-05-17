import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../api_services/services';
import { Class } from '../models/class.model';
import { Student } from '../models/student.model';

@Component({
  selector: 'app-payment',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, MatSnackBarModule],
  templateUrl: './payment.component.html',
  styleUrl: './payment.component.css'
})
export class PaymentComponent implements OnInit {
  classes: Class[] = [];
  students: Student[] = [];
  paymentForm: FormGroup;
  months = [
    { name: 'January', value: '01' },
    { name: 'February', value: '02' },
    { name: 'March', value: '03' },
    { name: 'April', value: '04' },
    { name: 'May', value: '05' },
    { name: 'June', value: '06' },
    { name: 'July', value: '07' },
    { name: 'August', value: '08' },
    { name: 'September', value: '09' },
    { name: 'October', value: '10' },
    { name: 'November', value: '11' },
    { name: 'December', value: '12' }
  ];

  constructor(
    private apiService: ApiService,
    private fb: FormBuilder,
    private snackBar: MatSnackBar
  ) {
    this.paymentForm = this.fb.group({
      studentId: ['', Validators.required],
      classId: ['', Validators.required],
      month: ['', Validators.required],
      year: ['', [Validators.required, Validators.pattern(/^\d{4}$/)]],
      amount: ['', [Validators.required, Validators.min(1)]]
    });
  }

  ngOnInit(): void {
    this.fetchStudents();
    this.getClasses();
  }

  private fetchStudents(): void {
    this.apiService.getStudents().subscribe({
      next: (students) => {
        console.log('Fetched students:', students);
        this.students = students;
      },
      error: (err) => {
        console.error('Error fetching students:', err);
        this.showSnackBar('Failed to load students');
      }
    });
  }

  private getClasses(): void {
    this.apiService.getClasses().subscribe({
      next: (classes) => {
        console.log('Fetched classes:', classes);
        this.classes = classes;
      },
      error: (err) => {
        console.error('Error fetching classes:', err);
        this.showSnackBar('Failed to load classes');
      }
    });
  }

  getStudentName(student: Student): string {
    return `${student.first_name} ${student.last_name}`;
  }

  onSubmit(): void {
    if (this.paymentForm.invalid) {
      this.showSnackBar('Please fill all required fields correctly');
      return;
    }

    const formValue = this.paymentForm.value;
    const payment = {
      student_id: formValue.studentId,
      class_id: formValue.classId,
      amount: Number(formValue.amount),
      payment_date: new Date().toISOString().split('T')[0],
      month: formValue.month,
      year: String(formValue.year),
      status: 'Paid'
    };

    const username = localStorage.getItem('username') || 'admin';

    console.log('Sending payment:', payment); 

    this.apiService.makePayment(payment, username).subscribe({
      next: (response) => {
        this.showSnackBar('Payment recorded successfully');
        this.paymentForm.reset();
      },
      error: (err) => {
        console.error('Error recording payment:', err);
        if (err.error?.detail) {
          console.error('Validation errors:', err.error.detail);
          this.showSnackBar(`Failed to record payment: ${JSON.stringify(err.error.detail)}`);
        } else {
          this.showSnackBar('Failed to record payment');
        }
      }
    });
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }
}