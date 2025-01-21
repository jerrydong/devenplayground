import './App.css'
import { useRef } from 'react'
import { SearchForm } from './components/verbal/SearchForm'
import { VerbalTable, type VerbalTableRef } from './components/verbal/VerbalTable'

function App() {
  const verbalTableRef = useRef<VerbalTableRef>(null);

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">话术管理系统</h1>
      <div className="space-y-6">
        <SearchForm onSearch={(values) => verbalTableRef.current?.fetchVerbals(values)} />
        <VerbalTable ref={verbalTableRef} />
      </div>
    </div>
  )
}

export default App
