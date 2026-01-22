# TerraBoost Design System - Typography

## 🔤 FONT FAMILIES

### Primary Font (UI)

```
Font Family: Geist, Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif
Use: All UI text (headings, body, buttons, labels)

```

### Monospace Font (Code)

```
Font Family: "JetBrains Mono", "Fira Code", "SF Mono", Consolas, monospace
Use: Code blocks, terminal output, technical data

```

---

## 📏 FONT SCALE & HIERARCHY

### Display

- **Size:** 40px
- **Line Height:** 48px (1.2)
- **Weight:** 700 (Bold)
- **Use:** Hero sections, landing pages, major announcements

### Heading 1 (H1)

- **Size:** 32px
- **Line Height:** 40px (1.25)
- **Weight:** 700 (Bold)
- **Use:** Page titles, main headings

### Heading 2 (H2)

- **Size:** 24px
- **Line Height:** 32px (1.33)
- **Weight:** 700 (Bold)
- **Use:** Section titles, card titles

### Heading 3 (H3)

- **Size:** 20px
- **Line Height:** 28px (1.4)
- **Weight:** 600 (Semibold)
- **Use:** Sub-section titles, component headings

### Heading 4 (H4)

- **Size:** 18px
- **Line Height:** 24px (1.33)
- **Weight:** 600 (Semibold)
- **Use:** Small headings, emphasis titles

### Body Large

- **Size:** 16px
- **Line Height:** 24px (1.5)
- **Weight:** 400 (Regular)
- **Use:** Large paragraphs, important body text

### Body (Default)

- **Size:** 14px
- **Line Height:** 20px (1.43)
- **Weight:** 400 (Regular)
- **Use:** Default body text, descriptions, most UI text

### Body Small

- **Size:** 13px
- **Line Height:** 18px (1.38)
- **Weight:** 400 (Regular)
- **Use:** Supporting text, metadata, secondary information

### Caption

- **Size:** 12px
- **Line Height:** 16px (1.33)
- **Weight:** 500 (Medium)
- **Use:** Labels, tags, small UI elements, table headers

### Code

- **Size:** 14px
- **Line Height:** 20px (1.43)
- **Weight:** 400 (Regular)
- **Font:** Monospace
- **Use:** Inline code, code blocks, technical text

---

## ⚖️ FONT WEIGHTS

### Available Weights

- **400 (Regular):** Default body text
- **500 (Medium):** Emphasis, labels, captions
- **600 (Semibold):** Sub-headings, important UI elements
- **700 (Bold):** Headings, strong emphasis, key numbers

### Usage Guidelines

```
Headings (Display, H1, H2): 700 (Bold)
Sub-headings (H3, H4): 600 (Semibold)
Body text: 400 (Regular)
Emphasis/Labels: 500 (Medium)
Buttons: 600 (Semibold)
Numbers (KPI, metrics): 700 (Bold)

```

---

## 📐 LINE HEIGHT RULES

### Tight (1.2-1.3)

- Large text (Display, H1)
- When space is limited
- Short, impactful statements

### Normal (1.3-1.5)

- Headings (H2-H4)
- UI elements
- Most interface text

### Relaxed (1.5-1.6)

- Body text
- Long-form content
- Paragraphs

---

## 🎨 LETTER SPACING

### Default: 0 (Normal)

Most text uses default spacing

### Special Cases:

- **Uppercase labels:** +0.5px to +1px
    - Example: "TOTAL PULL REQUESTS" → 0.5px
- **Large headings (Display):** -0.5px
    - Makes large text feel tighter
- **Small text (Caption):** +0.2px
    - Improves readability at small sizes

---

## 📋 FIGMA TEXT STYLES 설정

### Style Naming Convention

```
Type/Size/Weight
예시:
- Heading/H1/Bold
- Body/Default/Regular
- Caption/Small/Medium

```

### 생성할 Text Styles (총 10개)

### 1. Display/40/Bold

- Font: Geist
- Weight: **Bold**
- Size: **40**
- Line height: **48** (Auto 말고 수동으로)
- Letter spacing: **0%**

