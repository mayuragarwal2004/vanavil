import React, { useState, useEffect } from 'react';
import WordCloud from 'react-wordcloud';
import { removeStopwords } from 'stopword';
import Papa from 'papaparse';
import csvFileMapping from '../csvFileMapping.json';
import { useParams } from 'react-router-dom';

const WordCloudComponent = ({ onWordClick }) => {
  const [words, setWords] = useState([]);
  const [scale, setScale] = useState(1);
  const { csv } = useParams();

  useEffect(() => {
    fetch(`/data/${csvFileMapping[csv]}`)
      .then((response) => response.text())
      .then((text) => {
        Papa.parse(text, {
          header: true,
          dynamicTyping: true,
          complete: (result) => {
            const titles = result.data.map(item => item.article_title).join(' ');
            const filteredWords = removeStopwords(titles.split(' '));
            const wordCount = filteredWords.reduce((acc, word) => {
              acc[word] = (acc[word] || 0) + 1;
              return acc;
            }, {});
            const wordArray = Object.keys(wordCount).map(word => ({
              text: word,
              value: wordCount[word],
            }));
            setWords(wordArray);
          },
        });
      })
      .catch((error) => {
        console.error("Error fetching and parsing CSV file:", error);
      });
  }, [csv]);

  const handleZoomIn = () => {
    setScale(scale + 0.1);
  };

  const handleZoomOut = () => {
    setScale(scale - 0.1);
  };

  const handleResetZoom = () => {
    setScale(1);
  };

  const handleWordClick = (word) => {
    onWordClick(word);
  };

  return (
    <div style={{ height: '400px', width: '300px', overflow: 'auto' }}>
      <div style={{ transform: `scale(${scale})`, transformOrigin: '0 0' }}>
        <WordCloud words={words} onWordClick={handleWordClick} />
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
        <button onClick={handleZoomIn}>Zoom In</button>
        <button onClick={handleZoomOut}>Zoom Out</button>
        <button onClick={handleResetZoom}>Reset Zoom</button>
      </div>
    </div>
  );
};

export default WordCloudComponent;
