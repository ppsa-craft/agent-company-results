import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Mock fetch
global.fetch = vi.fn();

describe('Web UI App', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('renders loading state initially', () => {
    (fetch as any).mockImplementation(() => new Promise(() => {}));
    
    render(<App />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders error state on fetch failure', async () => {
    (fetch as any).mockRejectedValue(new Error('Network error'));
    
    render(<App />);
    await vi.waitFor(() => {
      expect(screen.getByText('Error: Network error')).toBeInTheDocument();
    });
  });

  it('renders health data on success', async () => {
    const mockHealth = {
      status: 'healthy',
      service: 'suggestion-api',
      version: '0.1.0',
      timestamp: '2024-01-15T10:00:00Z',
    };
    
    (fetch as any).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockHealth),
    });
    
    render(<App />);
    await vi.waitFor(() => {
      expect(screen.getByText('vnstock Advisor')).toBeInTheDocument();
      expect(screen.getByText('Service Health')).toBeInTheDocument();
    });
  });
});