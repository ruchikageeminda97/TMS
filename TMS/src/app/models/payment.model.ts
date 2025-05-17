export interface Payment {
  payment_id: string;
  student_id: string;
  class_id: string;
  amount: number;
  payment_date: string;
  month: string;
  year: string;
  status: string;
}