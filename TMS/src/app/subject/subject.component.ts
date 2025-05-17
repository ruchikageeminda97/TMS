import { Component, ViewChild } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { NgClass, NgIf } from '@angular/common';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { LanguageService } from '../language.service';
import { ApiService, Subject } from '../api_services/services';
@Component({
  selector: 'app-subject',
  imports: [FormsModule, NgClass, NgIf, MatSnackBarModule],
  templateUrl: './subject.component.html',
  styleUrl: './subject.component.css'
})
export class SubjectComponent {
  @ViewChild('subjectForm') subjectForm!: NgForm;

  subject: Subject = {
    subject_id: '',
    subject_name: '',
    description: '',
    level: ''
  };

  constructor(
    private apiService: ApiService,
    private snackBar: MatSnackBar,
    public languageService: LanguageService
  ) {}

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }

  onSubmit(): void {
    if (this.subjectForm.valid) {
      this.apiService.addSubject(this.subject).subscribe({
        next: () => {
          this.showSnackBar(this.getTranslation('subject_added'));
          this.subjectForm.resetForm();
          this.subject = {
            subject_id: '',
            subject_name: '',
            description: '',
            level: ''
          };
        },
        error: (err) => {
          console.error('Error adding subject:', err);
          this.showSnackBar(this.getTranslation('subject_add_failed'));
        }
      });
    } else {
      this.showSnackBar(this.getTranslation('subject_add_failed'));
    }
  }
}