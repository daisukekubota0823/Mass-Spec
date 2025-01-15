compute_mean <- function(values) {
    if (length(values) == 0) {
        stop("Values list cannot be empty")
    }
    return(mean(values))
}