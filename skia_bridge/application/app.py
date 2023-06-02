# Copyright 2023 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import absolute_import
from flask import Flask

from application.perf_api import query_anomalies, skia_perf_upload
from application import health_checks


def Create():
  app = Flask(__name__)
  app.register_blueprint(health_checks.blueprint, url_prefix='/')
  app.register_blueprint(query_anomalies.blueprint, url_prefix='/anomalies')
  app.register_blueprint(skia_perf_upload.blueprint, url_prefix='/data')
  return app
