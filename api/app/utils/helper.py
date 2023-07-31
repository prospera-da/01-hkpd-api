import calendar
import copy
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional


def response_tracking_adjustment(
    response: Dict,
    timestamp_list: List = [],
    date_list: List = [],
    boolean_list: List = [],
) -> Dict:

    """This is to accommodate pydantic model - tracking schema mapping
    as tracking schema can't understand types like datetime, date, and
    the translation is not automated. We cater three types of adjustment:
    date to int, datetime to int, and numerical bool to true-false bool.

    We expect the response to be either list or a dictionary, if it's a dictionary
    we presume that it has "result" key.

    Args:
        response (Union[List,Dict]): A response to be transformed
        timestamp_list (list, optional): List of timestamp fields that needs to be altered.
            Defaults to [].
        date_list (list, optional): List of date fields that needs to be altered.
            Defaults to [].
        boolean_list (list, optional): List of numerical bool fields that needs to be altered.
            Defaults to [].

    Returns:
        Dict: adjusted response
    """

    response_tracking = dict(copy.deepcopy(response))

    if "result" in response_tracking.keys():
        adjusted_result = []
        for single_result in response_tracking["result"]:
            adjusted_single_result = _response_tracking_adjustment(
                single_result, timestamp_list, date_list, boolean_list
            )
            adjusted_result.append(adjusted_single_result)

        response_tracking["result"] = adjusted_result
    else:
        response_tracking = _response_tracking_adjustment(
            response, timestamp_list, date_list, boolean_list
        )

    return response_tracking


def impute_time(value: Optional[int]) -> int:
    if value is None:
        value = int(1000 * time.time())
    return value


def impute_version(value: Optional[str]) -> str:
    if value is None:
        value = "v1"
    return value


def get_current_timestamp():
    return int(datetime.now().timestamp() * 1000)


def _response_tracking_adjustment(
    data: Dict,
    timestamp_list=[],
    date_list=[],
    boolean_list=[],
) -> Dict:
    response_tracking = {}
    for key, value in data.items():
        if key in date_list:
            response_tracking.update(
                {key: int(1000 * calendar.timegm(value.timetuple()))}
            )
        elif key in timestamp_list:
            response_tracking.update(
                {key: int(value.replace(tzinfo=timezone.utc).timestamp() * 1000)}
            )
        elif key in boolean_list:
            response_tracking.update(
                {key: True if value == 1 else False if value == 0 else None}
            )
        else:
            response_tracking.update({key: value})
    return response_tracking
