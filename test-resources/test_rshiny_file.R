library(shiny)
library(DT)
library(shinyjs)
library(shiny.semantic)
library(ggplot2)
library(dplyr)

ui <- fluidPage(
  useShinyjs(),
  extendShinyjs(text = "shinyjs.init = function() { console.log('ShinyJS Initialized!'); }", functions = c("init")),
  tags$head(
    tags$style(HTML("
      .custom-class {
        font-size: 16px;
        color: #2C3E50;
        background-color: #ECF0F1;
        padding: 10px;
        border-radius: 5px;
      }
      .box-style {
        background: #F7F9F9;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 20px;
      }
    "))
  ),
  div(id = "app-content",
      fluidRow(
        column(4, 
               box(id = "control-box", title = "Control Panel", solidHeader = TRUE, status = "primary", 
                   selectInput("data_choice", "Choose Dataset", choices = c("mtcars", "iris")),
                   sliderInput("n", "Number of Points", min = 1, max = 100, value = 30),
                   actionButton("go", "Generate Plot", class = "custom-class")
               )
        ),
        column(8,
               tabsetPanel(
                 tabPanel("Plot", plotOutput("plot_output", height = "600px")),
                 tabPanel("Table", DTOutput("table_output"))
               )
        )
      )
  )
)

server <- function(input, output, session) {
  
  values <- reactiveValues(data = NULL, plot_data = NULL)
  
  observe({
    req(input$data_choice)
    if (input$data_choice == "mtcars") {
      values$data <- mtcars
    } else {
      values$data <- iris
    }
  })
  
  observeEvent(input$go, {
    req(values$data)
    set.seed(123)
    sample_data <- values$data[sample(nrow(values$data), input$n), ]
    values$plot_data <- sample_data
  })
  
  output$plot_output <- renderPlot({
    req(values$plot_data)
    ggplot(values$plot_data, aes(x = Sepal.Length, y = Sepal.Width)) + 
      geom_point(aes(color = Species)) +
      theme_minimal() +
      labs(title = "Scatter Plot", x = "Sepal Length", y = "Sepal Width")
  })
  
  output$table_output <- renderDT({
    req(values$plot_data)
    datatable(values$plot_data, options = list(pageLength = 5))
  })
  
  observe({
    if (!is.null(values$plot_data)) {
      shinyjs::show("table_output")
    } else {
      shinyjs::hide("table_output")
    }
  })
  
  observe({
    shinyjs::runjs("console.log('App is running');")
  })
  
  outputOptions(output, "table_output", suspendWhenHidden = FALSE)
}

shinyApp(ui, server)
