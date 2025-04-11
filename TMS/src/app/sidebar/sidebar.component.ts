import { NgClass } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { LanguageService } from '../language.service'; // Double-check this path

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

  constructor(public languageService: LanguageService) {
    // Log to verify injection
    console.log('LanguageService in Sidebar:', this.languageService);
  }

  toggleStudentsSubmenu(): void {
    this.isStudentsOpen = !this.isStudentsOpen;
    if (this.isStudentsOpen) {
      this.isTeachersOpen = false;
    }
  }

  toggleTeachersSubmenu(): void {
    this.isTeachersOpen = !this.isTeachersOpen;
    if (this.isTeachersOpen) {
      this.isStudentsOpen = false;
    }
  }

  setLanguage(language: string) {
    this.languageService.setLanguage(language);
  }

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }
}