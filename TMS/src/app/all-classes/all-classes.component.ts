import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Class } from '../models/class.model';
import { ClassLanguageService } from '../languages/class.language';
import { LanguageService } from '../language.service';
import { ApiService } from '../api_services/services';

@Component({
  selector: 'app-all-classes',
  standalone: true,
  imports: [CommonModule, MatSnackBarModule],
  templateUrl: './all-classes.component.html'
})
export class AllClassesComponent implements OnInit {
  classes: Class[] = [];

  constructor(
    public languageService: LanguageService,
    public classLanguageService: ClassLanguageService,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {
    // Sync language with sidebar toggle
    this.languageService.language$.subscribe(language => {
      this.classLanguageService.setLanguage(language);
    });
  }

  ngOnInit(): void {
    this.apiService.getClasses().subscribe({
      next: (classes) => {
        console.log('Fetched classes:', classes);
        this.classes = classes;
      },
      error: (err) => {
        console.error('Error fetching classes:', err);
        this.showSnackBar(this.getTranslation('fetch_classes_failed'));
      }
    });
  }

  editClass(index: number): void {
    console.log('Edit class:', this.classes[index]);
    // TODO: Implement edit functionality (e.g., navigate to edit form)
  }

  deleteClass(index: number): void {
    if (confirm(this.getTranslation('confirm_delete'))) {
      console.log('Delete class:', this.classes[index]);
      // TODO: Implement delete API call
      // this.apiService.deleteClass(this.classes[index].class_id).subscribe({...});
    }
  }

  getTranslation(key: string): string {
    return this.classLanguageService.getTranslation(key);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }
}