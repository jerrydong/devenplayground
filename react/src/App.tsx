import { HashRouter as Router, Routes, Route } from 'react-router-dom'
import { PolicyConfigForm } from './components/policy-config'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<PolicyConfigForm />} />
      </Routes>
    </Router>
  )
}

export default App
