
linear_regression <- function(data, formula) {
  model <- lm(formula, data = data)
  summary_stats <- summary(model)
  
  coefficients <- summary_stats$coefficients
  r_squared <- summary_stats$r.squared
  p_value <- summary_stats$fstatistic[1]
  
  return(list(coefficients = coefficients, r_squared = r_squared, p_value = p_value))
}

standardize <- function(x) {
  mean_x <- mean(x, na.rm = TRUE)
  sd_x <- sd(x, na.rm = TRUE)
  standardized_x <- (x - mean_x) / sd_x
  return(standardized_x)
}

k_means_clustering <- function(data, centers = 3, max_iter = 100) {
  set.seed(42)
  result <- kmeans(data, centers = centers, iter.max = max_iter)
  
  return(list(cluster_centers = result$centers, cluster_assignments = result$cluster, total_within_ss = result$tot.withinss))
}

correlation_matrix <- function(data) {
  num_cols <- sapply(data, is.numeric)
  numeric_data <- data[, num_cols]
  corr_matrix <- cor(numeric_data, use = "complete.obs")
  
  return(corr_matrix)
}
