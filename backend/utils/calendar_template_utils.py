import stravalib.model
from stravalib import unithelper
from stravalib.model import Activity
import re
import logging
import time

from backend import schemas
from backend.schemas import CalendarTemplateType

VALID_ACTIVITIES: list = [t.lower() for t in stravalib.model.Activity.TYPES]

VALID_DEFAULT_TEMPLATE_KEYS = ['name', 'description', 'type', 'distance_miles', 'distance_kilometers',
                               'distance_meters', 'start_date', 'start_time', 'duration', 'end_time',
                               'total_elevation_gain_feet', 'total_elevation_gain_meters', 'elev_high_feet',
                               'elev_low_feet', 'elev_high_meters', 'elev_low_meters',
                               'average_speed_meters_per_second', 'average_speed_kilometers_per_hour',
                               'average_speed_miles_per_hour', 'max_speed_meters_per_second',
                               'max_speed_kilometers_per_hour', 'max_speed_miles_per_hour', 'kilojoules',
                               'average_watts', 'max_watts', 'pace_min_per_mile', 'pace_min_per_km']


VALID_DEFAULT_SUMMARY_TEMPLATE_KEYS = ['distance_miles', 'distance_kilometers', 'distance_meters', 'duration',
                                       'elevation_gain_feet', 'elevation_gain_meters', 'avg_distance_miles',
                                       'avg_distance_kilometers', 'avg_distance_meters', 'avg_duration',
                                       'avg_elevation_gain_meters', 'avg_pace_min_per_mile',
                                       'avg_pace_min_per_km']


def _value_dict(activity: Activity) -> dict:
    return {
        'name': str(activity.name),
        'description': str(activity.description),
        'type': str(activity.type),
        'distance_miles': str(unithelper.miles(activity.distance)),
        'distance_kilometers': str(unithelper.kilometers(activity.distance)),
        'distance_meters': str(unithelper.meters(activity.distance)),
        'start_date': str(activity.start_date_local.date()),
        'start_time': str(activity.start_date_local.time()),
        'duration': str(activity.moving_time),
        'end_time': str((activity.start_date_local + activity.moving_time).time()),
        'total_elevation_gain_feet': str(unithelper.feet(activity.total_elevation_gain)),
        'total_elevation_gain_meters': str(unithelper.meters(activity.total_elevation_gain)),
        'elev_high_feet': str(unithelper.feet(activity.elev_high)),
        'elev_low_feet': str(unithelper.feet(activity.elev_low)),
        'elev_high_meters': str(unithelper.meters(activity.elev_high)),
        'elev_low_meters': str(unithelper.meters(activity.elev_low)),
        'average_speed_meters_per_second': str(unithelper.meters_per_second(activity.average_speed)),
        'average_speed_kilometers_per_hour': str(unithelper.kilometers_per_hour(activity.average_speed)),
        'average_speed_miles_per_hour': str(unithelper.miles_per_hour(activity.average_speed)),
        'max_speed_meters_per_second': str(unithelper.meters_per_second(activity.max_speed)),
        'max_speed_kilometers_per_hour': str(unithelper.kilometers_per_hour(activity.max_speed)),
        'max_speed_miles_per_hour': str(unithelper.miles_per_hour(activity.max_speed)),
        'kilojoules': str(activity.kilojoules),  # Rides only
        'average_watts': str(activity.average_watts),  # Rides only
        'max_watts': str(activity.max_watts),
        'pace_min_per_mile': time.strftime('%M:%S', time.gmtime(
            activity.moving_time.total_seconds() / float(unithelper.miles(activity.distance)))) + ' min/mile',
        'pace_min_per_km': time.strftime('%M:%S', time.gmtime(
            activity.moving_time.total_seconds() / float(unithelper.kilometers(activity.distance)))) + ' min/km'
    }


