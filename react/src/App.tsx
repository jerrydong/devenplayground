import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import VerbalPage from './pages/verbal'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<VerbalPage />} />
      </Routes>
    </Router>
  )
}

export default App
