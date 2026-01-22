# TerraBoost Design System - Spacing System

## 📐 8PT GRID SYSTEM

모든 spacing은 **8의 배수**를 기준으로 합니다.
일관성 있는 레이아웃과 리듬을 만들기 위한 기본 원칙입니다.

---

## 🎯 SPACING SCALE

### Base Unit: 4px

| Token Name | Value | Common Use |
| --- | --- | --- |
| space-1 | 4px | Tight spacing, icon margins |
| space-2 | 8px | Small gaps, compact layouts |
| space-3 | 12px | Input padding, small margins |
| space-4 | 16px | Default padding, standard gaps |
| space-5 | 20px | Medium spacing |
| space-6 | 24px | Card padding, section spacing |
| space-8 | 32px | Large spacing, section gaps |
| space-10 | 40px | Extra large spacing |
| space-12 | 48px | Major section dividers |
| space-16 | 64px | Page-level spacing |
| space-20 | 80px | Maximum spacing |

---

## 📦 COMPONENT SPACING

### Buttons

**Padding (가로 × 세로):**

- Small: `12px × 8px` (space-3 × space-2)
- Medium (Default): `16px × 10px` (space-4 × space-3 미만)
- Large: `20px × 12px` (space-5 × space-3)

**Gap (아이콘 + 텍스트):**

- `8px` (space-2)

**Button Group Gap:**

- `8px` (space-2)

### Inputs & Text Fields

**Padding:**

- Horizontal: `12px` (space-3)
- Vertical: `10px`

**Height:**

- Default: `40px`

### Cards

**Padding:**

- Default: `24px` (space-6)
- Compact: `16px` (space-4)
- Spacious: `32px` (space-8)

**Gap between cards:**

- `16px` (space-4) - Grid layout
- `24px` (space-6) - List layout

### Tables

**Cell Padding:**

- Horizontal: `20px` (space-5)
- Vertical: `16px` (space-4)

**Row Height:**

- Compact: `48px` (space-12)
- Default: `64px` (space-16)
- Comfortable: `80px` (space-20)

### Lists

**Item Gap:**

- Tight: `8px` (space-2)
- Default: `12px` (space-3)
- Comfortable: `16px` (space-4)

**Item Padding:**

- `16px` (space-4)

### Badges / Tags

**Padding:**

- `8px × 4px` (space-2 × space-1)
- With icon: `6px × 4px` + icon

**Gap in badge group:**

- `8px` (space-2)

### Modals / Dialogs

**Padding:**

- Header: `24px` (space-6)
- Body: `24px` (space-6)
- Footer: `24px` (space-6)

**Gap between sections:**

- `16px` (space-4)

---

## 📱 LAYOUT SPACING

### Container

**Max Width:**

- Desktop: `1280px`
- Full width: `100%`

**Padding (좌우 여백):**

- Desktop (>1440px): `80px` (space-20)
- Tablet (768px-1439px): `40px` (space-10)
- Mobile (<768px): `20px` (space-5)

### Grid System

**Columns:**

- Desktop: 12 columns
- Tablet: 8 columns
- Mobile: 4 columns

**Gutter (컬럼 간격):**

- Desktop: `24px` (space-6)
- Tablet: `20px` (space-5)
- Mobile: `16px` (space-4)

### Page Layout

**Top Margin (헤더 아래):**

- `32px` (space-8)

**Section Gap (섹션 간격):**

- Small: `32px` (space-8)
- Default: `48px` (space-12)
- Large: `64px` (space-16)

**Content Max Width:**

- Full: `100%`
- Reading: `720px`
- Narrow: `560px`

---

## 🎨 SPECIFIC USE CASES

### Dashboard Layout

```
Page padding: 32px (space-8)
├─ Page title
├─ Gap: 16px (space-4)
├─ KPI Cards Row
│  ├─ Card padding: 24px (space-6)
│  └─ Gap between cards: 16px (space-4)
├─ Gap: 32px (space-8)
├─ Activity Card
│  ├─ Card padding: 24px (space-6)
│  ├─ Title
│  ├─ Gap: 16px (space-4)
│  └─ Table
│     └─ Row height: 64px
└─ Gap: 32px (space-8)

```

### PR Detail Page

