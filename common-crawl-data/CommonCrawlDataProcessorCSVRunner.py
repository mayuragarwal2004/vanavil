import csv
from CommonCrawlDataProcessor import CommonCrawlDataProcessor 

if __name__ == "__main__":
    search_query_csv_filename = input("Enter CSV file with the list of search queries: ")
    if not search_query_csv_filename:
        search_query_csv_filename = "search_queries_list.csv"
    csv_filename = input("Enter CSV filename (default: commoncrawl_preprocessed_data.csv): ")
    if not csv_filename:
        csv_filename = "commoncrawl_preprocessed_data.csv"

    mode = input("Enter mode (w for overwrite, a for append) [default: w]: ")
    if not mode:
        mode = "w"
        
    if mode == "w":
        with open(csv_filename, 'w', newline='') as file:
            pass
        
    
    with open(search_query_csv_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        records = list(reader)
        print(records)
        
        for item in records:
            search_query = item["search_query"]
            print(search_query)
            
            processor = CommonCrawlDataProcessor(search_query, csv_filename, "a")
            try:
                processor.process_data()
            except:
                pass
        

