import re
import pandas as pd
import datetime
def preprocess(data): 
    key='12hr'
    split_formats = {
        '12hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s',
        '24hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
        'custom' : ''
    }
    datetime_formats = {
        '12hr' : '%m/%d/%y, %I:%M %p - ',
        '24hr' : '%m/%d/%y, %H:%M - ',
        'custom': ''
    }
    datetime_formats1 = {
            '12hr' : '%d/%m/%y, %I:%M %p - ',
            '24hr' : '%d/%m/%y, %H:%M - ',
            'custom': ''

    }
    datetime_formats2={
        '12hr' : '%d/%m/%Y, %I:%M %p - ',
        '24hr' : '%d/%m/%Y, %H:%M - ',
        'custom': ''

    }
    datetime_formats3={
        '12hr' : '%m/%d/%y, %I:%M %p - ',
        '24hr' : '%m/%d/%y, %H:%M - ',
        'custom': ''

    }
    #with open(file, 'r', encoding='utf-8') as raw_data:
    raw_string = ' '.join(data.split('\n')) 
    user_msg = re.split(split_formats[key], raw_string) [1:] 
    date_time = re.findall(split_formats[key], raw_string)
    df = pd.DataFrame({'date_time': date_time, 'user_msg': user_msg})
    # try:

    #   df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats[key])
    # except:
    #   try:
    #     df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats1[key])
    #   except:
    #     df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats2[key])
    try:

      df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats[key])
    except:
      
      try:
        df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats1[key])
      except:

        try:

          df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats2[key])
        except:

          df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats3[key])

    usernames = []
    msgs = []
    for i in df['user_msg']:
        a = re.split('([\w\W]+?):\s', i) 
        if(a[1:]): 
            usernames.append(a[1])
            msgs.append(a[2])
        else: 
            usernames.append("group_notification")
            msgs.append(a[0])         
    df['user'] = usernames
    df['message'] = msgs
    df.drop('user_msg', axis=1, inplace=True)
    df[df['message'] == ""].shape[0]
    df['day'] = df['date_time'].dt.strftime('%a')
    df['month'] = df['date_time'].dt.strftime('%b')
    df['year'] = df['date_time'].dt.year
    df['date'] = df['date_time'].apply(lambda x: x.date())
    print(df.head())
    return df
    '''split_formats = {
        '12hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s',
        '24hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
        'custom' : ''
    }
    datetime_formats = {
        '12hr' : '%m/%d/%y, %I:%M %p - ',
        '24hr' : '%d/%m/%Y, %H:%M - ',
        'custom': ''
    }
    datetime_formats1 = {
            '12hr' : '%d/%m/%y, %I:%M %p - ',
            '24hr' : '%d/%m/%y, %H:%M - ',
            'custom': ''

    }
    datetime_formats2={
        '12hr' : '%d/%m/%Y, %I:%M %p - ',
        '24hr' : '%d/%m/%Y, %H:%M - ',
        'custom': ''

    }
    raw_string = ' '.join(data.split('\n')) 
    user_msg = re.split(split_formats[key], raw_string) [1:] 
    date_time = re.findall(split_formats[key], raw_string)
    df = pd.DataFrame({'date_time': date_time, 'user_msg': user_msg})
    try:

      df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats[key])
    except:
      try:
        df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats1[key])
      except:
        df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats2[key])
    usernames = []
    msgs = []
    for i in df['user_msg']:
        a = re.split('([\w\W]+?):\s', i) 
        if(a[1:]): 
            usernames.append(a[1])
            msgs.append(a[2])
        else: 
            usernames.append("group_notification")
            msgs.append(a[0])         
    df['user'] = usernames
    df['message'] = msgs
    df.drop('user_msg', axis=1, inplace=True)
    #df = rawToDf('WhatsApp Chat with III TRAINING&PLACEMENT.txt', '12hr')
    df[df['message'] == ""].shape[0]
    df['day'] = df['date_time'].dt.strftime('%a')
    df['month'] = df['date_time'].dt.strftime('%b')
    df['year'] = df['date_time'].dt.year
    df['date'] = df['date_time'].apply(lambda x: x.date())
    # print(df)
    return df'''