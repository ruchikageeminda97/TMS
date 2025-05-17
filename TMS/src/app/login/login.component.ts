import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { LanguageService } from '../language.service';
import { ApiService } from '../api_services/services';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, MatSnackBarModule,NgIf],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  regUsername: string = '';
  regPassword: string = '';
  regEmail: string = '';
  showRegisterForm: boolean = false;

  constructor(
    private router: Router,
    public languageService: LanguageService,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

  private showSnackBar(message: string, action: string = 'Close', duration: number = 3000): void {
    this.snackBar.open(message, action, { duration, verticalPosition: 'bottom' });
  }

  onSubmit() {
    if (this.showRegisterForm) {
      // Handle registration
      if (this.regUsername && this.regPassword && this.regEmail) {
        this.apiService.register({
          username: this.regUsername,
          password: this.regPassword,
          role: 'Admin',
          email: this.regEmail
        }).subscribe({
          next: (response) => {
            if (response && response.message === 'Registration successful') {
              localStorage.setItem('username', this.regUsername);
              this.showSnackBar(this.getTranslation('register_success'));
              this.router.navigate(['/dashboard']);
            } else {
              this.showSnackBar(this.getTranslation('register_failed'));
            }
          },
          error: (err) => {
            console.error('Registration error:', err);
            this.showSnackBar(this.getTranslation('register_failed'));
          }
        });
      } else {
        this.showSnackBar(this.getTranslation('register_failed'));
      }
    } else {
      // Handle login
      if (this.username && this.password) {
        this.apiService.login({ username: this.username, password: this.password }).subscribe({
          next: (response) => {
            if (response && response.message === 'Login successful') {
              localStorage.setItem('username', this.username);
              this.router.navigate(['/dashboard']);
            } else {
              this.showSnackBar(this.getTranslation('login_failed'));
            }
          },
          error: (err) => {
            console.error('Login error:', err);
            this.showSnackBar(this.getTranslation('login_failed'));
          }
        });
      } else {
        this.showSnackBar(this.getTranslation('login_failed'));
      }
    }
  }

  showLogin(): void {
    this.showRegisterForm = false;
    this.regUsername = '';
    this.regPassword = '';
    this.regEmail = '';
  }

  showRegister(): void {
    this.showRegisterForm = true;
    this.username = '';
    this.password = '';
  }
}