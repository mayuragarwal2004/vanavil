// /src/components/Page.jsx
import React, { useState, useEffect } from "react";
import Papa from "papaparse";
import Card from "./Card";
import Pagination from "./Pagination";
import Masonry from "react-masonry-css";
import "./Page.css";
import { useParams } from "react-router-dom";
import SearchBar from "./SearchBar";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

const csvFileMapping = {
  ncsu: "ncsu_processed_data.csv",
  stanford: "stanford_processed_data.csv",
};

const Page = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [itemsPerPage, setItemsPerPage] = useState(
    parseInt(localStorage.getItem("itemsPerPage")) || 50
  );
  const [searchQuery, setSearchQuery] = useState("");
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
            setFilteredData(result.data); // Initialize filteredData with full data
          },
        });
      })
      .catch((error) => {
        console.error("Error fetching and parsing CSV file:", error);
      });
  }, [csv]);

  useEffect(() => {
    localStorage.setItem("itemsPerPage", itemsPerPage);
  }, [itemsPerPage]);

  useEffect(() => {
    const filtered = data.filter(
      (item) =>
        item?.image_alt?.toLowerCase().includes(searchQuery?.toLowerCase()) ||
        item?.article_title
          ?.toLowerCase()
          .includes(searchQuery?.toLowerCase()) ||
        item?.article_url?.toLowerCase().includes(searchQuery?.toLowerCase()) ||
        item?.article_url?.toLowerCase().includes(searchQuery?.toLowerCase())
    );
    setFilteredData(filtered);
    setCurrentPage(0); // Reset to first page on new search
  }, [searchQuery, data]);

  const handlePageClick = (event) => {
    setCurrentPage(event.selected);
  };

  const handleItemsPerPageChange = (event) => {
    setItemsPerPage(parseInt(event.target.value));
    setCurrentPage(0); // Reset to first page
  };

  const handleSearchChange = (event) => {
    console.log("searching");
    console.log(event.target.value);
    setSearchQuery(event.target.value);
  };

  const offset = currentPage * itemsPerPage;
  const currentData = filteredData.slice(offset, offset + itemsPerPage);
  const pageCount = Math.ceil(filteredData.length / itemsPerPage);

  // Define breakpoints for masonry layout
  const breakpointColumnsObj = {
    default: 4,
    1100: 3,
    700: 2,
    500: 1,
  };

  return (
    <div className="Page">
      <h1>Image Gallery</h1>
      <div
        className="controls"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <label htmlFor="itemsPerPage">Items per page:</label>

        <FormControl style={{ width: "100px" }}>
          <Select
            labelId="itemsPerPage"
            id="itemsPerPage"
            value={itemsPerPage}
            onChange={handleItemsPerPageChange}
          >
            <MenuItem value={10}>10</MenuItem>
            <MenuItem value={20}>20</MenuItem>
            <MenuItem value={50}>50</MenuItem>
            <MenuItem value={100}>100</MenuItem>
          </Select>
        </FormControl>
      </div>
      <div className="controls">
        {/* <label htmlFor="search">Search:</label>
        <input
          id="search"
          type="text"
          
          placeholder="Search by title or alt text"
        /> */}
        <SearchBar value={searchQuery} onChange={handleSearchChange} />
      </div>
      <Masonry
        breakpointCols={breakpointColumnsObj}
        className="my-masonry-grid"
        columnClassName="my-masonry-grid_column"
      >
        {currentData.map((item, index) => (
          <Card key={index} image={item} />
        ))}
      </Masonry>
      <Pagination pageCount={pageCount} onPageChange={handlePageClick} />
    </div>
  );
};

export default Page;
