export interface Clas {
    ClassID:String;
    className: string;
    teacherID: string;
    teacherName: string;
    date: string;
    time: string;
    subject: string;
    fee: number ;
    student:string[];
  }  

  export interface Class {
  class_id: string;
  class_name: string;
  subject_id: string;
  day: string;
  start_time: string;
  end_time: string;
  room_number: string;
  capacity: number;
  status: string;
}