```
Page padding: 32px (space-8)
├─ PR Header
│  └─ Padding: 24px (space-6)
├─ Gap: 16px (space-4)
├─ Tabs
├─ Gap: 24px (space-6)
├─ Content Section
│  ├─ Section padding: 24px (space-6)
│  └─ Item gap: 12px (space-3)
└─ Gap: 32px (space-8)

```

### Form Layout

```
Form container padding: 24px (space-6)
├─ Form field
├─ Gap: 16px (space-4)
├─ Form field
├─ Gap: 16px (space-4)
├─ Form field
├─ Gap: 24px (space-6)
└─ Button row
   └─ Button gap: 8px (space-2)

```

### Sidebar Navigation

```
Sidebar padding: 16px (space-4)
├─ Logo section
│  └─ Padding: 16px (space-4)
├─ Gap: 24px (space-6)
├─ Menu items
│  ├─ Item padding: 12px (space-3)
│  └─ Item gap: 4px (space-1)
└─ Gap: 32px (space-8)

```

---

## 📏 SPACING RULES

### Rule 1: 항상 8의 배수 사용

```
✅ Good: 8px, 16px, 24px, 32px
❌ Bad: 10px, 15px, 25px, 35px

```

### Rule 2: 작은 spacing은 4px 단위 허용

```
✅ Good: 4px, 12px (아주 좁은 공간에만)
❌ Bad: 2px, 6px, 14px

```

### Rule 3: 같은 레벨의 요소는 같은 spacing

```
✅ Good: 모든 카드 간격이 16px로 동일
❌ Bad: 어떤 카드는 16px, 어떤 카드는 20px

```

### Rule 4: 계층적 spacing

```
큰 섹션 > 중간 그룹 > 작은 요소
64px > 32px > 16px > 8px

```

### Rule 5: 여백은 넉넉하게

```
✅ Good: 충분한 breathing room
❌ Bad: 답답하게 꽉 찬 레이아웃

```

---

## 🎯 QUICK REFERENCE

### 자주 쓰는 Spacing

| Use Case | Spacing |
| --- | --- |
| 아이콘 + 텍스트 gap | 8px |
| 버튼 내부 padding | 16px × 10px |
| 카드 padding | 24px |
| 카드 간 gap | 16px |
| 섹션 간 gap | 32px |
| 테이블 row height | 64px |
| 페이지 좌우 padding | 32px (desktop) |
| Input height | 40px |
| Button height (medium) | 40px |

---

## 💡 FIGMA 적용 방법

### 옵션 1: Auto Layout Spacing

Figma Auto Layout 사용 시 spacing 값 직접 입력:

- Gap: 8, 16, 24, 32
- Padding: 24 (상하좌우 동일)
- Padding: 16, 24 (세로, 가로)

### 옵션 2: Manual Spacing

선택 요소 간격 조정 시:

- 우측 패널에서 X, Y 값을 8의 배수로 설정
- Cmd/Ctrl + 방향키로 1px씩 이동
- Shift + 방향키로 10px씩 이동

### 옵션 3: Spacing Variables (추천)

Variables로 등록하면 일관성 유지 쉬움:

```
space/1 = 4
space/2 = 8
space/3 = 12
space/4 = 16
space/6 = 24
space/8 = 32

```

---

## ⚠️ 주의사항

### Don't

- ❌ 임의의 spacing 값 사용 (9px, 13px, 27px...)
- ❌ 같은 컴포넌트에 다른 spacing 적용
- ❌ 너무 빽빽한 레이아웃
- ❌ 불규칙한 간격

### Do

- ✅ 8의 배수 spacing 일관되게 사용
- ✅ 계층 구조에 맞는 spacing
- ✅ 충분한 여백 확보
- ✅ 같은 타입 요소는 같은 spacing

---

## 📊 SPACING SCALE VISUAL

```
4px   ▪
8px   ▪▪
12px  ▪▪▪
16px  ▪▪▪▪
24px  ▪▪▪▪▪▪
32px  ▪▪▪▪▪▪▪▪
48px  ▪▪▪▪▪▪▪▪▪▪▪▪
64px  ▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪
80px  ▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪

```

이 spacing을 사용해서 리듬감 있고 일관된 레이아웃을 만드세요!