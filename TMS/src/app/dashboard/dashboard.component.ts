import { Component, OnInit } from '@angular/core';
import { NgFor } from '@angular/common';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { LanguageService } from '../language.service';
import { ApiService, StatsCounts } from '../api_services/services';
import { Class } from '../models/class.model';

interface ClassDisplay {
  className: string;
  startTime: string;
  endTime: string;
  roomNumber: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [NgFor, MatSnackBarModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  studentCount: number = 0;
  teacherCount: number = 0;
  classCount: number = 0;
  todayIncome: string = 'LKR 500';
  ongoingClasses: number = 1;

  incomes = [
    { date: 'Apr 6', income: 8000 },
    { date: 'Apr 7', income: 7600 },
    { date: 'Apr 8', income: 6000 },
    { date: 'Apr 9', income: 18000 },
    { date: 'Apr 10', income: 12000 },
    { date: 'Apr 11', income: 9000 },
    { date: 'Apr 12', income: 12500 }
  ];

  classes: ClassDisplay[] = [];

  yAxisMax!: number;
  yAxisLabels: { value: number; position: number }[] = [];

  constructor(
    public languageService: LanguageService,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {
    this.updateYAxis();
  }

  ngOnInit(): void {
    this.fetchStats();
    this.fetchTodayClasses();
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }

  private fetchStats(): void {
    this.apiService.getStatsCounts().subscribe({
      next: (stats: StatsCounts) => {
        this.studentCount = stats.students;
        this.teacherCount = stats.teachers;
        this.classCount = stats.classes;
      },
      error: (err) => {
        console.error('Error fetching stats:', err);
        this.showSnackBar(this.getTranslation('fetch_stats_failed'));
      }
    });
  }

  private fetchTodayClasses(): void {
    this.apiService.getTodayClasses().subscribe({
      next: (response) => {
        console.log('Fetched today classes:', response);
        this.classes = response.today_classes.map(cls => ({
          className: cls.class_name,
          startTime: this.formatTime(cls.start_time),
          endTime: this.formatTime(cls.end_time),
          roomNumber: cls.room_number || 'N/A'
        }));
        this.ongoingClasses = response.today_classes.filter(cls => cls.status === 'Ongoing').length;
      },
      error: (err) => {
        console.error('Error fetching today classes:', err);
        this.showSnackBar(this.getTranslation('fetch_classes_failed'));
      }
    });
  }

  private formatTime(time: string): string {
    // Convert HH:MM to HH:MM AM/PM
    const [hours, minutes] = time.split(':').map(Number);
    const period = hours >= 12 ? 'PM' : 'AM';
    const adjustedHours = hours % 12 || 12;
    return `${adjustedHours}:${minutes.toString().padStart(2, '0')} ${period}`;
  }

  getBarHeight(income: number): number {
    return (income / this.yAxisMax) * 90;
  }

  formatIncome(income: number): string {
    return `${income.toLocaleString()}`;
  }

  private updateYAxis() {
    const maxIncome = Math.max(...this.incomes.map(item => item.income), 1000);
    this.yAxisMax = Math.ceil(maxIncome / 1000) * 1000;
    
    const increment = this.yAxisMax / 4;
    this.yAxisLabels = [];
    for (let i = 0; i <= 4; i++) {
      const value = i * increment;
      const position = ((this.yAxisMax - value) / this.yAxisMax) * 100;
      this.yAxisLabels.push({ value, position });
    }
  }

  updateIncomes() {
    this.incomes = [
      { date: 'Apr 6', income: 10000 },
      { date: 'Apr 7', income: 8200 },
      { date: 'Apr 8', income: 7000 },
      { date: 'Apr 9', income: 15000 },
      { date: 'Apr 10', income: 11000 },
      { date: 'Apr 11', income: 9500 },
      { date: 'Apr 12', income: 13000 }
    ];
    this.updateYAxis();
  }

  trackByDate(index: number, item: { date: string; income: number }): string {
    return item.date;
  }
}