import datetime

#Test dictionary
users=[
    {'name':'Mark' , 'birthday': datetime.datetime(year=2010 , month=1, day=3)},
    {'name':'Alex' , 'birthday': datetime.datetime(year=1999 , month=9 , day=1)},
    {'name':'Kate' , 'birthday': datetime.datetime(year=2001 , month=4 , day=26)},
    {'name':'Sue'  , 'birthday': datetime.datetime(year=2006 , month=10 , day=30) }
]

def get_birthdays_per_week(users : list) -> None: 

    result={
    'Monday': [],
    'Tuesday': [],
    'Wednesday': [],
    'Thursday': [],
    'Friday': []
    }

    for i in users:
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
        print(res_str[:-1])

print(get_birthdays_per_week(users))
