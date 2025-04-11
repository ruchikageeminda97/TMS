import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ClassLanguageService {
  private selectedLanguage: string = 'english';

  private translations: any = {
    english: {
      add_new_lass: 'Add New Class',
      class_name: 'Class Name',
      enter_class_name: 'Enter class name',
      invalid_class_name: 'Please enter a valid class name (letters and numbers only).',
      teacher_id: 'Teacher ID',
      enter_teacher_id: 'Enter teacher ID',
      invalid_teacher_id: 'Please enter a valid teacher ID (letters and numbers only).',
      teacher_name: 'Teacher Name',
      enter_teacher_name: 'Enter teacher name',
      invalid_teacher_name: 'Please enter a valid teacher name (letters only).',
      subject: 'Subject',
      enter_subject: 'Enter subject',
      invalid_subject: 'Please enter a valid subject (letters only).',
      date: 'Date',
      invalid_date: 'Please select a valid date.',
      start_time: 'Start Time',
      invalid_start_time: 'Please select a valid start time.',
      end_time: 'End Time',
      invalid_end_time: 'Please select a valid end time.',
      fee: 'Fee',
      enter_fee: 'Enter fee (LKR)',
      invalid_fee: 'Please enter a valid fee (positive number).',
      add_class: 'Add Class',
      class_added_success: 'Class added successfully!',
      fill_all_fields: 'Please fill all fields.',
      // Optional import translations
      import_class_list: 'Import Class List',
      drag_drop_csv: 'Drag and drop your CSV file here or click to upload.',
      choose_file: 'Choose File',
      cancel: 'Cancel',
      import: 'Import'
    },
    sinhala: {
      add_new_class: 'නව පන්තියක් එකතු කරන්න',
      class_name: 'පන්තියේ නම',
      enter_class_name: 'පන්තියේ නම ඇතුලත් කරන්න',
      invalid_class_name: 'කරුණාකර වලංගු පන්තියේ නමක් ඇතුලත් කරන්න (අකුරු සහ ඉලක්කම් පමණි).',
      teacher_id: 'ගුරුවරයාගේ හැඳුනුම් අංකය',
      enter_teacher_id: 'ගුරුවරයාගේ හැඳුනුම් අංකය ඇතුලත් කරන්න',
      invalid_teacher_id: 'කරුණාකර වලංගු ගුරුවරයාගේ හැඳුනුම් අංකයක් ඇතුලත් කරන්න (අකුරු සහ ඉලක්කම් පමණි).',
      teacher_name: 'ගුරුවරයාගේ නම',
      enter_teacher_name: 'ගුරුවරයාගේ නම ඇතුලත් කරන්න',
      invalid_teacher_name: 'කරුණාකර වලංගු ගුරුවරයාගේ නමක් ඇතුලත් කරන්න (අකුරු පමණි).',
      subject: 'විෂය',
      enter_subject: 'විෂය ඇතුලත් කරන්න',
      invalid_subject: 'කරුණාකර වලංගු විෂයක් ඇතුලත් කරන්න (අකුරු පමණි).',
      date: 'දිනය',
      invalid_date: 'කරුණාකර වලංගු දිනයක් තෝරන්න.',
      start_time: 'ආරම්භක වේලාව',
      invalid_start_time: 'කරුණාකර වලංගු ආරම්භක වේලාවක් තෝරන්න.',
      end_time: 'අවසන් වේලාව',
      invalid_end_time: 'කරුණාකර වලංගු අවසන් වේලාවක් තෝරන්න.',
      fee: 'ගාස්තුව',
      enter_fee: 'ගාස්තුව ඇතුලත් කරන්න (LKR)',
      invalid_fee: 'කරුණාකර වලංගු ගාස්තුවක් ඇතුලත් කරන්න (ධන ඉලක්කමක්).',
      add_class: 'පන්තිය එකතු කරන්න',
      class_added_success: 'පන්තිය සාර්ථකව එකතු කරන ලදී!',
      fill_all_fields: 'කරුණාකර සියලුම ක්ෂේත්‍ර පුරවන්න.',
      // Optional import translations
      import_class_list: 'පන්ති ලැයිස්තුව ආයාත කරන්න',
      drag_drop_csv: 'ඔබේ CSV ගොනුව මෙහි ඇද දමන්න හෝ උඩුගත කිරීමට ක්ලික් කරන්න.',
      choose_file: 'ගොනුව තෝරන්න',
      cancel: 'අවලංගු කරන්න',
      import: 'ආයාත කරන්න'
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