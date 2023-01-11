import datetime

#Test list
users=[
    {'name': 'Derek Thomas', 'birthday': datetime.datetime(2023, 1, 8, 0, 0)}, 
    {'name': 'Julie Mathis', 'birthday': datetime.datetime(2023, 1, 9, 0, 0)},
    {'name': 'Jacqueline Griffin', 'birthday': datetime.datetime(2023, 1, 10, 0, 0)},
    {'name': 'Kenneth Smith', 'birthday': datetime.datetime(2023, 1, 11, 0, 0)},
    {'name': 'Ivan Robertson', 'birthday': datetime.datetime(2023, 1, 12, 0, 0)},
    {'name': 'John Woods', 'birthday': datetime.datetime(2023, 1, 30, 0, 0)},       #The date does not match the task condition
    {'name': 'Laura Christensen', 'birthday': datetime.datetime(2023, 1, 5, 0, 0)}  #The date does not match the task condition
    ]

def get_birthdays_per_week(users) -> None: 

    result={
    'Monday': [],
    'Tuesday': [],
    'Wednesday': [],
    'Thursday': [],
    'Friday': []
    }
    
    today = datetime.date.today()

    for i in users:
        if i.get('birthday').year == today.year and i.get('birthday').month == today.month and today.day <= i.get('birthday').day <= (today + datetime.timedelta(days=7)).day :
            
            #The current day of the week converted to the name of the day of the week in English
            current_day = i.get('birthday').strftime('%A')
            
            #Checking the days of the week
            if current_day == 'Monday' or current_day == 'Saturday' or current_day == 'Sunday':
                result.get('Monday').append(i.get('name'))
            elif current_day == 'Tuesday' :
                result.get('Tuesday').append(i.get('name'))
            elif current_day == 'Wednesday' :
                result.get('Wednesday').append(i.get('name'))
            elif current_day == 'Thursday' :
                result.get('Thursday').append(i.get('name'))
            elif current_day == 'Friday' :
                result.get('Friday').append(i.get('name'))


    for day_and_name in result.items():
        if len(day_and_name[1])==0:
            continue
        res_str = f"{day_and_name[0]}:"
        for name in day_and_name[1]:
            res_str+=f' {name},'
        print(res_str[:-1]+'\n')

print(get_birthdays_per_week(users))

#Output: Monday: Derek Thomas, Julie Mathis
         #Tuesday: Jacqueline Griffin
         #Wednesday: Kenneth Smith
         #Thursday: Ivan Robertson