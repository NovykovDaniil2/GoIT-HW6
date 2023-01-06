import datetime

#For test
import random

#Test dict
name_dict=[]
with open('name_holder.txt', 'r') as file:
    for line in file.readlines():
        name_dict.append({'name': line.replace('\n', '') , 'birthday': datetime.datetime(year=random.randint(1950,2050) , month=random.randint(1,12), day=random.randint(1,28))})



def get_birthdays_per_week(users) -> None: 

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
        print(res_str[:-1]+'\n')

print(get_birthdays_per_week(name_dict))
