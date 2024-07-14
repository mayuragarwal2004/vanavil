import React, { useState } from 'react';
import FullScreenModal from './FullScreenModal';

const Card = ({ image }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);

  const openModal = () => {
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  return (
    <div>
      <div className="card">
        <img src={image.image_url} alt={image.image_alt} onClick={openModal} />
        <h3>{image.image_alt}</h3>
        <h4>{image.article_title}</h4>
        <a href={image.article_url} target='_blank' rel="noopener noreferrer">Read More</a>
      </div>
      <FullScreenModal isOpen={modalIsOpen} onRequestClose={closeModal} image={image} />
    </div>
  );
};

export default Card;
