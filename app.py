import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz


# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Page Ranking Decoder"),
            html.Button('Add Page', id='add-page-button', n_clicks=0),
            html.Div(id='page-inputs-container'),
            html.Button('Submit', id='submit-val', n_clicks=0)
        ], width=4),
        dbc.Col([
            html.H2("Predicted Results"),
            html.Div(id='results')
        ], width=8)
    ])
])

# Callback to add new page input fields
@app.callback(
    Output('page-inputs-container', 'children'),
    Input('add-page-button', 'n_clicks'),
    State('page-inputs-container', 'children')
)
def add_page_inputs(n_clicks, children):
    if children is None:
        children = []
    new_page = html.Div([
        html.H3(f"Page {n_clicks + 1}"),
        html.Label("Title:"),
        dcc.Input(id={'type': 'title', 'index': n_clicks}, type='text', value=''),
        html.Label("Headings:"),
        dcc.Input(id={'type': 'headings', 'index': n_clicks}, type='text', value=''),
        html.Label("First Paragraph:"),
        dcc.Input(id={'type': 'first_paragraph', 'index': n_clicks}, type='text', value=''),
        html.Label("Body Text:"),
        dcc.Textarea(id={'type': 'body_text', 'index': n_clicks}, value='', style={'width': '100%', 'height': 200}),
        html.Label("Views:"),
        dcc.Input(id={'type': 'views', 'index': n_clicks}, type='number', value=0),
        html.Label("Shares:"),
        dcc.Input(id={'type': 'shares', 'index': n_clicks}, type='number', value=0),
        html.Label("Likes:"),
        dcc.Input(id={'type': 'likes', 'index': n_clicks}, type='number', value=0),
        html.Label("Comments:"),
        dcc.Input(id={'type': 'comments', 'index': n_clicks}, type='number', value=0),
        html.Label("Known Page Ranking Position:"),
        dcc.Input(id={'type': 'position', 'index': n_clicks}, type='number', value=0),
        html.Label("Age of the Page (days):"),
        dcc.Input(id={'type': 'age', 'index': n_clicks}, type='number', value=0),
        html.Label("Keyword for Ranking Prediction:"),
        dcc.Input(id={'type': 'keyword', 'index': n_clicks}, type='text', value='')
    ])
    children.append(new_page)
    return children

# Define the callback to update the results
@app.callback(
    Output('results', 'children'),
    Input('submit-val', 'n_clicks'),
    State({'type': 'title', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'headings', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'first_paragraph', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'body_text', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'views', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'shares', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'likes', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'comments', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'position', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'age', 'index': dash.dependencies.ALL}, 'value'),
    State({'type': 'keyword', 'index': dash.dependencies.ALL}, 'value')
)
def update_results(n_clicks, titles, headings, first_paragraphs, body_texts, views, shares, likes, comments, positions, ages, keywords):
    if n_clicks > 0:
        results = []
        
        for i in range(len(titles)):
            # Calculate TF-IDF and TF
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([titles[i], headings[i], first_paragraphs[i], body_texts[i]])
            tfidf_scores = np.sum(tfidf_matrix.toarray(), axis=0)
            tf_scores = np.sum(tfidf_matrix.toarray() > 0, axis=0)

            # Calculate relevance score
            keyword = keywords[i]
            T, H, P, B, M = 5, 3, 4, 1, 2
            k_t = fuzz.partial_ratio(titles[i].lower(), keyword.lower())
            k_h = fuzz.partial_ratio(headings[i].lower(), keyword.lower())
            k_p = fuzz.partial_ratio(first_paragraphs[i].lower(), keyword.lower())
            k_b = body_texts[i].lower().count(keyword.lower())
            k_m = 1
            R = T * k_t + H * k_h + P * k_p + B * k_b + M * k_m

            # Calculate freshness score
            F = 100
            age = ages[i]
            F_s = F / age

            # Calculate user interaction score
            V, S, L, C = 0.1, 0.2, 0.3, 0.4
            U = V * views[i] + S * shares[i] + L * likes[i] + C * comments[i]

            # Calculate final ranking score
            alpha, beta, gamma, delta = 0.4, 0.3, 0.2, 0.1
            personalised = 5.0
            F_r = alpha * R + beta * 1 + gamma * F_s + delta * U + personalised

            # Display results for each page
            page_results = [
                html.H4(f"Page {i + 1} Results"),
                html.P(f"Relevance Score (R): {R:.2f}"),
                html.P(f"TF-IDF Scores: {tfidf_scores}"),
                html.P(f"TF Scores: {tf_scores}"),
                html.P(f"Freshness Score (F_s): {F_s:.2f}"),
                html.P(f"User Interaction Score (U): {U:.2f}"),
                html.P(f"Final Ranking Score (F_r): {F_r:.2f}"),
                html.P(f"Known Page Ranking Position: {positions[i]}"),
                html.P(f"Keyword for Ranking Prediction: {keywords[i]}")
            ]
            
            results.extend(page_results)
        
        return results
    
    return []

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
