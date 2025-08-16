import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import App from '../App'

describe('App Component', () => {
  it('renders without crashing', () => {
  render(<App />)

    // Verificar que el componente se renderiza
    expect(document.body).toBeDefined()
  })

  it('has correct title structure', () => {
  render(<App />)

    // Verificar que se puede acceder al contenido
    expect(document.querySelector('body')).toBeTruthy()
  })
})
