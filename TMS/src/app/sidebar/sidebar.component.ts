import { NgClass } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { LanguageService } from '../language.service'; 
import { ClassLanguageService } from '../languages/class.language'; 

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, NgClass],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent {
  isStudentsOpen: boolean = false;
  isTeachersOpen: boolean = false;
  isClassOpen: boolean = false;

  constructor(
    public languageService: LanguageService,
    public classLanguageService: ClassLanguageService
  ) {
    // console.log('LanguageService in Sidebar:', this.languageService);
    // console.log('ClassLanguageService in Sidebar:', this.classLanguageService);
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

  setLanguage(language: string) {
    this.languageService.setLanguage(language); 
    this.classLanguageService.setLanguage(language); 
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key); 
  }
}