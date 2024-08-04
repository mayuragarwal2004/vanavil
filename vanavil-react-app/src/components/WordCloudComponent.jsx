// /src/components/WordCloudComponent.jsx
import React, { useEffect, useState } from 'react';
import WordCloud from 'react-wordcloud';
import { removeStopwords } from 'stopword';

const WordCloudComponent = ({ data, onWordClick }) => {
  const [words, setWords] = useState([]);

  useEffect(() => {
    if (!data) return;
    const titles = data.map(item => item.article_title).join(' ');
    const filteredWords = removeStopwords(titles.split(' '));
    const wordCount = filteredWords.reduce((acc, word) => {
      acc[word] = (acc[word] || 0) + 1;
      return acc;
    }, {});
    const wordArray = Object.keys(wordCount).map(word => ({
      text: word,
      value: wordCount[word],
    }));
    console.log(wordArray);
    setWords(wordArray);
  }, [data]);

  const options = {
    enableTooltip: true,
    deterministic: false,
    fontSizes: [15, 60],
    rotations: 2,
    rotationAngles: [-90, 0],
    scale: 'sqrt',
    spiral: 'archimedean',
    transitionDuration: 1000,
  };

  const callbacks = {
    onWordClick: (word) => {
      onWordClick(word.text);
    },
  };

  return (
    <div style={{ height: 400, width: '100%' }}>
      <WordCloud words={words} options={options} callbacks={callbacks} />
    </div>
  );
};

export default WordCloudComponent;