### 2. Heading/H1/Bold

- Weight: **Bold**
- Size: **32**
- Line height: **40**
- Letter spacing: **0%**

### 3. Heading/H2/Bold

- Weight: **Bold**
- Size: **24**
- Line height: **32**
- Letter spacing: **0%**

### 4. Heading/H3/Semibold

- Weight: **SemiBold**
- Size: **20**
- Line height: **28**
- Letter spacing: **0%**

### 5. Heading/H4/Semibold

- Weight: **SemiBold**
- Size: **18**
- Line height: **24**
- Letter spacing: **0%**

### 6. Body/Large/Regular

- Weight: **Regular**
- Size: **16**
- Line height: **24**
- Letter spacing: **0%**

### 7. Body/Default/Regular

- Weight: **Regular**
- Size: **14**
- Line height: **20**
- Letter spacing: **0%**

### 8. Body/Small/Regular

- Weight: **Regular**
- Size: **13**
- Line height: **18**
- Letter spacing: **0%**

### 9. Caption/Small/Medium

- Weight: **Medium**
- Size: **12**
- Line height: **16**
- Letter spacing: **0.5%**

### 10. Code/Default/Regular

- Font: **JetBrains Mono** (또는 SF Mono)
- Weight: **Regular**
- Size: **14**
- Line height: **20**
- Letter spacing: **0%**

---

## 💡 USAGE EXAMPLES

### Dashboard Page

```
Page Title: H1 (32px/Bold)
Section Title: H2 (24px/Bold)
Card Title: H3 (20px/Semibold)
Card Description: Body Default (14px/Regular)
Labels: Caption (12px/Medium)
Large Numbers (KPI): Display (40px/Bold)
Small Numbers: H2 (24px/Bold)

```

### PR Detail Page

```
PR Title: H2 (24px/Bold)
Section Headers: H3 (20px/Semibold)
Code Comments: Body Default (14px/Regular)
Code Blocks: Code (14px/Regular, Monospace)
Metadata: Body Small (13px/Regular)
Status Labels: Caption (12px/Medium)

```

### Table

```
Table Headers: Caption (12px/Medium) + uppercase + letter-spacing
Row Content: Body Default (14px/Regular)
Row Numbers: Body Default (14px/Semibold)
Row Metadata: Body Small (13px/Regular)

```

---

## 🎯 HIERARCHY 원칙

1. **크기로 계층 표현**
    - 중요할수록 큰 사이즈
    - 4px 단위로 차이 (12, 16, 20, 24...)
2. **굵기로 강조**
    - 중요한 정보: Bold (700)
    - 일반 정보: Regular (400)
3. **컬러로 구분**
    - Primary text (#FAFAFA): 주요 내용
    - Secondary text (#A0A4B8): 보조 내용
    - Tertiary text (#6B7280): 부가 정보
4. **일관성 유지**
    - 같은 역할 = 같은 스타일
    - 예외는 최소화

---

## ⚠️ DON'T

❌ 한 화면에 너무 많은 폰트 크기 사용
❌ Body text에 Bold 남용
❌ 작은 텍스트(12px 이하)에 Regular 사용
❌ 긴 텍스트에 짧은 Line Height
❌ 대문자 + 작은 사이즈 + 좁은 Letter Spacing

---

## 📊 QUICK REFERENCE

| Element | Size | Weight | Color |
| --- | --- | --- | --- |
| Page Title | 32px | 700 | text-primary |
| Section Title | 24px | 700 | text-primary |
| Card Title | 20px | 600 | text-primary |
| Body Text | 14px | 400 | text-primary |
| Description | 14px | 400 | text-secondary |
| Label | 12px | 500 | text-secondary |
| Metadata | 13px | 400 | text-tertiary |
| Button Text | 14px | 600 | white |
| Link | 14px | 400 | text-accent |
| Number (Large) | 40px | 700 | text-primary |
| Number (Small) | 24px | 700 | text-primary |