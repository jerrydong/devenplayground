# Postage Income Form Implementation Plan

## Component Structure
```
PostageIncomeForm/
├── index.tsx              # Main form component
├── ConfigurationModule/   # Module 1: Configuration Info
├── DisplayLogicModule/    # Module 2: Package Display Logic
└── EffectiveDimensions/  # Module 3: Effective Dimensions
```

## Technology Stack
- React Hook Form for form state management
- Zod for form validation
- shadcn/ui components for UI elements
- Tailwind CSS for styling

## Module Implementation Details

### 1. Configuration Info Module
Components needed:
- Card wrapper from @/components/ui/card
- Form components from @/components/ui/form
- Input with tooltip for strategy name
- Checkbox group for fulfillment nodes
- Radio group for management line options
- Conditional radio group for pricing plan

### 2. Package Display Logic Module
Components needed:
- Card wrapper
- Form components
- Radio groups and checkboxes based on prototype

### 3. Effective Dimensions Module
Components needed:
- Card wrapper
- Form components
- Custom city selection component using mockCityApi
- Version selection with comparison operators
- Number selection for rider ID
- Role selection radio group

## Data Flow
1. Form state managed by react-hook-form
2. Zod schema for validation
3. City data fetched from mockCityApi
4. Form submission handler to be implemented

## Implementation Steps
1. Create base form component with react-hook-form setup
2. Implement each module as a separate component
3. Add form validation using Zod
4. Implement conditional rendering logic
5. Add city selection functionality
6. Add version comparison functionality
7. Implement form submission
8. Add proper TypeScript types

## Component API
```typescript
interface PostageIncomeFormProps {
  onSubmit: (data: PostageIncomeFormData) => void;
  initialData?: PostageIncomeFormData;
}
```

## Form Data Structure
```typescript
interface PostageIncomeFormData {
  configuration: {
    strategyName: string;
    fulfillmentNodes: string[];
    managementLine: string;
    pricingPlan?: string;
  };
  displayLogic: {
    // To be defined based on prototype
  };
  effectiveDimensions: {
    appVersion: {
      isGrayscale: boolean;
      cities?: Array<{type: string; city: string}>;
    };
    cityRange: {
      isGrayscale: boolean;
      systems: string[];
      comparison: string;
      versions: string[];
    };
    riderNumber: {
      isGrayscale: boolean;
      restrictionType: string;
      numbers: number[];
    };
    displayRole: string;
  };
}
```
