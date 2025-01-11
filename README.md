# SPSearchReverseEng
An attempt to reverse engineer SharePoint Online Search using known variables 
# Page Ranking System

This project contains a Dash application designed to evaluate and display the ranking of web pages based on various metrics. The application allows users to input details about web pages and calculates scores for relevance, freshness, and user interaction to determine a final ranking score.

## Key Components

### 1. Dash Application
The main application is built using the Dash framework with Bootstrap components for styling. Dash is a productive Python framework for building web applications, and it is particularly suited for data visualization.

### 2. User Inputs
Users can input details about web pages, including:
- **Titles**: The title of the web page.
- **Headings**: The main headings of the web page.
- **First Paragraphs**: The introductory paragraphs of the web page.
- **Body Text**: The main content of the web page.
- **Views**: The number of views the web page has received.
- **Shares**: The number of times the web page has been shared.
- **Likes**: The number of likes the web page has received.
- **Comments**: The number of comments on the web page.
- **Known Page Ranking Positions**: The known ranking position of the web page.
- **Ages**: The age of the web page in days.
- **Keywords for Ranking Prediction**: Keywords used to predict the ranking of the web page.

### 3. Callbacks
The application uses Dash callbacks to dynamically add input fields for multiple pages and to update the results based on user inputs. Callbacks are functions that are automatically called by Dash whenever an input component's property changes.

### 4. Scoring Functions
The application includes several functions to calculate different scores:

#### TF-IDF and TF Scores
- **TF-IDF (Term Frequency-Inverse Document Frequency)**: Measures the importance of a keyword in a document relative to a collection of documents.
- **TF (Term Frequency)**: Measures how frequently a keyword appears in a document.

#### Relevance Score
Uses fuzzy matching and TF-IDF scores to calculate the relevance of the content to the search terms. The relevance score is calculated using the following formula:
\[ R = T \cdot k_t + H \cdot k_h + P \cdot k_p + B \cdot k_b + M \cdot k_m + \text{tfidf\_score} + \text{tf\_score} \]
where \( k_t, k_h, k_p, k_b, k_m \) are the match scores for title, headings, first paragraph, body text, and metadata respectively.

#### Freshness Score
Calculates how recent the content is based on its age using the formula:
\[ F_s = \frac{F}{A} \]
where \( F \) is a freshness constant and \( A \) is the age of the page in days.

#### User Interaction Score
Calculates user engagement based on views, shares, likes, and comments using the formula:
\[ U = V \cdot v + S \cdot s + L \cdot l + C \cdot c \]
where \( V, S, L, C \) are the weights for views, shares, likes, and comments respectively, and \( v, s, l, c \) are the respective counts.

#### Final Ranking Score
Combines relevance, freshness, and user interaction scores to determine the final ranking score for each page using the formula:
\[ F_r = \alpha \cdot R + \beta \cdot C + \gamma \cdot F_s + \delta \cdot U + \text{personalised} \]
where \( \alpha, \beta, \gamma, \delta \) are the weights for relevance, content, freshness, and user interaction scores respectively, and \( \text{personalised} \) is a constant personalization factor.

### 5. Results Display
The application displays detailed results for each page, including all calculated scores and the final ranking score. The results are displayed in a structured format, making it easy to compare the performance of different pages.

## Running the Application
To run the application, execute the script and open the provided URL in a web browser. The application will be accessible at  port 8052

## Dependencies
- Dash
- Dash Bootstrap Components
- NumPy
- Scikit-learn
- FuzzyWuzzy


Ensure all dependencies are installed before running the application.

