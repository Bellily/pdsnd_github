import time
import pandas as pd

CITY_DATA = { 'Chicago' : 'chicago.csv' ,
              'New York City' : 'new_york_city.csv',
              'Washington' : 'washington.csv' }

list_months = ["Jan", "Feb", "Mar", "May", "Jun", "Jul"]
dict_days = { 'Mo' : 'Monday', 'Tu':'Tuesday', 'We':'Wednesday', 'Th': 'Thursday', 'Fr': 'Friday', 'Sa': 'Saturday', 'Su':'Sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to analyze "Chicago", "New York City" or "Washington"? Please type out the city name:\n').title()
            # check if the user made a valid choice of city
        except ValueError:
            print('Please type out the city name')
            continue
        if city not in ('Chicago', 'New York City', 'Washington'):
            print('Please select a valid city or check the spelling.')
            continue
        else:
            # user made a valid choice and the loop is exited
            print('You selected: ', city)
            break

    # get user input for month (all, january, february, ... , june) and check whether he made a valid entry
    while True:
        try:
            month = input('Which month would you like to analyze? Please type "Jan", "Feb", "Mar", "May", "Jun", "Jul", or type "None" for no month-filter.\n').title()
            # check if the user made a valid choice of city
        except ValueError:
            print('Please type out the month as specified above.')
            continue
        if month not in list_months and month != 'None':
            print('Please select a valid month or check the spelling.')
            continue
        else:
            # user made a valid choice and the loop is exited
            print('You selected: ', month)
            break

    # get user input for day of week (all, monday, tuesday, ... sunday) and check whether he made a valid entry
    while True:
        try:
            day_input = input('Which day of the week would you like to analyze? Type "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su" or "None" for no day-filter:\n').title()

        except ValueError:
            print('Please type out the day as specified above')
            continue
        if day_input not in ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su", "None"):
            print('Please select a valid month or check the spelling.')
            continue
        else:
            # user made a valid choice and the loop is exited
            if day_input != "None":
                day = dict_days[day_input]
            else: 
                day = "None"
            print('You selcted: ', day)
            break


    print('-'*40)
    return city, month, day


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
    #The following function contains code which was taken from the Practise Solution #3 from Udacity
    #Read the csv file of the selected city, by indexing the CITY_DATA dictionary given above
    df = pd.read_csv(CITY_DATA[city])


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'None':
        # use the index of the months list to get the corresponding int and increase by +1 as counting starts at 0
        month = list_months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'None':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df['month'].value_counts().idxmax()
    print('\n Most common month:', common_month)


    # display the most common day of week
    common_weekday = df['day_of_week'].value_counts().idxmax()
    print('\n Most common weekday:', common_weekday)


    # display the most common start hour
    common_hour = df['hour'].value_counts().idxmax()
    print('\n Most common hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('\n Most people started at the station:', start_station)
    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\n Most people ended their ride at the station:', end_station)

    # display most frequent combination of start station and end station trip
    start_end_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('\n Most common combination:', start_end_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()/60
    print('\n Total travel time in minutes: ', travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    print('\n Mean travel time in minutes: ', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\n User types: ', user_types)
    # In case the user selected Washington, a Key Error needs to be avoided, as there is no data on gender and year of birth
    while True:
        try:
            # Display counts of gender
            genders = df['Gender'].value_counts()
            print('\n Gender counts: ', genders)

            # Display earliest, most recent, and most common year of birth
            earliest_yob = df['Birth Year'].min()
            print('\n Earliest year of birth: ', earliest_yob)

            recent_yob = df['Birth Year'].max()
            print('\n Most recent year of birth: ', recent_yob)

            common_yob = df['Birth Year'].mode()[0]
            print('\n Most common year of birth: ', common_yob)

            break

        except KeyError:
            print('No data on gender and year of birth available.')
            break


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        print(df.head())
        station_stats(df)
        print(df.head())
        trip_duration_stats(df)
        print(df.head())
        user_stats(df)

        # Ask the suer if he want's to see the first 5 lines of code
        raw_data = input('\nWould you like to see the first 5 lines of code?').lower()
        if raw_data == 'yes':
            i=5
            print(df.iloc[:i])
            # Ask the user if they want to see 5 additional lines of code and repeat as requested
            repeat = input('\nWould you like to see the next 5 lines of code?\n').lower()
            while repeat == 'yes':
                n = i
                i +=5
                print(df.iloc[n : i])
                repeat = input('\nWould you like to see the next 5 lines of code?\n')



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
