import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Page from './components/Page';
import NoPage from './components/NoPage';
import WordCloudComponent from './components/WordCloud';
import HNLinksViewer from './components/HNLinksViewer';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/hnlink" element={<HNLinksViewer />} />
        <Route path="/wordcloud/:csv" element={<WordCloudComponent />} />
        <Route path="/:csv" element={<Page />} />
        <Route path="*" element={<NoPage />} />
      </Routes>
    </Router>
  );
};

export default App;
