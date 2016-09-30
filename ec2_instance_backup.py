#!/usr/bin/env python
####################################################################################
#
# Create a snapshot of every instance's volumes and optionally delete older copies.
# Requires a config file with the same name as this script but with .json extension.
# Options:
#   backupList: an array of instance id(s) or tags to backup
#   stopInstanceBeforeBackup: should we stop instance before backup. Recommended.
#   deleteOldSnapshots: should we delete old snapshot(s)
#   copiesToKeep: how many copies of old snapshot(s) to keep
#
####################################################################################

import os
import sys
import json
import click
from datetime import datetime
from gen_util import LoggingUtil
from aws_util import Ec2Util


def date_compare(date1, date2):
    if date1.start_time < date2.start_time:
        return -1
    elif date1.start_time == date2.start_time:
        return 0
    return 1    

    
def backup_volume(start_date, instance_name, instance, is_delete_old=True, num_retained=7):
    for volume in instance.volumes.all():
        description = 'Snapshot created by {} for {}, {}, {}, {} on {} UTC'.format(sys.argv[0], instance_name, instance.id, instance.image_id, volume.id, start_date)

        snapshot_result = volume.create_snapshot(DryRun=False, Description=description)
        if snapshot_result:
            log_util.info('\t' + description)
            snapshots = [i for i in volume.snapshots.all()]
            snapshots.sort(date_compare)

            if is_delete_old:
                delta = len(snapshots) - num_retained
                for i in range(delta):
                    try:
                        log_util.info('\t\tDeleting %s' % snapshots[i])
                        snapshots[i].delete()
                    except Exception as ex:
                        log_util.info('\t\tCannot delete %s. %s' % (snapshots[i], ex))
        else:
            log_util.info('\tFailed to create snapshot for %s' % volume.id)


@click.command()
@click.option('-p', '--profile', default='default', help='Profile name to use.')
def cli():
    base_name = os.path.basename(sys.argv[0])
    base_name_no_ext = os.path.splitext(base_name)[0]
    config_file = base_name_no_ext + '.json'
    log_file = base_name_no_ext + '.log'

    ec2_util = Ec2Util(profile)
    log_util = LoggingUtil(log_file)
    log_util.info('Starting backup')
    log_util.info('Using config file at: ' + config_file)

    with open(config_file) as json_file:
        json_config = json.load(json_file)
        backup_list = json_config['backupList']
        stop_instance_before_backup = json_config['stopInstanceBeforeBackup']
        delete_old_snapshots = json_config['deleteOldSnapshots']
        copies_to_keep = json_config['copiesToKeep']

    log_util.info('Backup will use the following options:')
    log_util.info('    backupList: %s' % backup_list)
    log_util.info('    stopInstanceBeforeBackup: %s' % stop_instance_before_backup)
    log_util.info('    deleteOldSnapshots: %s' % delete_old_snapshots)
    log_util.info('    copiesToKeep: %s' % copies_to_keep)

    start_date = datetime.today().isoformat(' ')
    instances = ec2_util.get_all_instances()

    for instance in instances:
        found = False
        instance_name = None
        if instance.id in backup_list:
            found = True
            instance_name = instance.id
        elif instance.tags is not None:
            for tag in instance.tags:
                tag_key = tag['Key']
                tag_value = tag['Value']
                if tag_key == 'Name' and tag_value in backup_list:
                    found = True
                    instance_name = tag_value
        if found:
            log_util.info('Backing up all volumes for instance %s' % instance_name)

            # If stop_instance_before_backup == True and instance is running, we need to stop it first
            cur_instance_state = instance.state['Name']
            if stop_instance_before_backup and cur_instance_state == 'running':
                instance.stop()
                instance.wait_until_stopped()

            backup_volume(start_date, instance_name, instance, delete_old_snapshots, copies_to_keep)

            # If instance was running at the beginning, we need to start it again
            if cur_instance_state == 'running':
                instance.start()

    log_util.info('All done!')

if __name__ == '__main__':
    cli()