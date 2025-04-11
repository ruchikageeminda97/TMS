import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StuEnrollComponent } from './stu-enroll.component';

describe('StuEnrollComponent', () => {
  let component: StuEnrollComponent;
  let fixture: ComponentFixture<StuEnrollComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StuEnrollComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StuEnrollComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