def _value_dict_aggregate(activities: [Activity]) -> dict:
    total_activities = len(activities)
    if total_activities == 0:
        return {}

    total_distance_meters: unithelper.meters = unithelper.meters(
        sum(float(unithelper.meters(activity.distance)) for activity in activities))
    total_duration_seconds: unithelper.seconds = unithelper.seconds(
        sum(float(unithelper.seconds(activity.moving_time.total_seconds())) for activity in activities))
    total_elevation_gain_meters: unithelper.meters = unithelper.meters(
        sum(float(unithelper.meters(activity.total_elevation_gain)) for activity in activities))

    return {
        'distance_miles': str(unithelper.miles(total_distance_meters)),
        'distance_kilometers': str(unithelper.kilometers(total_distance_meters)),
        'distance_meters': str(unithelper.meters(total_distance_meters)),
        'duration': str(time.strftime('%H:%M:%S', time.gmtime(float(total_duration_seconds)))),
        'elevation_gain_feet': str(unithelper.feet(total_elevation_gain_meters)),
        'elevation_gain_meters': str(float(total_elevation_gain_meters)),
        'avg_distance_miles': str(unithelper.miles(total_distance_meters / total_activities)),
        'avg_distance_kilometers': str(unithelper.kilometers(total_distance_meters / total_activities)),
        'avg_distance_meters': str(unithelper.meters(total_distance_meters / total_activities)),
        'avg_duration': str(time.strftime('%H:%M:%S', time.gmtime(float(total_duration_seconds / total_activities)))),
        'avg_elevation_gain_meters': str(float(total_elevation_gain_meters / total_activities)),
        'avg_pace_min_per_mile': time.strftime('%M:%S', time.gmtime(
            int(total_duration_seconds / unithelper.miles(total_distance_meters)))) + ' min/mile',
        'avg_pace_min_per_km': time.strftime('%M:%S', time.gmtime(
            int(total_duration_seconds / unithelper.kilometers(total_distance_meters)))) + ' min/km'
    }


def fill_template(template: str, activity: Activity) -> str:
    """
    Fill a template with the details from an activity
    :param template: the template to fill
    :param activity: the activity to pull information for the activity for
    :return: the filled template
    """

    filled_template: str = template
    vals: dict = _value_dict(activity)
    temp_keys = re.findall(r'{[a-zA-Z_. ]*}', filled_template)
    found_keys = map(lambda k: k.replace('{', '').replace('}', '').strip(), temp_keys)

    for key in found_keys:
        if key in vals:
            filled_template = re.sub(r'{ *' + key + ' *}', vals[key], filled_template)
        else:
            # Log error with key, but do not throw an exception so the template is still built
            logging.error('Failed to find key : {} while building template for activity: {}'.format(key, activity.id))

    return filled_template


def fill_summary_template(template: str, activities: [Activity]) -> str:
    """
    Fill a summary template by aggregating data for all activities
    :param template: the template to fill with activity information
    :param activities: the activities to pull data from
    :return: the completed template
    """
    filled_template: str = template
    temp_keys = re.findall(r'{[a-zA-Z_. ]*}', filled_template)
    found_keys = map(lambda k: k.replace('{', '').replace('}', '').strip(), temp_keys)

    cache: dict = {
        '': _value_dict_aggregate(activities)
    }

    for key in found_keys:
        split_key = key.split('.')
        activity_type: str = '' if len(split_key) == 1 else split_key[0].lower()
        temp_key: str = split_key[-1]

        if activity_type not in cache:
            cache[activity_type] = _value_dict_aggregate([a for a in activities if a.type.lower() == activity_type])

        vals = cache[activity_type]

        if temp_key in vals:
            filled_template = re.sub(r'{ *' + key + ' *}', vals[temp_key], filled_template)
        elif (activity_type in VALID_ACTIVITIES or activity_type == '') and len(vals.keys()) == 0:
            # Valid key, but no activities found
            filled_template = re.sub(r'{ *' + key + ' *}', 'None', filled_template)

    return filled_template


def verify_template(template: str, template_type: CalendarTemplateType) -> list:
    """
    Verify the template configuration returning any invalid template keys
    :param template: the template to verify
    :param template_type: the template type to distinguish between a summary or single activity template
    :return: a list of invalid template keys if there are any
    """

    temp_keys = re.findall(r'{[a-zA-Z_. ]*}', template)
    found_keys = map(lambda k: k.replace('{', '').replace('}', '').strip(), temp_keys)
    invalid_keys = []

    for key in found_keys:
        if template_type == CalendarTemplateType.ACTIVITY_SUMMARY and key not in VALID_DEFAULT_TEMPLATE_KEYS:
            invalid_keys.append(key)
        if template_type != CalendarTemplateType.ACTIVITY_SUMMARY:
            if len(key.split('.')) == 1:
                if key not in VALID_DEFAULT_SUMMARY_TEMPLATE_KEYS:
                    invalid_keys.append(key)
            elif len(key.split('.')) == 2:
                if key.split('.')[0].lower() not in VALID_ACTIVITIES or key.split('.')[1] not in VALID_DEFAULT_SUMMARY_TEMPLATE_KEYS:
                    invalid_keys.append(key)
            else:
                invalid_keys.append(key)

    return invalid_keys
