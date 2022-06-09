 /* eslint-disable */

export default Object.freeze({
  SUMMARY_TYPES: {
    PER_RUN: 'per_run',
    DAILY: 'daily',
    WEEKLY: 'weekly'
  },
  API_BASE_PATH: process.env.NODE_ENV === 'development' ? 'http://localhost:9005' : '',
  ACTIVITY_TYPES: {

  },
  PER_EVENT_TEMPLATE_TAGS: {
    'name': 'The activity title in Strava',
    'description': 'The activity description in Strava',
    'type': 'The type of activity',
    'distance_miles': 'Total distance in miles',
    'distance_kilometers': 'Total distance in kilometers',
    'distance_meters': 'Total distance in meters',
    'start_date': 'The local start date of the activity',
    'start_time': 'The local start time of the activity',
    'duration': 'The duration of the activity',
    'end_time': 'The local end time of the activity',
    'total_elevation_gain_feet': 'Total elevation gain in feet', 
    'total_elevation_gain_meters': 'Total elevation gain in meters', 
    'elev_high_feet': 'Highest elevation point in feet',
    'elev_low_feet': 'Lowest elevation point in feet', 
    'elev_high_meters': 'Highest elevation point in meters', 
    'elev_low_meters': 'Lowest elevation point in meters',
    'average_speed_meters_per_second': 'Average speed in meters/second', 
    'average_speed_kilometers_per_hour': 'Average speed in km/hour',
    'average_speed_miles_per_hour': 'Average speed in miles/hour', 
    'max_speed_meters_per_second': 'Max speed in meters/second',
    'max_speed_kilometers_per_hour': 'Max speed in km/hour', 
    'max_speed_miles_per_hour': 'Max speed in miles/hour', 
    'kilojoules': 'Total work done in kilojoules during this activity. Rides only',
    'average_watts': 'Average power output in watts during this activity. Rides only', 
    'max_watts': 'Rides with power meter data only', 
    'pace_min_per_mile': 'Activity pace in minutes/mile', 
    'pace_min_per_km': 'Activity pace in min/kilometer'
  }
})


