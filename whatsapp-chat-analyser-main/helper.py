from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Fetch number of messages
    num_messages = df.shape[0]
    
    # Fetch total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    # Fetch number of media messages
    num_media_messages = df[df['message'].str.contains('<Media omitted>')].shape[0]
    
    #fetch number of links
    links=[]
    for message in df['message']:
       links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media_messages, len(links)
    
def most_busy_users(df):
    x=df['user'].value_counts().head()
    new_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x, new_df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()
    temp = df[df['user'] != 'group_notification']
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
          if word not in stop_words:
            y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc= wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc 

def most_common_words(selected_user, df):  
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user] 
    temp = df[df['user'] != 'group_notification']
  
    
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
       
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# def emoji_helper(selected_user,df):
#     if selected_user != 'Overall':
#         df=df[df['user'] == selected_user]
#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI])
#     emoji_df =pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emoji_df
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend(find_emojis(message))

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

# Your find_emojis function
def find_emojis(text):
    emoji_ranges = [
        (0x1F300, 0x1F3FA),  # Miscellaneous Symbols and Pictographs
        (0x1F400, 0x1F6F9),  # Additional Transport & Map Symbols, Geometric Shapes Extended
        (0x1F700, 0x1F773),  # Alchemical Symbols
        (0x1F780, 0x1F7D8),  # Geometric Shapes Extended
        (0x1F800, 0x1F80B),  # Supplemental Arrows-C
        (0x1F810, 0x1F847),  # Supplemental Symbols and Pictographs
    ]

    emojis = []
    for char in text:
        codepoint = ord(char)
        for start, end in emoji_ranges:
            if start <= codepoint <= end:
                emojis.append(char)
                break

    return emojis
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline
def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
