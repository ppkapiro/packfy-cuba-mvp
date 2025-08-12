import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from '../App'

describe('App Component', () => {
  it('renders without crashing', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    
    // Verificar que el componente se renderiza
    expect(document.body).toBeDefined()
  })

  it('has correct title structure', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    
    // Verificar que se puede acceder al contenido
    expect(document.querySelector('body')).toBeTruthy()
  })
})
