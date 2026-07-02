import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App.jsx';

describe('App component', () => {
  it('renders the heading', () => {
    render(<App />);
    expect(screen.getByText('SonarCloud CI/CD Demo')).toBeInTheDocument();
  });

  it('starts with count 0', () => {
    render(<App />);
    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: 0');
  });

  it('increments the count when button is clicked', () => {
    render(<App />);
    const button = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(button);
    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: 1');
  });
});
