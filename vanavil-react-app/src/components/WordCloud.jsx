// /src/components/WordCloud.jsx
import React, { useEffect, useState } from 'react';
import WordCloud from 'react-wordcloud';
import {removeStopwords} from 'stopword';
import Papa from 'papaparse';
import csvFileMapping from '../csvFileMapping.json';
import { useParams } from 'react-router-dom';

const WordCloudComponent = () => {
  const [words, setWords] = useState([]);
  const { csv } = useParams();

  useEffect(() => {
    fetch(`/data/${csvFileMapping[csv]}`)
      .then((response) => response.text())
      .then((text) => {
        Papa.parse(text, {
          header: true,
          dynamicTyping: true,
          complete: (result) => {
            console.log(result.data.length);
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

  return (
    <div style={{ height: 400, width: 600 }}>
      <WordCloud words={words} />
    </div>
  );
};

export default WordCloudComponent;
