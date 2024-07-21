import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Page from './components/Page';
import NoPage from './components/NoPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/:csv" element={<Page />} />
        <Route path="*" element={<NoPage />} />
      </Routes>
    </Router>
  );
};

export default App;
