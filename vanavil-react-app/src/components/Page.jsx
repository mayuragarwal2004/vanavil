
import React, { useState, useEffect } from "react";
import Papa from "papaparse";
import Card from "./Card";
import Pagination from "./Pagination";
import "./Page.css";
import { useParams } from "react-router-dom";

const csvFileMapping = {
        "ncsu": "ncsu_processed_data.csv",
        "stanford": "stanford_processed_data.csv",
    }

const Page = () => {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [itemsPerPage, setItemsPerPage] = useState(
    parseInt(localStorage.getItem("itemsPerPage")) || 50
  );
  const { csv } = useParams();

  useEffect(() => {
    fetch(`/data/${csvFileMapping[csv]}`)
      .then((response) => response.text())
      .then((text) => {
        Papa.parse(text, {
          header: true,
          dynamicTyping: true,
          complete: (result) => {
            setData(result.data);
          },
        });
      })
      .catch((error) => {
        console.error("Error fetching and parsing CSV file:", error);
      });
  }, []);

  useEffect(() => {
    localStorage.setItem("itemsPerPage", itemsPerPage);
  }, [itemsPerPage]);

  const handlePageClick = (event) => {
    setCurrentPage(event.selected);
  };

  const handleItemsPerPageChange = (event) => {
    setItemsPerPage(parseInt(event.target.value));
    setCurrentPage(0); // Reset to first page
  };

  const offset = currentPage * itemsPerPage;
  const currentData = data.slice(offset, offset + itemsPerPage);
  const pageCount = Math.ceil(data.length / itemsPerPage);

  return (
    <div className="Page">
      <h1>Image Gallery</h1>
      <div className="controls">
        <label htmlFor="itemsPerPage">Items per page:</label>
        <select
          id="itemsPerPage"
          value={itemsPerPage}
          onChange={handleItemsPerPageChange}
        >
          <option value={10}>10</option>
          <option value={20}>20</option>
          <option value={50}>50</option>
          <option value={100}>100</option>
        </select>
      </div>
      <div className="card-container">
        {currentData.map((item, index) => (
          <Card key={index} image={item} />
        ))}
      </div>
      <Pagination pageCount={pageCount} onPageChange={handlePageClick} />
    </div>
  );
};

export default Page;
