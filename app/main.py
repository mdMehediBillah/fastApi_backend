from fastapi import FastAPI, HTTPException, Query, Depends
import pandas as pd
import os

app = FastAPI()

# Old_File path which shows error when running the tests
# =====================================================
# FILE_PATH = "./uploads/TestData.xlsx"

# After running the tests -> resolve the file path dynamically based on the current file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
FILE_PATH = os.path.join(BASE_DIR, "..", "uploads", "TestData.xlsx")  


# Load the data only once and share across the app
# This function will be called by other routes to access the data
# =====================================================
# =====================================================
# Here we are using the openpyxl engine to read the Excel file
# This is because the default engine (xlrd) does not support the latest Excel file format
# The openpyxl engine is slower but more reliable for newer Excel files
# The convert_dtypes() method is used to convert mixed data types to a single data type
# This is useful for columns with mixed data types (e.g., float and int)
# The RAND() values are replaced with fixed values to ensure consistent results
# The data is returned as a DataFrame object
# If an error occurs, an HTTP 500 error is raised with the error message

def load_data():
    if not os.path.exists(FILE_PATH):
        raise HTTPException(status_code=404, detail="File not found in uploads folder")

    try:
        # Load the Excel file using the openpyxl engine
        df = pd.read_excel(FILE_PATH, sheet_name=0, engine="openpyxl")

        # Use strip() to remove leading/trailing or whitespaces from column names
        df.columns = df.columns.str.strip()

        # Converts mixed types (e.g., float/int)
        df = df.convert_dtypes()  

        # Replace RAND() values with a fixed snapshot
        for col in df.columns:
            if df[col].dtype == 'float64':  # Check numeric columns
                df[col] = df[col].astype(float)  # Force evaluation

        return df

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")







# load data and convert float columns to string to avoid rounding issues
# =====================================================
# def load_data():
#     if not os.path.exists(FILE_PATH):
#         raise HTTPException(status_code=404, detail="File not found in uploads folder")

#     try:
#         # Load the Excel file, ensuring data types are preserved correctly
#         df = pd.read_excel(FILE_PATH, sheet_name=0, engine="openpyxl")

#         # Ensure column names have no leading/trailing spaces
#         df.columns = df.columns.str.strip()

#         # Convert float columns to string to avoid rounding issues
#         for col in df.select_dtypes(include=['float64']).columns:
#             df[col] = df[col].apply(lambda x: f"{x:.10f}" if pd.notnull(x) else x)

#         return df

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")





# load data without using openpyxl engine
# =====================================================
# def load_data():
#     if not os.path.exists(FILE_PATH):
#         raise HTTPException(status_code=404, detail="File not found in uploads folder")
#     try:
#         df = pd.read_excel(FILE_PATH)
#         return df
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")
    
    

# Reusable function to filter data by country code
def filter_by_country(df, country_code: str):
    if "ISOTwoLetterCountryCode" not in df.columns:
        raise HTTPException(status_code=500, detail="Missing 'CountryCode' column in dataset")
    return df[df["ISOTwoLetterCountryCode"].astype(str).str.upper() == country_code.upper()]

# Reusable function to handle empty data
def handle_empty_data(df):
    if df.empty:
        raise HTTPException(status_code=404, detail="No matching data found")
    return df



# Routes
# ====================================================================================================
# =====================================================

# Home route =========================================
# =====================================================
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}



# test data
# =====================================================
# check if the given number is odd or even
# The route parameter {number} is used to pass an integer value
@app.get("/test/{number}")
def test(number: int = 0):
    given_number = number ** 2
    is_odd = given_number % 2 != 0
    return {"number": given_number, "is_odd": is_odd}


# Get all data from the Excel file =========================================
# =========================================================================
# The load_data() function is used to load the Excel file
# The data is converted to a dictionary and returned as a JSON response
# Headers are extracted from the DataFrame columns

