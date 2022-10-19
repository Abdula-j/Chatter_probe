import re
import pandas as pd
import datetime
def preprocess(data): 
    key='12hr'
    # print(data)
    # print(key)   
# def rawToDf(file, key):

#     '''Converts raw .txt file into a Data Frame'''
    split_formats = {
        '12hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s',
        '24hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
        'custom' : ''
    }
    datetime_formats = {
    
            '12hr' : '%d/%m/%y, %I:%M %p - ',
            '24hr' : '%d/%m/%y, %H:%M - ',
            'custom': ''

    }
    datetime_formats1={
        '12hr' : '%d/%m/%Y, %I:%M %p - ',
        '24hr' : '%d/%m/%Y, %H:%M - ',
        'custom': ''

    }
        # except:
            
        #     print("Something went wrong")

        # try:

        #     '12hr' : '%d/%m/%y, %I:%M %p - ',
        #     '24hr' : '%d/%m/%y, %H:%M - ',
        #     'custom': ''

        #     #df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
        # except:
        #     print("hellp")


        # #df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')

            
    # with open(file, 'r', encoding='utf-8') as raw_data:
    raw_string = ' '.join(data.split('\n')) 
    user_msg = re.split(split_formats[key], raw_string) [1:] 
    date_time = re.findall(split_formats[key], raw_string)
    df = pd.DataFrame({'date_time': date_time, 'user_msg': user_msg})
    try:

        df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats[key])
    except:
        df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_formats1[key])

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
    return df
    # pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # messages = re.split(pattern, data)[1:]
    # dates = re.findall(pattern, data)

    # df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # # convert message_date type
    # df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    # df.rename(columns={'message_date': 'date'}, inplace=True)

    # users = []
    # messages = []
    # for message in df['user_message']:
    #     entry = re.split('([\w\W]+?):\s', message)
    #     if entry[1:]:  # user name
    #         users.append(entry[1])
    #         messages.append(" ".join(entry[2:]))
    #     else:
    #         users.append('group_notification')
    #         messages.append(entry[0])

    # df['user'] = users
    # df['message'] = messages
    # df.drop(columns=['user_message'], inplace=True)

    # df['only_date'] = df['date'].dt.date
    # df['year'] = df['date'].dt.year
    # df['month_num'] = df['date'].dt.month
    # df['month'] = df['date'].dt.month_name()
    # df['day'] = df['date'].dt.day
    # df['day_name'] = df['date'].dt.day_name()
    # df['hour'] = df['date'].dt.hour
    # df['minute'] = df['date'].dt.minute

    # period = []
    # for hour in df[['day_name', 'hour']]['hour']:
    #     if hour == 23:
    #         period.append(str(hour) + "-" + str('00'))
    #     elif hour == 0:
    #         period.append(str('00') + "-" + str(hour + 1))
    #     else:
    #         period.append(str(hour) + "-" + str(hour + 1))

    # df['period'] = period

    #return df