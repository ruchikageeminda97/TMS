import { Component } from '@angular/core';
import { LanguageService } from '../language.service'; 

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  
  studentCount: number = 150;
  teacherCount: number = 25;
  classCount: number = 40;
  todayIncome: string = 'LKR 12,500';
  ongoingClasses: number = 8;

  constructor(public languageService: LanguageService) {} 

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }
}