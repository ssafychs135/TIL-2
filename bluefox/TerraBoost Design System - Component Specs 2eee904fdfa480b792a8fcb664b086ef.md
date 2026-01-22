# TerraBoost Design System - Component Specs

## 🎯 BUTTONS

### Sizes

| Size | Height | Padding (H×V) | Font Size | Font Weight | Border Radius |
| --- | --- | --- | --- | --- | --- |
| Small | 32px | 12px × 8px | 13px | 600 (Semibold) | 6px |
| Medium | 40px | 16px × 10px | 14px | 600 (Semibold) | 6px |
| Large | 48px | 20px × 12px | 16px | 600 (Semibold) | 6px |

### Variants

**Primary Button**

- Background: `blue-500` (#2563EB)
- Text: White (#FFFFFF)
- Hover: `blue-600` (#1D4ED8)
- Active: `blue-700` (#1E40AF)
- Disabled: Opacity 50%

**Secondary Button**

- Background: Transparent
- Border: 1px solid `border-default` (rgba(255,255,255,0.08))
- Text: `text-primary` (#FAFAFA)
- Hover: Background `bg-tertiary` (#24262E)
- Active: Background `bg-elevated` (#2D3039)
- Disabled: Opacity 50%

**Ghost Button**

- Background: Transparent
- Text: `text-accent` (#2563EB)
- Hover: Background rgba(37,99,235,0.08)
- Active: Background rgba(37,99,235,0.12)
- Disabled: Opacity 50%

**Danger Button**

- Background: `danger` (#EF4444)
- Text: White (#FFFFFF)
- Hover: Darken 10%
- Active: Darken 20%
- Disabled: Opacity 50%

### Icon + Text

- Icon size: 16px (Small), 20px (Medium/Large)
- Gap: 8px (space-2)
- Icon position: Left or Right

### States

- Default: Base styles
- Hover: Background change + cursor pointer
- Active/Pressed: Darker background
- Focus: Focus ring (3px, rgba(37,99,235,0.4))
- Disabled: Opacity 50% + cursor not-allowed
- Loading: Spinner + disabled state

---

## 📝 INPUTS & TEXT FIELDS

### Default Input

| Property | Value |
| --- | --- |
| Height | 40px |
| Padding | 12px (horizontal) |
| Font Size | 14px |
| Font Weight | 400 (Regular) |
| Border Radius | 6px |
| Border | 1px solid `border-default` |
| Background | rgba(255,255,255,0.03) |

### States

**Default:**

- Border: rgba(255,255,255,0.08)
- Background: rgba(255,255,255,0.03)
- Text: `text-primary`

**Hover:**

- Border: rgba(255,255,255,0.12)

**Focus:**

- Border: 2px solid `blue-500` (#2563EB)
- Shadow: 0 0 0 3px rgba(37,99,235,0.2)

**Error:**

- Border: 2px solid `danger` (#EF4444)
- Shadow: 0 0 0 3px rgba(239,68,68,0.2)

**Disabled:**

- Opacity: 50%
- Cursor: not-allowed

### With Icon

- Icon size: 16px
- Icon position: Left or Right
- Padding adjustment: 36px (icon side)
- Icon color: `text-tertiary`

### Label

- Font size: 13px
- Font weight: 500 (Medium)
- Color: `text-secondary`
- Margin bottom: 8px

### Helper Text / Error Message

- Font size: 12px
- Font weight: 400 (Regular)
- Color: `text-tertiary` (helper) or `danger` (error)
- Margin top: 4px

---

## 🗂️ CARDS

### Default Card

| Property | Value |
| --- | --- |
| Padding | 24px (space-6) |
| Border Radius | 8px |
| Background | `bg-secondary` (#1A1C23) |
| Border | 1px solid `border-default` |
| Shadow | None (flat design) |

### Variants

**Compact Card:**

- Padding: 16px (space-4)

**Spacious Card:**

- Padding: 32px (space-8)

**Interactive Card (Clickable):**

- Hover: Background `bg-tertiary` (#24262E)
- Cursor: pointer
- Transition: background 0.2s ease

### Card Header

- Margin bottom: 16px (space-4)
- Title: H3 (20px, Semibold)
- Description: Body Small (13px, Regular, `text-secondary`)

### Card Content

- Default spacing

### Card Footer

- Margin top: 16px (space-4)
- Border top: 1px solid `border-subtle`
- Padding top: 16px

---

## 🏷️ BADGES / TAGS

### Size

| Property | Value |
| --- | --- |
| Height | 26px |
| Padding | 8px × 4px |
| Font Size | 12px |
| Font Weight | 700 (Bold) |
| Border Radius | 4px |

### Variants

**Success Badge:**

- Background: `success` (#00C853)
- Text: Black (#000000)

**Info Badge:**

- Background: `blue-500` (#2563EB)
- Text: White (#FFFFFF)

**Warning Badge:**

- Background: `warning` (#FFB020)
- Text: Black (#000000)

**Danger Badge:**

- Background: `danger` (#EF4444)
- Text: White (#FFFFFF)

**Neutral Badge:**

- Background: `bg-tertiary` (#24262E)
- Border: 1px solid `border-default`
- Text: `text-primary`

### With Icon

- Icon size: 12px
- Gap: 4px

---

## 📊 TABLES

### Table Container

| Property | Value |
| --- | --- |
| Background | `bg-secondary` (#1A1C23) |
| Border | 1px solid `border-default` |
| Border Radius | 8px |
| Padding | 0 (rows have padding) |

### Table Header

| Property | Value |
| --- | --- |
| Height | 48px |
| Padding | 20px (horizontal), 16px (vertical) |
| Font Size | 12px |
| Font Weight | 600 (Semibold) |
| Text Transform | Uppercase |
| Letter Spacing | 0.5px |
| Color | `text-tertiary` (#6B7280) |
| Background | rgba(255,255,255,0.02) |
| Border Bottom | 2px solid `border-default` |

### Table Row

| Property | Value |
| --- | --- |
| Height | 64px |
| Padding | 20px (horizontal), 16px (vertical) |
| Font Size | 14px |
| Font Weight | 400 (Regular) |
| Border Bottom | 1px solid `border-subtle` |

**Hover State:**

- Background: rgba(37,99,235,0.06)
- Cursor: pointer

**Selected State:**

- Background: rgba(37,99,235,0.12)

### Table Cell

- Vertical align: middle
- Text overflow: ellipsis (긴 텍스트 처리)

---

## 🎨 ICONS

### Sizes

| Size | Dimension | Use Case |
| --- | --- | --- |
| XSmall | 12px × 12px | Inline, small badges |
| Small | 16px × 16px | Buttons, inputs, list items |
| Medium | 20px × 20px | Sidebar, navigation |
| Large | 24px × 24px | Section icons, emphasis |
| XLarge | 32px × 32px | Hero sections, empty states |

### Style

- Stroke width: 2px (Medium weight)
- Corner radius: 1px
- Color: Inherit from parent or specific color

### Repository Icons (Circular)

- Size: 36px × 36px
- Border radius: 50% (circle)
- Background: Varies by repo
- Text: 13px, Bold, White
- Center aligned

---

## 📋 MODALS / DIALOGS

### Modal Container

| Property | Value |
| --- | --- |
| Max Width | 640px (medium), 800px (large) |
| Border Radius | 12px |
| Background | `bg-elevated` (#2D3039) |
| Border | 1px solid `border-default` |
| Shadow | 0 8px 32px rgba(0,0,0,0.6) |

### Modal Header

- Padding: 24px
- Border bottom: 1px solid `border-subtle`
- Title: H2 (24px, Bold)

### Modal Body

- Padding: 24px
- Max height: 60vh (scrollable)

### Modal Footer

- Padding: 24px
- Border top: 1px solid `border-subtle`
- Button alignment: Right
- Button gap: 8px

### Backdrop

- Background: rgba(0,0,0,0.75)
- Backdrop blur: 4px (optional)

---

## 📱 DROPDOWN / SELECT

### Dropdown Trigger

| Property | Value |
| --- | --- |
| Height | 40px |
| Padding | 12px |
| Border Radius | 6px |
| Border | 1px solid `border-default` |
| Background | rgba(255,255,255,0.03) |

### Dropdown Menu

| Property | Value |
| --- | --- |
| Border Radius | 8px |
| Background | `bg-elevated` (#2D3039) |
| Border | 1px solid `border-default` |
| Shadow | 0 4px 16px rgba(0,0,0,0.5) |
| Padding | 4px |
| Max height | 320px (scrollable) |

### Dropdown Item

- Height: 36px
- Padding: 8px 12px
- Font size: 14px
- Border radius: 4px
- Hover: Background `bg-tertiary`
- Selected: Background rgba(37,99,235,0.12)

---

## 🔘 CHECKBOX / RADIO

### Checkbox

| Property | Value |
| --- | --- |
| Size | 20px × 20px |
| Border Radius | 4px |
| Border | 2px solid `border-default` |
| Background (unchecked) | Transparent |
| Background (checked) | `blue-500` (#2563EB) |
| Checkmark color | White |

### Radio

| Property | Value |
| --- | --- |
| Size | 20px × 20px |
| Border Radius | 50% (circle) |
| Border | 2px solid `border-default` |
| Background (unchecked) | Transparent |
| Inner circle (checked) | 10px, `blue-500` |

### Label

- Font size: 14px
- Gap: 8px
- Vertical align: center

---

## 🔀 SWITCH / TOGGLE

### Switch

| Property | Value |
| --- | --- |
| Width | 44px |
| Height | 24px |
| Border Radius | 12px (pill) |
| Background (off) | `bg-tertiary` (#24262E) |
| Background (on) | `blue-500` (#2563EB) |

### Switch Handle

- Size: 20px × 20px
- Border radius: 50% (circle)
- Background: White
- Position (off): Left (2px offset)
- Position (on): Right (2px offset)
- Transition: 0.2s ease

---

## 📑 TABS

### Tab Container

- Border bottom: 1px solid `border-subtle`
- Gap: 0 (tabs touch)

### Tab Item

| Property | Value |
| --- | --- |
| Height | 44px |
| Padding | 12px 16px |
| Font Size | 14px |
| Font Weight | 500 (Medium) |
| Color (inactive) | `text-secondary` |
| Color (active) | `text-accent` (#2563EB) |
| Border bottom (active) | 2px solid `blue-500` |

**Hover (inactive):**

- Color: `text-primary`
- Background: rgba(255,255,255,0.04)

---

## 📊 PROGRESS BAR

### Container

| Property | Value |
| --- | --- |
| Height | 8px |
| Border Radius | 4px |
| Background | `bg-tertiary` (#24262E) |

### Progress Fill

- Height: 8px (same as container)
- Border radius: 4px
- Background: `blue-500` (#2563EB)
- Transition: width 0.3s ease

### Variants

- Success: `success` (#00C853)
- Warning: `warning` (#FFB020)
- Danger: `danger` (#EF4444)

---

## 🎯 TOOLTIP

### Container

| Property | Value |
| --- | --- |
| Padding | 8px 12px |
| Border Radius | 6px |
| Background | #000000 |
| Color | White |
| Font Size | 13px |
| Font Weight | 400 (Regular) |
| Max Width | 240px |
| Shadow | 0 2px 8px rgba(0,0,0,0.4) |

### Arrow

- Size: 6px
- Color: #000000

---

## 💬 TOAST / NOTIFICATION

### Container

| Property | Value |
| --- | --- |
| Min Width | 320px |
| Max Width | 480px |
| Padding | 16px |
| Border Radius | 8px |
| Border | 1px solid `border-default` |
| Background | `bg-elevated` (#2D3039) |
| Shadow | 0 4px 16px rgba(0,0,0,0.5) |

### Variants

- Success: Left border 3px solid `success`
- Warning: Left border 3px solid `warning`
- Danger: Left border 3px solid `danger`
- Info: Left border 3px solid `blue-500`

### Content

- Icon: 20px × 20px
- Title: 14px, Semibold
- Message: 13px, Regular
- Gap: 12px

---

## 📐 DIVIDER / SEPARATOR

### Horizontal

| Property | Value |
| --- | --- |
| Height | 1px |
| Background | `border-subtle` or `border-default` |
| Margin | 16px or 24px (top & bottom) |

### Vertical

| Property | Value |
| --- | --- |
| Width | 1px |
| Background | `border-subtle` or `border-default` |
| Height | 100% or specific |
| Margin | 16px (left & right) |

---

## 🎨 CODE BLOCK

### Container

| Property | Value |
| --- | --- |
| Padding | 16px |
| Border Radius | 6px |
| Background | #161B22 (GitHub dark) |
| Border | 1px solid rgba(255,255,255,0.06) |
| Font | JetBrains Mono, monospace |
| Font Size | 14px |
| Line Height | 20px |
| Color | #C9D1D9 |

### Inline Code

- Padding: 2px 6px
- Border radius: 4px
- Background: rgba(255,255,255,0.08)
- Font: JetBrains Mono, monospace
- Font size: 13px
- Color: `text-accent`

---

## 📊 SUMMARY

**Total Components Defined: 16**

1. Buttons (4 variants, 3 sizes)
2. Inputs & Text Fields
3. Cards (3 variants)
4. Badges / Tags (5 variants)
5. Tables
6. Icons (5 sizes)
7. Modals / Dialogs
8. Dropdown / Select
9. Checkbox / Radio
10. Switch / Toggle
11. Tabs
12. Progress Bar
13. Tooltip
14. Toast / Notification
15. Divider / Separator
16. Code Block

---

이제 이 Specs를 기반으로 Figma에서 실제 컴포넌트를 만들 준비가 됐습니다!