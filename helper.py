from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import itertools
import re 
from collections import Counter

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head(10)
    print("the values o ftop 10 must busy users are")
    print(x)
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    #print(x)
    #print("new data")
    #print(df)
    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emoji_ctr = Counter()
    emojis_list = map(lambda x: ''.join(x.split()), emoji.EMOJI_DATA.keys())
    r = re.compile('|'.join(re.escape(p) for p in emojis_list))
    for idx, row in df.iterrows():

        emojis_found = r.findall(row["message"])
        for emoji_found in emojis_found:
            
            emoji_ctr[emoji_found] += 1
    top10emojis = pd.DataFrame()#columns={"emoji", "emoji_description", "emoji_count"})
# top10emojis = pd.DataFrame(data, columns={"emoji", "emoji_description", "emoji_count"}) 
    top10emojis["emoji"] = [''] * 10
    top10emojis['emoji_count'] = [0] * 10
    top10emojis['emoji_description'] = [''] * 10

    i = 0
    for item in emoji_ctr.most_common(10):
    # will be using another helper column, since during visualization, the emojis won't be rendered.
        description = emoji.demojize(item[0])[1:-1]    # using `[1:-1]` to remove the colons ':' at the end of the demojized strin
    
    # appending top 10 data of emojis.  # Loading into a DataFrame.
        top10emojis.emoji[i] = item[0]
        top10emojis.emoji_count[i] = int(item[1])
        top10emojis.emoji_description[i] = description
        i += 1
    # print("printing top10emojis")
    # print(top10emojis)
    emojis = []
    for msg in df['message']:
        #emojis.extend([c for c in message if c in emoji.EMOJI_DATA.keys()['en']])
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA.keys()])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return top10emojis

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    

    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day'].value_counts()

def month_activity_map(selected_user,df):


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    '''df3=df.copy()
    df3['message_count'] = [1] * df.shape[0]    # helper column to keep a count.
    #print(df3['message_count'])
    df3['hour'] = df3['date_time'].apply(lambda x: x.hour)
    #print(df3['hour'])
    grouped_by_time = df3.groupby('hour').sum().reset_index().sort_values(by = 'hour')
    #print(grouped_by_time)
    grouped_by_month_and_day = df.groupby(['month', 'day']).sum().reset_index()[['month', 'day', 'message_count']]
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    # grouping by day;
    grouped_by_day = df3.groupby('day').sum().reset_index()[['day', 'message_count']]


    # specific `order` to be printed in;
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']   # till Sept, since chats are till Septemeber
    # grouping by month;
    grouped_by_month = df3.groupby('month').sum().reset_index()[['month', 'message_count']]
    # (index='day', columns='period', values='message', aggfunc='count').fillna(0)'''
    user_heatmap = df.pivot_table(index = 'month', columns = 'day', values = 'message',aggfunc='count').fillna(0)

    return user_heatmap