@app.get("/data")
def get_all_data(df: pd.DataFrame = Depends(load_data)):
    try:
        data_row = df.to_dict(orient="records")  # Convert dataframe to dictionary
        data_col = df.columns.tolist()
        
        # Debugging: Print first 2 rows in terminal
        # print("Sample Data:", data_row[:2])

        response = {"headers": data_col, "data": data_row}
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")



# Get data by country ISO code =========================================
# =========================================================================
# The route parameter {country_code} is used to filter data by country code (e.g., "US". "DE", "GB")
# The filter_by_country() function is used to filter the data by country code
# Modify url path as needed (e.g., /data/country/US) to filter data by country code

@app.get("/data/country/{country_code}")
def get_data_by_country(country_code: str, df: pd.DataFrame = Depends(load_data)):
    try:
        filtered_df = filter_by_country(df, country_code)
        handle_empty_data(filtered_df)
        return filtered_df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    



# Filtering data based on parameters or query parameters =========================================
# ================================================================================================
# Appended to the URL after a ? symbol.
# The query parameter is defined as a function argument with a default value of None.
# The Query function is used to define the query parameter and provide additional metadata.
# The query parameter is optional and can be used to filter data by country code.
# Modify the URL path as needed (e.g., /data/country?country_code=US) to filter data by country code.
@app.get("/data/country")
def filter_data(country_code: str = Query(..., description="Filter by ISO country code"), df: pd.DataFrame = Depends(load_data)):
    """
    Fetch data based on the given country_code query parameter.
    Example: /data/country?country_code=de
    """
    try:
        df = filter_by_country(df, country_code)
        handle_empty_data(df)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    


