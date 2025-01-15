import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import json

def run_r_script(data: dict):
    """
    Pass data to R and retrieve the result.
    """
    jsonlite = importr("jsonlite")
    r_data = jsonlite.toJSON(data, auto_unbox=True)

    # Define R function
    ro.r("""
    process_data <- function(data) {
        library(jsonlite)
        parsed <- fromJSON(data)
        result <- list(sum = sum(unlist(parsed$values)))
        return(toJSON(result, auto_unbox=TRUE))
    }
    """)
    r_process_data = ro.globalenv['process_data']
    result = r_process_data(r_data)
    return json.loads(result[0])
