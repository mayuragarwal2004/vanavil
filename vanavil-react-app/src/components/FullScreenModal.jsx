// /src/components/FullScreenModal.jsx

import React from 'react';
import Modal from 'react-modal';

Modal.setAppElement('#root');

function getDomainName(url) {
  try {
    const parsedUrl = new URL(url);
    return parsedUrl.origin;
  } catch (error) {
    console.log("Invalid URL:", url);
    console.error("Invalid URL:", error);
    return null;
  }
}

const FullScreenModal = ({ isOpen, onRequestClose, image }) => {
  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      style={{
        content: {
          top: '50%',
          left: '50%',
          right: 'auto',
          bottom: 'auto',
          marginRight: '-50%',
          transform: 'translate(-50%, -50%)',
          maxWidth: '90%',
          maxHeight: '90%',
          padding: 0,
          overflow: 'hidden',
        },
        overlay: {
          backgroundColor: 'rgba(0, 0, 0, 0.75)',
        },
      }}
    >
      <img src={image?.image_url?.startsWith("http")
              ? image.image_url
              : `${getDomainName(image.article_url)}${image.image_url}`} alt={image.image_alt} style={{ width: '100%', height: '100%' }} />
    </Modal>
  );
};

export default FullScreenModal;
