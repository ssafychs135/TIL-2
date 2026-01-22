# TerraBoost Design System - Alignment & Layout

## 📐 정렬 원칙

### 기본 원칙

모든 정렬은 **시각적 균형**과 **읽기 편의성**을 최우선으로 합니다.

---

## 1️⃣ 체크박스 정렬

### 규칙

체크박스와 텍스트는 **중심선(centerline)** 기준으로 정렬합니다.

### 레이아웃

```
Row Height: 64px

┌─────────────────────────────────────┐
│                                     │
│  [✓] Main Text        [Badge]      │  ← 모두 y=20 중심선에 정렬
│      subtext                        │
│                                     │
└─────────────────────────────────────┘

상세 좌표:
- Checkbox: y=10, height=20 (중심: y=20)
- Main Text baseline: y=24 (14px 폰트의 중심이 y=20 근처)
- Badge: y=7, height=26 (중심: y=20)
- Subtext baseline: y=46

```

### 코드 예시

```
<g>
  <!-- Row container -->
  <rect width="584" height="64" rx="6" fill="#0F1014"/>

  <!-- Checkbox: 10-30, center at 20 -->
  <rect x="20" y="10" width="20" height="20" rx="4" fill="#2563EB"/>

  <!-- Main text: baseline at 24 -->
  <text x="56" y="24" font-size="14">PostgreSQL 14.x</text>

  <!-- Badge: 7-33, center at 20 -->
  <g transform="translate(200, 7)">
    <rect width="80" height="26" rx="4" fill="#2563EB" fill-opacity="0.2"/>
    <text x="40" y="18" text-anchor="middle">기본 DB</text>
  </g>

  <!-- Subtext -->
  <text x="56" y="46" font-size="13">localhost:5432</text>
</g>

```

### Spacing

- Checkbox left margin: 20px
- Checkbox to text gap: 16px (space-4)
- Text to badge gap: 유동적 (텍스트 길이에 따라)
- Main text to subtext: 22px

---

## 2️⃣ 테이블 정렬

### 규칙

- 헤더와 데이터는 **같은 X 좌표**를 공유
- 모든 텍스트는 **baseline** 기준 정렬
- 숫자는 **우측 정렬** 권장

### 테이블 구조

```
┌─────────┬──────────┬──────────┬─────┐
│ METHOD  │ API 경로  │ 소요시간  │ SQL │  ← Header (Caption 12px)
├─────────┼──────────┼──────────┼─────┤
│ [GET]   │ /api/... │ 1,245ms  │  12 │  ← Data row
│ x=0     │ x=80     │ x=240    │x=320│
└─────────┴──────────┴──────────┴─────┘

Row height: 40px (data), 48px (header)
Row gap: 48px

```

### 코드 예시

```
<!-- Header -->
<g>
  <text x="0" y="16" font-size="12" font-weight="600">METHOD</text>
  <text x="80" y="16" font-size="12" font-weight="600">API 경로</text>
  <text x="240" y="16" font-size="12" font-weight="600">소요시간</text>
  <text x="320" y="16" font-size="12" font-weight="600">SQL</text>
</g>

<!-- Data Row -->
<g transform="translate(0, 40)">
  <rect x="-12" y="-4" width="364" height="40" fill="#0F1014"/>

  <!-- Badge aligned to x=0 -->
  <rect x="0" y="4" width="44" height="20" rx="4" fill="#00C853"/>
  <text x="22" y="19" text-anchor="middle">GET</text>

  <!-- Text aligned to column x positions -->
  <text x="80" y="19">/api/users</text>
  <text x="240" y="19" font-weight="600">1,245ms</text>
  <text x="320" y="19">12</text>
</g>

```

---

## 3️⃣ 폼 필드 정렬

### Input Field

```
Label
└─ Input (40px height)

Label to Input gap: 8px (space-2)

```

### 코드 예시

```
<g>
  <!-- Label -->
  <text y="0" font-size="13" font-weight="500">테스트 API 엔드포인트</text>

  <!-- Input: label 아래 8px -->
  <rect y="8" width="576" height="40" rx="6" fill="#0F1014"/>
  <text x="12" y="34" font-size="14">https://api.example.com</text>
</g>

```

### 수평 필드 배치

```
[Field 1: 276px] [24px gap] [Field 2: 276px]

Total: 276 + 24 + 276 = 576px

```

### 필드 간 수직 간격