# Search data by country name or ISO code =========================================
# =================================================================================
# The query parameter is used to search data by country name or ISO code.
# The query parameter is defined as a function argument with a default value of None.
# The Query function is used to define the query parameter and provide additional metadata.
# The query parameter is optional and can be used to search data by country name or ISO code.
@app.get("/data/search")
def search_data(query: str, df: pd.DataFrame = Depends(load_data)):
    try:
        iso_match = df[df["ISOTwoLetterCountryCode"].astype(str).str.upper() == query.upper()]
        country_match = df[df["country"].astype(str).str.lower() == query.lower()]

        # check input query against country name and ISO code
        if not iso_match.empty:
            return iso_match.to_dict(orient="records")
        elif not country_match.empty:
            return country_match.to_dict(orient="records")
        raise HTTPException(status_code=404, detail="No matching data found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    


# Get data by process name =========================================
# ================================================================
# The route parameter {process_name} is used to filter data by process name
# Modify the URL path as needed (e.g., /data/process/ProcessName) to filter data by process name
# The process name is case-insensitive and will match any case
# Filter data by process name and return as JSON response
# The handle_empty_data() function is used to check if the data is empty
# An HTTP 404 error is raised if no matching data is found
@app.get("/data/process/{process_name}")
def get_data_by_process(process_name: str, df: pd.DataFrame = Depends(load_data)):
    try:
        filtered_df = df[df["processName"].astype(str).str.lower() == process_name.lower()]
        handle_empty_data(filtered_df)
        return filtered_df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    




# Aggregating GWP data by country =========================================
# =========================================================================
# Agrregating data by country code
# The route parameter {country_code} is used to filter data by country code (e.g., "US". "DE", "GB")
# Aggregating GWP data by columns for a specific country
# Total GWP100 is calculated as the sum of all GWP columns
# The result is returned as a JSON response with the total GWP100 value
# Modify the URL path as needed (e.g., /data/gwp/aggregate/US) to aggregate GWP data by country code
@app.get("/data/gwp/aggregate/{country_code}")
def get_gwp_aggregate_by_country(country_code: str, df: pd.DataFrame = Depends(load_data)):
    try:
        country_data = filter_by_country(df, country_code)
        handle_empty_data(country_data)
        
        gwp_columns = [
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change - global warming potential (GWP100) [kg CO2-Eq]",
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change: biogenic emissions - global warming potential (GWP100) [kg CO2-Eq]",
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change: biogenic removal - global warming potential (GWP100) [kg CO2-Eq]",
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change: fossil - global warming potential (GWP100) [kg CO2-Eq]",
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change: land use - global warming potential (GWP100) [kg CO2-Eq]"
        ]

        country_data[gwp_columns] = country_data[gwp_columns].apply(pd.to_numeric, errors="coerce").fillna(0)
        country_data[gwp_columns] = country_data[gwp_columns].astype(float)

        gwp_sums = country_data[gwp_columns].sum().to_dict()
        total_gwp = sum(gwp_sums.values())

        return {
            "country": country_data["country"].iloc[0],
            "total_GWP100": round(total_gwp, 2),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    

    

# Aggregating data by country and returning additional statistics =========================================
# ========================================================================================================
# The route parameter {country_code} is used to filter data by country code (e.g., "US". "DE", "GB")
# Aggregating GWP data by columns for a specific country
# Total GWP100 is calculated as the sum of all GWP columns
# The result is returned as a JSON response with the total GWP100 value
# Modify the URL path as needed (e.g., /data/gwp/aggregate/US) to aggregate GWP data by country code
# Additional statistics such as min and max GWP100 values are calculated
# The result also includes the column-wise total GWP100 values
@app.get("/data/aggregate/{country_code}")
def get_aggregate_by_country(country_code: str, df: pd.DataFrame = Depends(load_data)):
    try:
        country_data = filter_by_country(df, country_code)
        handle_empty_data(country_data)

        country_name = country_data["country"].values[0]

        # select columns for aggregation
        gwp_columns = [
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change - global warming potential (GWP100) [kg CO2-Eq]",
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change: biogenic emissions - global warming potential (GWP100) [kg CO2-Eq]",
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change: biogenic removal - global warming potential (GWP100) [kg CO2-Eq]",
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change: fossil - global warming potential (GWP100) [kg CO2-Eq]",
            "Carbon Minds ISO 14067 (based on IPCC 2021) - climate change: land use - global warming potential (GWP100) [kg CO2-Eq]"
        ]


        gwp_sums = country_data[gwp_columns].sum().to_dict()
        total_gwp = sum(gwp_sums.values())
        min_gwp = min(gwp_sums.values())
        max_gwp = max(gwp_sums.values())

        gwp_sums = {key: round(value, 2) for key, value in gwp_sums.items()}

        return {
            "country": country_name,
            "total_GWP100": round(total_gwp, 2),
            "min_GWP100": round(min_gwp, 2),
            "max_GWP100": round(max_gwp, 2),
            "total_GWP100_by_column": gwp_sums
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    


# Search for process names =========================================
# ================================================================
#  Users can search for process names using the /data/process_names/search endpoint
# The search query looks for process names that start with the specified query string
# The process names are returned as a list of strings
@app.get("/data/process_names/search")
def get_process_names(
    query: str = Query(None, description="Search for process names"),
    df: pd.DataFrame = Depends(load_data),
):
    try:
        if "processName" not in df.columns:
            raise HTTPException(status_code=500, detail="Missing 'processName' column in dataset")

        process_names = df["processName"].dropna().unique().tolist()

        if query:

            # The following code can be used to filter process names containing the query string
            # The process name can contain the query string anywhere in the name
            # =====================================================
            # filtered_names = [name for name in process_names if query.lower() in name.lower()]

            # The following code filters process names starting with the query string
            # The process look letter from the start of the process name
            # =====================================================
            filtered_names = [name for name in process_names if name.lower().startswith(query.lower())]

            if not filtered_names:
                return {"message": "No Process Name found"}  # Return message when no match is found
            
        else:
            filtered_names = process_names  

        return {"process_names": filtered_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")