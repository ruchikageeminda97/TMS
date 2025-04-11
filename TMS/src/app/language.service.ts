import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root' // Singleton service available app-wide
})
export class LanguageService {
  private selectedLanguage: string = 'english'; // Default language

  // Combined translations for all components
  private translations: any = {
    english: {
      // Sidebar
      dashboard: 'Dashboard',
      students: 'Students',
      add_student: 'Add Student',
      all_students: 'All Students',
      teachers: 'Teachers',
      add_teacher: 'Add Teacher',
      all_teachers: 'All Teachers',
      language: 'Language',
      logout: 'Logout',
      // Login
      login: 'Login',
      username: 'Username',
      password: 'Password',
      enter_username: 'Enter your username',
      enter_password: 'Enter your password',
      // Dashboard
      classes: 'Classes',
      today_income: 'Today\'s Income',
      ongoing_classes: 'Ongoing Classes'
    },
    sinhala: {
      // Sidebar
      dashboard: 'උපකරණ පුවරුව',
      students: 'සිසුන්',
      add_student: 'සිසුවෙකු එකතු කරන්න',
      all_students: 'සියලුම සිසුන්',
      teachers: 'ගුරුවරු',
      add_teacher: 'ගුරුවරයෙකු එකතු කරන්න',
      all_teachers: 'සියලුම ගුරුවරු',
      language: 'භාෂාව',
      logout: 'ඉවත් වන්න',
      // Login
      login: 'පිවිසෙන්න',
      username: 'පරිශීලක නම',
      password: 'මුරපදය',
      enter_username: 'ඔබේ පරිශීලක නම ඇතුලත් කරන්න',
      enter_password: 'ඔබේ මුරපදය ඇතුලත් කරන්න',
      // Dashboard
      classes: 'පන්ති',
      today_income: 'අද දින ආදායම',
      ongoing_classes: 'පවතින පන්ති'
    }
  };

  setLanguage(language: string) {
    this.selectedLanguage = language;
  }

  getLanguage(): string {
    return this.selectedLanguage;
  }

  getTranslation(key: string): string {
    return this.translations[this.selectedLanguage][key] || key;
  }
}