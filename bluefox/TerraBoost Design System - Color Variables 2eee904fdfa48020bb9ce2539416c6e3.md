# TerraBoost Design System - Color Variables

## 📋 Figma Variables 설정 가이드

### 1. Figma에서 Variables 패널 열기

- 우측 상단 Variables 아이콘 클릭 또는
- 단축키: Option + Shift + K (Mac) / Alt + Shift + K (Windows)

### 2. Collection 생성

- "Create collection" 클릭
- 이름: "TerraBoost Colors"

### 3. 아래 컬러들을 하나씩 추가

---

## 🎨 PRIMARY COLORS

**Name:** blue-400
**Value:** #3B82F6
**Description:** Hover state

**Name:** blue-500
**Value:** #2563EB
**Description:** Main primary color - buttons, links, key actions

**Name:** blue-600
**Value:** #1D4ED8
**Description:** Active/pressed state

**Name:** blue-700
**Value:** #1E40AF
**Description:** Dark variant

---

## ✅ SEMANTIC COLORS

**Name:** success
**Value:** #00C853
**Description:** Passed tests, completed status, positive actions

**Name:** success-light
**Value:** #00E676
**Description:** Positive trends, growth indicators

**Name:** warning
**Value:** #FFB020
**Description:** Caution, pending status, attention needed

**Name:** danger
**Value:** #EF4444
**Description:** Failed tests, errors, destructive actions

**Name:** info
**Value:** #00AFF4
**Description:** Information messages, tips, neutral notifications

---

## 🖼️ BACKGROUND & SURFACES

**Name:** bg-primary
**Value:** #0F1014
**Description:** Main application background

**Name:** bg-secondary
**Value:** #1A1C23
**Description:** Cards, sidebar, secondary surfaces

**Name:** bg-tertiary
**Value:** #24262E
**Description:** Hover states, subtle elevated surfaces

**Name:** bg-elevated
**Value:** #2D3039
**Description:** Modals, dropdowns, popovers

---

## 📝 TEXT COLORS

**Name:** text-primary
**Value:** #FAFAFA
**Description:** Headings, body text, main content

**Name:** text-secondary
**Value:** #A0A4B8
**Description:** Descriptions, labels, secondary content

**Name:** text-tertiary
**Value:** #6B7280
**Description:** Placeholder text, disabled text, supporting content

**Name:** text-accent
**Value:** #2563EB
**Description:** Links, interactive text, emphasized content

---

## 🔲 BORDER & UTILITIES

**Name:** border-subtle
**Value:** rgba(255, 255, 255, 0.04)
**Description:** Very subtle dividers, light separators

**Name:** border-default
**Value:** rgba(255, 255, 255, 0.08)
**Description:** Default borders, card outlines, input borders

**Name:** border-strong
**Value:** rgba(255, 255, 255, 0.12)
**Description:** Emphasized borders, active outlines

**Name:** focus-ring
**Value:** rgba(37, 99, 235, 0.4)
**Description:** Focus indicator for interactive elements

---

## 💡 사용 팁

1. **Collection 구조:**
    
    ```
    TerraBoost Colors/
    ├── Primary/
    │   ├── blue-400
    │   ├── blue-500 (main)
    │   ├── blue-600
    │   └── blue-700
    ├── Semantic/
    │   ├── success
    │   ├── success-light
    │   ├── warning
    │   ├── danger
    │   └── info
    ├── Background/
    │   ├── bg-primary
    │   ├── bg-secondary
    │   ├── bg-tertiary
    │   └── bg-elevated
    ├── Text/
    │   ├── text-primary
    │   ├── text-secondary
    │   ├── text-tertiary
    │   └── text-accent
    └── Border/
        ├── border-subtle
        ├── border-default
        ├── border-strong
        └── focus-ring
    
    ```
    
2. **Variable 이름 규칙:**
    - 소문자와 하이픈 사용 (kebab-case)
    - 명확하고 의미 있는 이름
    - 계층 구조를 슬래시(/)로 표현
3. **적용 방법:**
    - 컴포넌트 만들 때 직접 Hex 코드 대신 Variable 사용
    - 나중에 컬러 수정 시 Variable만 바꾸면 모든 곳에 자동 반영

---

## 📊 총 컬러 개수: 21개

- Primary: 4개
- Semantic: 5개
- Background: 4개
- Text: 4개
- Border: 4개

---

## ⚠️ 주의사항

1. **rgba 값 입력 시:**
    - Figma에서 rgba 입력할 때는 RGBA 형식으로 직접 입력
    - 예: rgba(255, 255, 255, 0.04)
2. **이름 중복 방지:**
    - 각 Variable 이름이 고유해야 함
    - Collection 내에서 같은 이름 사용 불가
3. **Mode 설정:**
    - 지금은 Dark 모드만 있음
    - 나중에 Light 모드 추가 가능