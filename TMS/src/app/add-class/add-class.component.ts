import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms'; 
import { Class } from '../models/class.model';
import { ClassLanguageService } from '../languages/class.language';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-add-class',
  standalone: true,
  imports: [FormsModule,NgIf],
  templateUrl: './add-class.component.html',
  styleUrls: ['./add-class.component.css']
})
export class AddClassComponent {
  class: Class = {
    ClassID: "",
    className: "",
    teacherID: "",
    teacherName: "",
    date: "",
    time: "",
    subject: "",
    fee: 0, 
    student: []
  };

  startTime: string = "";
  endTime: string = "";
  isImportModalOpen = false; 
  isDragging = false; 
  selectedFile: File | null = null; 

  constructor(public languageService: ClassLanguageService) {
    console.log('ClassLanguageService in AddClass:', this.languageService);
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

  onSubmit(form: NgForm) {
    if (this.startTime && this.endTime) {
      this.class.time = `${this.startTime} to ${this.endTime}`;
    }

    if (form.valid) {
      console.log('Class Data:', this.class);
      alert(this.getTranslation('class_added_success'));
      this.resetForm();
    }
  }

  resetForm() {
    this.class = {
      ClassID: "",
      className: "",
      teacherID: "",
      teacherName: "",
      date: "",
      time: "",
      subject: "",
      fee: 0,
      student: []
    };
    this.startTime = "";
    this.endTime = "";
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
    }
  }
}