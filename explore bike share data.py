import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_name=input('Please select a city to analyze (\'chicago\',\'new york city\',\'washington\'): ')
    city_name=city_name.lower()
    while city_name not in CITY_DATA:
        city_name=input('City name is NOT valid, please input city name again (\'chicago\',\'new york city\', or \'washington\'): ')
        city_name=city_name.lower()
    global is_washington
    is_washington=0
    if city_name=='washington':
        is_washington=1

    # TO DO: get user input for month (all, january, february, ... , june)
    month=input("Which month would you like to see? Type 'january','february','march','april','may','june',or 'all':  ")
    month=month.lower()
    month_list=['all','january','february','march','april','may','june']
    while month not in month_list:
        month=input("An invalid month is entered, make sure you have typed 'january','february','march','april','may','june',or 'all'\nand enter again: ")
        month=month.lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day=input("Which day of the week would you like to see? Enter 'monday','tuesday','wednesday','thursday','friday','saturday',sunday',or 'all': ")
    day=day.lower()
    day_list=['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    while day not in day_list:
        day=input("day of week entered is invalid, type 'monday','tuesday','wednesday','thursday','friday','saturday',sunday',or 'all': ")
        day=day.lower()
    print('-'*40)
    return city_name, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #loading the city data
    filename=CITY_DATA[city]
    df=pd.read_csv(filename)

    #creating two extra colunms in df for filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    month_list=['all','january','february','march','april','may','june']
    #filtering df by 'month' and 'day_of_week'
    if month != 'all':
        df=df[df['month']==month_list.index(month)] # remember to use double equal sign ==
    if day!='all':
        df=df[df['day_of_week']==day.capitalize()] #The first letter of df['day_of_week'] is capitalised

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month=df['month'].mode()[0]
    print('The most common month is : ',most_common_month,'\n')

    # TO DO: display the most common day of week
    most_common_day_of_week=df['day_of_week'].mode()[0]
    print('The most common day of the week is : ',most_common_day_of_week,'\n')

    # TO DO: display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    most_common_start_hour=df['hour'].mode()[0]
    print('The most common start hour is : ',most_common_start_hour,'\n')

    #printing time took to finish the calcalations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station=df['Start Station'].mode()[0]
    print('Most common start station is ',most_common_start_station,'\n')
    # TO DO: display most commonly used end station
    most_common_end_station=df['End Station'].mode()[0]
    print('Most common end station is ',most_common_end_station,'\n')
    # TO DO: display most frequent combination of start station and end station trip
    df2=df.copy()
    df2['COUNTER'] =1       #initially, set that counter to 1.
    group_data = df2.groupby(['Start Station','End Station'])['COUNTER'].sum() #sum function

    print('most popular start&end station combination is \n',group_data.sort_values(ascending=False).head(1),'\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum(skipna=True)
    print('Total Travel Time is ',total_travel_time,'\n')

    # TO DO: display mean travel time
    count=df['Trip Duration'].count()
    mean_travel_time=total_travel_time/count
    print('Mean Travel Time is ', mean_travel_time,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if is_washington==0:
        gender_counts=df['Gender'].value_counts()
        print(gender_counts)

        # TO DO: Display earliest, most recent, and most common year of birth
        print('Earliest year of birth is ',df['Birth Year'].min(),'\n')
        print('Most recent year of birth is ',df['Birth Year'].max(),'\n')

        most_common_year_of_birth=df['Birth Year'].mode()[0]
        print('The most common year of birth is ',most_common_year_of_birth,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def see_rawdata(df):

    whether_to_see_rawdata=input('Would you like to see some raw data? Type \'yes\' or \'no\': ')
    if whether_to_see_rawdata.lower()=='yes':
        i=1
        print(df.iloc[0:5*i])
        whether_to_see_more_raw_data=input("Would you like to see more raw data? Type 'yes' or 'no': ")
        
        while whether_to_see_more_raw_data.lower()=='yes':
            i=i+1
            print(df.iloc[0:5*i])
            whether_to_see_more_raw_data=input("Would you like to see more raw data? Type 'yes' or 'no': ")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        see_rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
