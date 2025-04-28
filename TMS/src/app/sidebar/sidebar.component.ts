import { NgClass } from '@angular/common';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { LanguageService } from '../language.service';
import { ClassLanguageService } from '../languages/class.language';
import { TeacherLanguageService } from '../languages/teacher.language';
import { trigger, transition, style, animate } from '@angular/animations';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, NgClass, DatePipe],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css'],
  providers: [DatePipe],
  animations: [
    trigger('slideIn', [
      transition(':enter', [
        style({ transform: 'translateX(-100%)', opacity: 0 }),
        animate('0.4s ease-out', style({ transform: 'translateX(0)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('0.4s ease-in', style({ transform: 'translateX(-100%)', opacity: 0 }))
      ])
    ])
  ]
})
export class SidebarComponent implements OnInit, OnDestroy {
  isSidebarOpen: boolean = false;
  isStudentsOpen: boolean = false;
  isTeachersOpen: boolean = false;
  isClassOpen: boolean = false;
  currentDate: string = '';
  currentTime: string = '';
  private timeInterval: any;

  constructor(
    public languageService: LanguageService,
    public classLanguageService: ClassLanguageService,
    public teacherLanguageService: TeacherLanguageService,
    private datePipe: DatePipe
  ) {}

  ngOnInit(): void {
    this.updateDateTime();
    this.timeInterval = setInterval(() => this.updateDateTime(), 1000);
  }

  ngOnDestroy(): void {
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
  }

  updateDateTime(): void {
    const now = new Date();
    this.currentDate = this.datePipe.transform(now, 'EEEE, MMMM d, yyyy') || now.toDateString();
    this.currentTime = this.datePipe.transform(now, 'HH:mm:ss') || now.toTimeString().split(' ')[0];
  }

  toggleSidebar(): void {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  toggleStudentsSubmenu(): void {
    this.isStudentsOpen = !this.isStudentsOpen;
    if (this.isStudentsOpen) {
      this.isTeachersOpen = false;
      this.isClassOpen = false;
    }
  }

  toggleTeachersSubmenu(): void {
    this.isTeachersOpen = !this.isTeachersOpen;
    if (this.isTeachersOpen) {
      this.isStudentsOpen = false;
      this.isClassOpen = false;
    }
  }

  toggleClassesSubmenu(): void {
    this.isClassOpen = !this.isClassOpen;
    if (this.isClassOpen) {
      this.isStudentsOpen = false;
      this.isTeachersOpen = false;
    }
  }

  setLanguage(language: string): void {
    this.languageService.setLanguage(language);
    this.classLanguageService.setLanguage(language);
    this.teacherLanguageService.setLanguage(language);
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }
}