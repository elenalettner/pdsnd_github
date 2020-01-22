import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS =  ["january", "february", "march", "april", "may", "june", "all"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city, day, month = "","",""
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    while city not in CITY_DATA:
        city = input('\nWould you like to see data for "Chicago", "New York City", or "Washington"?\n').strip().lower()

   # get user input for month (all, january, february, ... , june)
    while month not in MONTHS:
        month = input('\nFor which month - "January", "February", "March", "April", "May", "June", or "all" to apply no month filter?\n').strip().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in DAYS:
        day = input('\nFor which day - "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", or "all" to apply no day filter?\n').strip().lower()

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

    print('\nOK, loading data for "{}" city and filtering by month="{}" and day="{}"...\n'.format(city,month,day))
    start_time = time.time()
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print('-'*40)
    return df


def display_data(df, rows=5):
    """Displays rows from the DataFrame provided as an argument.
    Args:
        (df) DataFrame - the dataframe from where to take the rows to display
        (int) rows - optional argument, which specifies how many rows to display. It defaults to 5
    """
    print('\nDisplaying data...\n')
    start_time = time.time()
    print(df.iloc[0:rows])

    for i in range(rows, len(df)-1, rows):
        more = input('\nWould you like to see more raw data? Enter "yes" or "no".\n')
        if more.strip().lower() != "yes":
            break
        else:
            print(df.iloc[i:i+rows])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month is {}.'.format(MONTHS[common_month-1].title()))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of week is {}.'.format(common_day))

    # display the most common start hour
    df['start hour'] = df['Start Time'].dt.hour
    start_hour = df['start hour'].mode()[0]
    print('Most common start hour is {} o\'clock.'.format(start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station is "{}"'.format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station is "{}"'.format(end_station))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' --> '+ df['End Station']
    frequent_trip = df['trip'].mode()[0]
    print('Most common trip from start to end is "{}"'.format(frequent_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('\nTotal travel time is %s seconds.' % total_time)
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('\nAverage travel time is %s seconds.\n' % mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nUser Types:\n{}'.format(user_types))

    try:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print('\nGender:\n{}'.format(gender_counts))

        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mean())
        print('\nEarliest year of birth is {}'.format(earliest_year))
        print('Most recent year of birth is {}'.format(recent_year))
        print('Most common year of birth is {}'.format(common_year))
    except KeyError:
        print('\n"Gender" and "Birth Year" Statistics are unavailable for {}\n'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
