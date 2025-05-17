import { Component, OnInit, ViewChild } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { NgClass, NgFor, NgIf } from '@angular/common';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Class } from '../models/class.model';
import { ClassLanguageService } from '../languages/class.language';
import { ApiService, Subject } from '../api_services/services';

@Component({
  selector: 'app-add-class',
  standalone: true,
  imports: [FormsModule, NgIf, NgClass, MatSnackBarModule, NgFor],
  templateUrl: './add-class.component.html',
  styleUrls: ['./add-class.component.css']
})
export class AddClassComponent implements OnInit {
  @ViewChild('classForm') classForm!: NgForm;

  class: Class = {
    class_id: '',
    class_name: '',
    subject_id: '',
    day: '',
    start_time: '',
    end_time: '',
    room_number: '',
    capacity: 0,
    status: 'Ongoing'
  };

  subjects: Subject[] = [];
  weekdays: string[] = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  isImportModalOpen = false;
  isDragging = false;
  selectedFile: File | null = null;

  constructor(
    public languageService: ClassLanguageService,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.apiService.getSubjects().subscribe({
      next: (subjects) => {
        console.log('Fetched subjects:', subjects);
        this.subjects = subjects;
      },
      error: (err) => {
        console.error('Error fetching subjects:', err);
        this.showSnackBar(this.getTranslation('fetch_subjects_failed'));
      }
    });
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }

  onSubmit(): void {
    if (this.classForm.valid) {
      this.apiService.addClass(this.class).subscribe({
        next: () => {
          this.showSnackBar(this.getTranslation('class_added_success'));
          this.classForm.resetForm();
          this.class = {
            class_id: '',
            class_name: '',
            subject_id: '',
            day: '',
            start_time: '',
            end_time: '',
            room_number: '',
            capacity: 0,
            status: 'Ongoing'
          };
        },
        error: (err) => {
          console.error('Error adding class:', err);
          this.showSnackBar(this.getTranslation('class_add_failed'));
        }
      });
    } else {
      this.showSnackBar(this.getTranslation('class_add_failed'));
    }
  }

  openImportModal() { this.isImportModalOpen = true; }
  closeImportModal() { this.isImportModalOpen = false; this.selectedFile = null; this.isDragging = false; }
  onDragOver(event: DragEvent) { event.preventDefault(); this.isDragging = true; }
  onDragLeave(event: DragEvent) { event.preventDefault(); this.isDragging = false; }
  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
    const files = event.dataTransfer?.files;
    if (files && files.length > 0 && files[0].type === 'text/csv') {
      this.selectedFile = files[0];
    } else {
      this.showSnackBar(this.getTranslation('invalid_csv_file'));
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
      console.log('Importing CSV:', this.selectedFile);
      this.closeImportModal();
      this.showSnackBar(this.getTranslation('csv_import_success'));
    }
  }
}