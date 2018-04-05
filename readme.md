# Pull Historical Weather Data From Dark Sky

_Created for the 2nd Milestone Assignment for DATASCI 400 BS Wi 18 at the University of Washington._

[Powered by Dark Sky](https://darksky.net/poweredby/)

[API Documentation](https://darksky.net/dev/docs)

This code pulls a given number of days worth of weather data from Dark Sky (starting from the current day and working backwards), parses the response, does some formatting, then saves it as a csv. With the free tier of the Dark Skies API, I can make up to 1000 requests (or 1000 days' worth of data) a day, so the script limits the max number of days one can pull.