- Input to Input: 72px (전체 높이 포함)
- Input to Toggle: 96px
- Toggle to Toggle: 48px

---

## 4️⃣ 토글 스위치 정렬

### 규칙

- 토글은 항상 **우측 정렬**
- 텍스트와 토글은 **수직 중앙** 정렬

### 레이아웃

```
┌─────────────────────────────────────┐
│ Label text              [●─────]    │
│                         ^            │
│                      x=532           │
└─────────────────────────────────────┘

토글 높이: 24px
텍스트 baseline: y=16 (중앙 정렬)
토글 중심: y=16

```

### 코드 예시

```
<g>
  <!-- Text baseline at y=16 -->
  <text y="16" font-size="14">실패 시 자동 재시도</text>

  <!-- Toggle: y=4 (center at y=16) -->
  <g transform="translate(532, 4)">
    <rect width="44" height="24" rx="12" fill="#2563EB"/>
    <circle cx="32" cy="12" r="10" fill="#FFFFFF"/>
  </g>
</g>

```

---

## 5️⃣ 버튼 그룹 정렬

### 규칙

- 버튼은 **좌측부터** 배치
- Primary → Secondary → Ghost 순서
- 버튼 간 gap: 8px (space-2)

### 코드 예시

```
<g>
  <!-- Primary -->
  <rect width="140" height="48" rx="6" fill="#2563EB"/>
  <text x="70" y="31" text-anchor="middle">설정 저장</text>

  <!-- Secondary: 140 + 16 = 156 -->
  <g transform="translate(156, 0)">
    <rect width="160" height="48" rx="6" fill="none" stroke="#2D3139"/>
    <text x="80" y="31" text-anchor="middle">테스트 실행</text>
  </g>

  <!-- Ghost: 156 + 160 + 16 = 332 -->
  <g transform="translate(332, 0)">
    <text x="50" y="31" text-anchor="middle">취소</text>
  </g>
</g>

```

---

## 6️⃣ 카드 내부 Padding

### 규칙

모든 카드는 **24px (space-6)** padding 사용

```
┌─────────────────────────────┐
│ ← 24px                      │
│                             │
│  Content                    │
│                             │
│                      24px → │
└─────────────────────────────┘

```

### 예외

- 테이블 row: 12px horizontal padding
- 작은 카드/뱃지: 12px padding

---

## 7️⃣ 아이콘-텍스트 정렬

### 규칙

아이콘과 텍스트는 **수직 중앙** 정렬

### 20px 아이콘 예시

```
Icon: y=0, height=20 (center at y=10)
Text baseline: y=14 (14px 폰트)

```

### 16px 아이콘 예시

```
Icon: y=2, height=16 (center at y=10)
Text baseline: y=14 (14px 폰트)

```

---

## 📏 정렬 체크리스트

페이지 완성 후 다음을 확인하세요:

- [ ]  체크박스-텍스트-뱃지가 같은 중심선에 있는가?
- [ ]  테이블 헤더와 데이터 컬럼이 정확히 정렬되었는가?
- [ ]  폼 필드 간 간격이 8의 배수인가?
- [ ]  토글이 우측 정렬되고 텍스트와 중앙 정렬되었는가?
- [ ]  모든 카드 padding이 24px인가?
- [ ]  버튼 그룹 순서와 간격이 올바른가?

---

## 🎯 핵심 좌표 참조표

| 요소 | 기준 Y | 비고 |
| --- | --- | --- |
| Checkbox (20px) | y=10 | 중심 y=20 |
| Main Text (14px) | y=24 | baseline |
| Badge (26px) | y=7 | 중심 y=20 |
| Subtext (13px) | y=46 | baseline |
| Toggle (24px) | y=4 | 중심 y=16 |
| Toggle Label (14px) | y=16 | baseline |
| Table Header (12px) | y=16 | baseline |
| Table Data (13-14px) | y=19 | baseline |
| Button Text (14-16px) | y=26-31 | middle |

---

## 💡 실전 팁

1. **먼저 중심선을 정하라**: 모든 요소의 중심 Y 좌표를 먼저 정하고, 거기서부터 계산
2. **baseline을 이해하라**: 텍스트는 baseline 기준, 도형은 center 기준
3. **8pt grid를 지켜라**: 모든 Y 좌표는 8의 배수가 되도록
4. **일관성이 핵심**: 같은 패턴은 항상 같은 좌표 사용

---

이 문서는 TerraBoost UI의 정렬 일관성을 보장하기 위한 필수 가이드입니다.