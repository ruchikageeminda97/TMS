import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { LanguageService } from '../language.service'; // Import service

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private router: Router, public languageService: LanguageService) {} // Inject service

  getTranslation(key: string): string {
    return this.languageService.getTranslation(key);
  }

  onSubmit() {
    if (this.username && this.password) {
      console.log('Login attempted with:', { username: this.username, password: this.password });
      this.router.navigate(['/dashboard']);
    }
  }
}