# Copyright 2023 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from flask import make_response, Blueprint, request
import logging

from models import alert_group

alert_groups = Blueprint('alert_groups', __name__)

@alert_groups.route('/<group_id>/anomalies', methods=['GET'])
def GetAnomaliesHandler(group_id):
  try:
    group_id = int(group_id)
  except ValueError:
    logging.debug('Using group id %s as string.', group_id)

  try:
    anomalies = alert_group.AlertGroup.GetAnomaliesByID(group_id)
  except alert_group.NoEntityFoundException as e:
    return make_response(str(e), 404)
  return make_response(anomalies)

@alert_groups.route(
  '/test/<path:test_key>/start/<start_rev>/end/<end_rev>/subs/<subscription_names>/projects/<project_names>',
  methods=['GET'])
def GetGroupsForAnomalyHandler(
  test_key, start_rev, end_rev, subscription_names, project_names):
  group_keys = alert_group.AlertGroup.GetGroupsForAnomaly(
    test_key, start_rev, end_rev, subscription_names, project_names)

  return make_response(group_keys)
