import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleAggregatesComponent } from './article-aggregates.component';

describe('ArticleAggregatesComponent', () => {
  let component: ArticleAggregatesComponent;
  let fixture: ComponentFixture<ArticleAggregatesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ArticleAggregatesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleAggregatesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
