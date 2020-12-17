import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US Cities bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input("Enter the city you would like to explore: [Chicago], [New York City], [Washington]? ")
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Wrong city! Please enter the correct city to explore!")


    # Get user input for month (january, february, ... , june, all)
    while True:    
        month = input("Which month's details you want: [January], [February], [March], [April], [May], [June], [All]? ")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Wrong month! Please enter the correct month name or type [All]!")

    # Get user input for day of week (monday, tuesday, ... sunday, all)
    while True:
        day = input("Which day's details you want: [Monday], [Tuesday], [Wednesday], [Thursday], [Friday], [Saturday], [Sunday], [All]? ")
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Wrong day! Please enter the correct day name or type [All]!")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
   df = pd.read_csv(CITY_DATA[city])
   df['Start Time'] = pd.to_datetime(df['Start Time'])
   df['month'] = df['Start Time'].dt.month
   df['day_name'] = df['Start Time'].dt.day_name()

   if month != 'all':
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months.index(month) + 1
    df = df[df['month'] == month]
        
   if day != 'all':
       df = df[df['day_name'] == day.title()]

   return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month's Name instead of showing the month's order number
    popular_month = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f"Most Popular Month: {popular_month[df['month'].mode()[0]-1]}")

    # Most popular day
    popular_day = df['day_name'].mode()[0]
    print(f"\nMost Popular Day: {popular_day}")

    df['hour'] = df['Start Time'].dt.hour

    # Most popular hour
    popular_hour = df['hour'].mode()[0]
    print(f"\nMost Popular Start Hour: {popular_hour}")


    # Most common start hour
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    print("The most commonly used start station: ", df['Start Station'].mode()[0], "\n")

    # Most commonly used end station
    print("The most commonly used end station: ", df['End Station'].mode()[0], "\n")

    # Most frequent combination of start station and end station trip
    df['comb'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start station and end station trip: ", df['comb'].mode()[0])

    # Most frequent combination of start station and end station trip
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("The total travel time:", df['Trip Duration'].sum(), "\n")

    # Mean travel time
    print("The total mean time:", df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, "\n")
    if city != 'washington':
        # Washington raw data doesn't has gender information
        # Display count of genders
        gender = df.groupby(['Gender'])['Gender'].count()
        print(gender)
        # Display earliest, most recent, and most common year of birth
        mostRecentYearOfBirth = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        earliestYearOfBirth = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        mostCommonYearOfBirth = df['Birth Year'].mode()[0]
        print("The earliest year of birth: ", earliestYearOfBirth, "\n")
        print("The most recent year of birth: ", mostRecentYearOfBirth, "\n")
        print("The most common year of birth: ", mostCommonYearOfBirth, "\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    x = 1
    while True:
        raw = input('\nWould you like to see some raw data? Enter [Yes] or [No].\n')
        if raw.lower() == 'yes':
            print(df[x:x+5])
            x = x + 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart and expolre another city? Enter [Yes] or [No].\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
