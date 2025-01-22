import './App.css'
import { PostageIncomeForm } from './components/PostageIncomeForm'
import { TooltipProvider } from '@/components/ui/tooltip'

function App() {
  return (
    <TooltipProvider>
      <div className="min-h-screen bg-gray-100 p-4">
        <PostageIncomeForm
          onSubmit={(data) => {
            console.log('Form submitted:', data);
          }}
        />
      </div>
    </TooltipProvider>
  )
}

export default App
