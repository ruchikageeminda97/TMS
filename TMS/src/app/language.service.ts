import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LanguageService {
  // BehaviorSubject to broadcast language changes
  private languageSubject = new BehaviorSubject<string>('english');
  language$ = this.languageSubject.asObservable();

  private selectedLanguage: string = 'english';

  private translations: any = {
    english: {
      sinhala: 'Sinhala',
      dashboard: 'Dashboard',
      students: 'Students',
      all_classes: 'All Classes',
      stu_enroll: 'Student Enrollment',
      add_new_student: 'Add New Student',
      add_student: 'Add Student',
      add_subject: 'Add Subject',
      all_students: 'All Students',
      add_new_class: 'Add New Class',
      teachers: 'Teachers',
      add_teacher: 'Add Teacher',
      all_teachers: 'All Teachers',
      language: 'Language',
      logout: 'Logout',
      login: 'Login',
      username: 'Username',
      password: 'Password',
      enter_username: 'Enter your username',
      enter_password: 'Enter your password',
      today_classes: 'Today\'s Classes',
      class_name: 'Class Name',
      start_time: 'Start Time',
      end_time: 'End Time',
      room_number: 'Hall No',
      classes: 'Classes',
      today_income: 'Today\'s Income',
      ongoing_classes: 'Ongoing Classes',
      income: 'Income',
      last_7_days_income: 'Last 7 Days Income',
      day_1: 'Day 1',
      day_2: 'Day 2',
      day_3: 'Day 3',
      day_4: 'Day 4',
      day_5: 'Day 5',
      day_6: 'Day 6',
      day_7: 'Day 7',
      payment: 'Payment',
            // AllStudentsComponent translations
      student_id: 'Student ID',
      first_name: 'First Name',
      last_name: 'Last Name',
      date_of_birth: 'Date of Birth',
      gender: 'Gender',
      contact_number: 'Contact Number',
      email: 'Email',
      address: 'Address',
      admission_date: 'Admission Date',
      actions: 'Actions',
      edit: 'Edit',
      delete: 'Delete',
      confirm_delete: 'Are you sure you want to delete this student?'
    },
    sinhala: {
      payment: 'ගෙවීම්',
      sinhala: 'සිංහල',
      stu_enroll: 'සිසුන් ඇතුලත් කිරීම',
      add_new_class: 'නව පන්තියක් එකතු කරන්න',
      all_classes: 'සියලුම පන්තියන්',
      dashboard: 'උපකරණ පුවරුව',
      students: 'සිසුන්',
      today_classes: 'අද පන්තියන්',
      class_name: 'පන්ති නම',
      start_time: 'ආරම්භක වේලාව',
      end_time: 'අවසන් වේලාව',
      room_number: 'කාමර අංකය',
      add_new_student: 'නව සිසුවෙකු එකතු කරන්න',
      add_student: 'සිසුවෙකු එකතු කරන්න',
      all_students: 'සියලුම සිසුන්',
      teachers: 'ගුරුවරු',
      add_teacher: 'ගුරුවරයෙකු එකතු කරන්න',
      add_subject: 'විෂය එකතු කරන්න',
      all_teachers: 'සියලුම ගුරුවරු',
      language: 'භාෂාව',
      logout: 'ඉවත් වන්න',
      login: 'පිවිසෙන්න',
      username: 'පරිශීලක නම',
      password: 'මුරපදය',
      enter_username: 'ඔබේ පරිශීලක නම ඇතුලත් කරන්න',
      enter_password: 'ඔබේ මුරපදය ඇතුලත් කරන්න',
      classes: 'පන්ති',
      today_income: 'අද දින ආදායම',
      ongoing_classes: 'පවතින පන්ති',
      income: 'ආදායම',
      last_7_days_income: 'පසුගිය දින 7 ආදායම',
      day_1: 'දින 1',
      day_2: 'දින 2',
      day_3: 'දින 3',
      day_4: 'දින 4',
      day_5: 'දින 5',
      day_6: 'දින 6',
      day_7: 'දින 7',

      // AllStudentsComponent translations
      student_id: 'සිසු අංකය',
      first_name: 'මුල් නම',
      last_name: 'අවසන් නම',
      date_of_birth: 'උපන් දිනය',
      gender: 'ස්ත්‍රී පුරුෂ භාවය',
      contact_number: 'සම්බන්ධතා අංකය',
      email: 'ඊමේල්',
      address: 'ලිපිනය',
      admission_date: 'ඇතුලත් වූ දිනය',
      actions: 'ක්‍රියා',
      edit: 'සංස්කරණය',
      delete: 'මකන්න',
      confirm_delete: 'ඔබට මෙම සිසුවා මැකීමට අවශ්‍ය බව විශ්වාසද?'
    }
  };

  setLanguage(language: string): void {
    this.selectedLanguage = language;
    this.languageSubject.next(language); // Notify subscribers of the language change
  }

  getLanguage(): string {
    return this.selectedLanguage;
  }

  getTranslation(key: string): string {
    return this.translations[this.selectedLanguage][key] || key;
  }
}