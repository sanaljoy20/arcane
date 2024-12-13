# Linear Regression, Standardization, K-Means Clustering, and Correlation Matrix functions.

 #' Perform linear regression on the given data.
 #'
 #' @param data The data frame containing the variables for regression.
 #' @param formula The formula specifying the regression model.
 #'
 #' @return A list containing coefficients, R-squared value, and p-value.
 #'
linear_regression <- function(data, formula) {
  model <- lm(formula, data = data)
  summary_stats <- summary(model)
  
  coefficients <- summary_stats$coefficients
  r_squared <- summary_stats$r.squared
  p_value <- summary_stats$fstatistic[1]
  
  return(list(coefficients = coefficients, r_squared = r_squared, p_value = p_value))
}

 #' Standardize the input vector.
 #'
 #' @param x Numeric vector to be standardized.
 #'
 #' @return Standardized numeric vector.
 #'
standardize <- function(x) {
  mean_x <- mean(x, na.rm = TRUE)
  sd_x <- sd(x, na.rm = TRUE)
  standardized_x <- (x - mean_x) / sd_x
  return(standardized_x)
}

 #' Perform K-means clustering on the data.
 #'
 #' @param data The data frame containing the data points.
 #' @param centers Number of clusters to form.
 #' @param max_iter Maximum number of iterations.
 #'
 #' @return A list containing cluster centers, cluster assignments, and total within SS.
 #'
k_means_clustering <- function(data, centers = 3, max_iter = 100) {
  set.seed(42)
  result <- kmeans(data, centers = centers, iter.max = max_iter)
  
  return(list(cluster_centers = result$centers, cluster_assignments = result$cluster, total_within_ss = result$tot.withinss))
}

 #' Calculate the correlation matrix.
 #'
 #' @param data Data frame containing numeric variables.
 #'
 #' @return Correlation matrix of the numeric variables.
 #'
correlation_matrix <- function(data) {
  num_cols <- sapply(data, is.numeric)
  numeric_data <- data[, num_cols]
  corr_matrix <- cor(numeric_data, use = "complete.obs")
  
  return(corr_matrix)
}

