#!/usr/bin/env python3

import sys
import argparse
import yaml
from datetime import datetime, timedelta

from helpers import create_time_clause, connect_to_influxdb


backup_hour = 11


def validate_influxdb(influx_client):
    time_str = "%Y-%m-%dT%H:%M:%SZ"
    short_time_str = "%Y-%m-%dT%H"

    td = datetime.utcnow()
    end_dt = datetime(td.year, td.month, td.day, backup_hour, 0)
    if end_dt > td:
        end_dt -= timedelta(days=1)

    start_dt = datetime(2019, 1, 1, backup_hour, 0)

    dt = start_dt
    while dt < end_dt:
        start_time = dt.strftime(time_str)
        next_dt = dt + timedelta(days=1)
        end_time = next_dt.strftime(time_str)

        time_clause = create_time_clause(start_time, end_time)
        results = influx_client.query(
            'SELECT count(video_ts) FROM video_acked WHERE ' + time_clause)

        for pt in results['video_acked']:
            count = pt['count']
            break

        ss = dt.strftime(short_time_str)
        se = next_dt.strftime(short_time_str)

        if count < 20000:
            backup_data_name = '{}_{}.tar.gz'.format(ss, se)

            print('ERROR: {} - {}, count {}'.format(ss, se, count))
            print("    probably didn't restore {}".format(backup_data_name))
        else:
            print('OK: {} - {}, count {}'.format(ss, se, count))

        dt = next_dt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_settings')
    args = parser.parse_args()

    with open(args.yaml_settings, 'r') as fh:
        yaml_settings = yaml.safe_load(fh)

    # create an InfluxDB client and perform queries
    influx_client = connect_to_influxdb(yaml_settings)

    validate_influxdb(influx_client)


if __name__ == '__main__':
    main()