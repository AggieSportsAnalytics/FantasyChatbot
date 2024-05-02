### 🏁 AI-powered Chatbot for draft and trade guidance in Fantasy Football and Basketball

Every year, over 60 million Americans play fantasy sports. Many players depend on online tools for trade and draft guidance. These trade analyzers are purely data driven and poorly designed. Our project aims to revolutionize fantasy sport trade analyzers. <b>HIKE</b> is a chatbot for amazing personalized advice in Fantasy Football and Basketball. It provides conversational advice using a combination of time series analysis, score projections, and LLM-powered sentiment analysis. The project is built entirely in Python using the LangChain, Statsmodels, and Streamlit libraries.
<br></br>
<img width="990" alt="image" src="https://github.com/AggieSportsAnalytics/FantasyChatbot/blob/7f7ebd179ebdf983c86fbd8d6ab373f9f6d7b98a/chatbotphoto.png">

# 🔑 Key Features

## Large Language Model (LLM) Integration

HIKE utilizes LLMs through Retrieval Augmented Generation (RAG) for natural language chatting and conducting sentiment analysis on sports news.
<br></br>
<img width="990" alt="image" src="https://github.com/AggieSportsAnalytics/FantasyChatbot/blob/45c3f1d46ab61f51957e33a64bff22cf9f19024b/images/rag.png">

## Time Series Analysis

HIKE implements time series analysis to analyze data over the sports season. This allows HIKE algorithm to understand data at specific times during the football and basketball seasons.
<br></br>
<img width="990" alt="image" src="https://github.com/AggieSportsAnalytics/FantasyChatbot/blob/45c3f1d46ab61f51957e33a64bff22cf9f19024b/images/timeseriesanalysis.png">

## Streamlit Frontend

The frontend is built using Streamlit, allowing for easy modification and rapid performance. This choice eliminates the need for conventional request-response cycles between a frontend and backend, significantly reducing latency.
<br></br>
<img width="990" alt="image" src="https://github.com/AggieSportsAnalytics/FantasyChatbot/blob/45c3f1d46ab61f51957e33a64bff22cf9f19024b/images/streamlit.png">

### 💻 Code

We sourced Football data from an open-source <a href="https://www.kaggle.com/datasets/jpmiller/nfl-competition-data" target="_blank">Kaggle dataset</a> with robust data covering the past five seasons, including the most recent reason in 2023.

This data needed to be converted from CSV to JSON format in order to feed to our LLM using LangChain.

```py
def csv_to_json(file_paths):
    for file_path in file_paths:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            week_number = file_name.replace('week', '')  # Extracting week number from file name

            # Creating JSON structure with week number
            json_data = {
                "week_number": week_number,
                "data": list(csv_reader)
            }

            # Saving each file as a separate JSON file
            json_file_name = f"{file_name}.json"
            with open(json_file_name, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
 ...
```

We sourced Basketball data via webscraping on the NBA website.

```py
for y in years:
    for s in season_type:
        api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season='+y+'&SeasonType='+s+'&StatCategory=PTS'
        r = requests.get(url=api_url, headers=headers).json()
        stats_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
        stats_df2 = pd.DataFrame({'Year':[y for i in range(len(temp_df1))],
                        'Season_type':[s for i in range(len(temp_df1))]})
        stats_df3 = pd.concat([stats_df2, stats_df1], axis=1)
        df = pd.concat([df, stats_df3], axis=0)
        print(f'Finish scraping data for the {y} {s}.')
        lag = np.random.uniform(low=5,high=40) #Want to be not looking like a bot out there
        print(f'...waiting {round(lag,1)} seconds')
        time.sleep(lag)
...
```
