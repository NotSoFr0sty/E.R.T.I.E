def getCurrentWeather(city='New York'):

    return "It's prolly sunny or something, idk."

if __name__ == "__main__":
    print('\n*** Get Current Weather Conditions ***\n')
    city = input("\nPlease enter a city: ")
    weatherData = getCurrentWeather(city)
    print("\n")
    print(weatherData)