// src/components/__tests__/Feed.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import Feed from '../Feed';

// Mock the articles data
jest.mock('/Users/aryantyagi/rap-news/src/data.js', () => [
  {
    title: 'Test Rap Article',
    author: 'u/testuser',
    source: { name: 'r/hiphopheads' },
    score: 100,
    age: '2 hours ago'
  }
], { virtual: true });

// Mock Card component
jest.mock('../Card.jsx', () => {
  return function MockCard({ articleData }) {
    return <div data-testid="article-card">{articleData.title}</div>;
  };
});

describe('Feed Component', () => {
  test('renders articles', () => {
    render(<Feed />);
    expect(screen.getByText('Test Rap Article')).toBeInTheDocument();
  });
});