import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TeacherLanguageService {
  private translations: { [key: string]: { [key: string]: string } } = {
    english: {
      add_new_teacher: 'Add New Teacher',
      import_teacher_list: 'Import Teacher List',
      first_name: 'First Name',
      enter_first_name: 'Enter first name',
      invalid_first_name: 'First name must contain only letters',
      last_name: 'Last Name',
      enter_last_name: 'Enter last name',
      invalid_last_name: 'Last name must contain only letters',
      gender: 'Gender',
      select_gender: 'Select gender',
      male: 'Male',
      female: 'Female',
      other: 'Other',
      invalid_gender: 'Please select a gender',
      contact_number: 'Contact Number',
      enter_contact_number: 'Enter contact number',
      invalid_contact_number: 'Contact number must be 10 digits',
      address: 'Address',
      enter_address: 'Enter address',
      invalid_address: 'Address is required',
      subject: 'Subject',
      enter_subject: 'Enter subject',
      invalid_subject: 'Subject is required',
      education_level: 'Education Level',
      select_education_level: 'Select education level',
      diploma: 'Diploma',
      degree: 'Degree',
      masters: 'Masters',
      phd: 'PhD',
      invalid_education_level: 'Please select an education level',
      add_teacher: 'Add Teacher',
      drag_drop_csv: 'Drag & Drop CSV File Here',
      choose_file: 'Choose File',
      cancel: 'Cancel',
      import: 'Import',
      // AllTeachersComponent translations
      all_teachers : 'All Teachers',
      teacher_id: 'Teacher ID',
      actions: 'Actions',
      edit: 'Edit',
      delete: 'Delete',
      confirm_delete: 'Are you sure you want to delete this teacher?'
    },
    sinhala: {
      add_new_teacher: 'නව ගුරුවරයෙක් එක් කරන්න',
      import_teacher_list: 'ගුරු ලැයිස්තුව ආයාත කරන්න',
      first_name: 'මුල් නම',
      enter_first_name: 'මුල් නම ඇතුලත් කරන්න',
      invalid_first_name: 'මුල් නමේ අකුරු පමණක් තිබිය යුතුය',
      last_name: 'අවසන් නම',
      enter_last_name: 'අවසන් නම ඇතුලත් කරන්න',
      invalid_last_name: 'අවසන් නමේ අකුරු පමණක් තිබිය යුතුය',
      gender: 'ස්ත්‍රී පුරුෂ භාවය',
      select_gender: 'ස්ත්‍රී පුරුෂ භාවය තෝරන්න',
      male: 'පිරිමි',
      female: 'ගැහැණු',
      other: 'වෙනත්',
      invalid_gender: 'කරුණාකර ස්ත්‍රී පුරුෂ භාවය තෝරන්න',
      contact_number: 'සම්බන්ධතා අංකය',
      enter_contact_number: 'සම්බන්ධතා අංකය ඇතුලත් කරන්න',
      invalid_contact_number: 'සම්බන්ධතා අංකය ඉලක්කම් 10ක් විය යුතුය',
      address: 'ලිපිනය',
      enter_address: 'ලිපිනය ඇතුලත් කරන්න',
      invalid_address: 'ලිපිනය අවශ්‍යයි',
      subject: 'විෂය',
      enter_subject: 'විෂය ඇතුලත් කරන්න',
      invalid_subject: 'විෂය අවශ්‍යයි',
      education_level: 'අධ්‍යාපන මට්ටම',
      select_education_level: 'අධ්‍යාපන මට්ටම තෝරන්න',
      diploma: 'ඩිප්ලෝමා',
      degree: 'උපාධිය',
      masters: 'මාස්ටර්ස්',
      phd: 'පීඑච්ඩී',
      invalid_education_level: 'කරුණාකර අධ්‍යාපන මට්ටම තෝරන්න',
      add_teacher: 'ගුරුවරයා එක් කරන්න',
      drag_drop_csv: 'CSV ගොනුව මෙහි ඇද දමන්න',
      choose_file: 'ගොනුව තෝරන්න',
      cancel: 'අවලංගු කරන්න',
      import: 'ආයාත කරන්න',
      // AllTeachersComponent translations
      all_teachers : 'සියලුම ගුරුවරු',
      teacher_id: 'ගුරු අංකය',
      actions: 'ක්‍රියා',
      edit: 'සංස්කරණය',
      delete: 'මකන්න',
      confirm_delete: 'ඔබට මෙම ගුරුවරයා මැකීමට අවශ්‍ය බව විශ්වාසද?'
    }
  };

  private selectedLanguage: string = 'english';

  setLanguage(language: string): void {
    this.selectedLanguage = language;
  }

  getLanguage(): string {
    return this.selectedLanguage;
  }

  getTranslation(key: string): string {
    return this.translations[this.selectedLanguage][key] || key;
  }
}