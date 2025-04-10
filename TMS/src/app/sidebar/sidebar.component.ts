import { NgClass } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive,NgClass],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css'
})
export class SidebarComponent {
  isStudentsOpen: boolean = false; // Track submenu state

  toggleStudentsSubmenu(): void {
    this.isStudentsOpen = !this.isStudentsOpen;
  }
}