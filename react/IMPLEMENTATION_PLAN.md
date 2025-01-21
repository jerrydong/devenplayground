# Implementation Plan for Verbal Management System

## 1. Component Structure
```
App.tsx
├── SearchForm.tsx (Filter Component)
└── VerbalTable.tsx (Table Component with Actions)
    ├── DatasetDialog.tsx (Bind Dataset Modal)
    ├── OwnerDialog.tsx (Modify Owner Modal)
    ├── ImportDialog.tsx (Import Learning City Verbal Modal)
    └── VerbalDialog.tsx (Add/Edit Verbal Modal)
```

## 2. Feature Implementation Details

### 2.1 Search Form Implementation
- Create form with input fields:
  - Script Name (话术名称)
  - Script Content (话术内容)
  - Dataset (数据集)
  - Creator (创建人)
  - Owner (负责人)
- Use react-hook-form for form handling
- Implement search functionality using verbalQuery API
- Add debounce to search to prevent excessive API calls

### 2.2 Table Implementation
- Use shadcn/ui Table component
- Default display 50 records per page
- Implement pagination using verbalQuery API
- Add checkbox column for row selection
- Display columns:
  - Selection checkbox
  - Script Name
  - Script Content
  - Dataset
  - Creator
  - Owner
  - Actions (Edit button)
- Implement cross-page selection:
  - Add header checkbox for cross-page selection
  - When enabled, select all checkboxes in the first column
  - Track selected state for pagination

### 2.3 Action Buttons Implementation
1. Bind Dataset Button:
   - Disabled by default
   - Enabled when rows are selected
   - Opens DatasetDialog
   - Uses verbalGetSuggestDataset and verbalBatchModifyDataset APIs
   - Handles both single and cross-page selection cases

2. Modify Owner Button:
   - Disabled by default
   - Enabled when rows are selected
   - Opens OwnerDialog
   - Uses verbalGetSuggest and verbalBatchModifyOwner APIs
   - Handles both single and cross-page selection cases

3. Import Learning City Verbal Button:
   - Always enabled
   - Opens ImportDialog
   - Uses importXcVerbal API
   - Implements link input and dataset/owner selection

4. Add Verbal Button:
   - Always enabled
   - Opens VerbalDialog in create mode
   - Uses verbalAdd API
   - Implements form for name, content, dataset, and owner

### 2.4 Edit Functionality
- Share VerbalDialog component between Add and Edit operations
- Use type prop to distinguish between modes
- In edit mode:
  - Disable name field
  - Pre-fill form with existing data
  - Use verbalModify API for updates
  - Validate changes before submission

### 2.5 Dialog Components
1. DatasetDialog:
   - Dataset selection dropdown
   - Load options from verbalGetSuggestDataset API
   - Submit using verbalBatchModifyDataset API

2. OwnerDialog:
   - Owner selection dropdown with search
   - Load options from verbalGetSuggest API
   - Submit using verbalBatchModifyOwner API

3. ImportDialog:
   - Link input field
   - Dataset and owner selection
   - Submit using importXcVerbal API

4. VerbalDialog:
   - Form for verbal details
   - Name validation using verbalIsNameValid API
   - Dataset and owner selection
   - Content list management
   - Submit using verbalAdd or verbalModify API

## 3. State Management
- Use React useState for local component state
- Implement custom hooks for shared logic:
  - useVerbalQuery: Handle table data and pagination
  - useSelection: Manage row selection state
  - useDialog: Control dialog open/close states

## 4. Error Handling
- Implement error boundaries for component error handling
- Add error states for API calls
- Show appropriate error messages to users
- Implement loading states for async operations

## 5. Testing Strategy
- Test form validation
- Test table functionality
- Test dialog operations
- Test API integration
- Test error handling

## 6. Implementation Order
1. Set up base components and routing
2. Implement table with pagination
3. Add search form and filtering
4. Implement selection functionality
5. Add action buttons and dialogs
6. Implement error handling
7. Add loading states
8. Test and refine UI/UX
