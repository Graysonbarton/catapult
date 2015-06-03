# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from telemetry import benchmark
from telemetry.core import util
from telemetry.core.backends import android_command_line_backend
from telemetry.unittest_util import options_for_unittests

util.AddDirToPythonPath(util.GetChromiumSrcDir(), 'build', 'android')
from pylib.device import device_errors # pylint: disable=import-error
from pylib.device import device_utils # pylint: disable=import-error


class _MockBackendSettings(object):
  pseudo_exec_name = 'chrome'

  def __init__(self, path):
    self._path = path

  def GetCommandLineFile(self, _):
    return self._path


class AndroidCommandLineBackendTest(unittest.TestCase):

  def testQuoteIfNeededNoEquals(self):
    string = 'value'
    self.assertEqual(string,
                     android_command_line_backend._QuoteIfNeeded(string))

  def testQuoteIfNeededNoSpaces(self):
    string = 'key=valueA'
    self.assertEqual(string,
                     android_command_line_backend._QuoteIfNeeded(string))

  def testQuoteIfNeededAlreadyQuoted(self):
    string = "key='valueA valueB'"
    self.assertEqual(string,
                     android_command_line_backend._QuoteIfNeeded(string))

  def testQuoteIfNeeded(self):
    string = 'key=valueA valueB'
    expected_output = "key='valueA valueB'"
    self.assertEqual(expected_output,
                     android_command_line_backend._QuoteIfNeeded(string))

  @benchmark.Enabled('android')
  def testSetUpCommandLineFlagsCmdRestored(self):
    """Test that a previous command line file is restored.

    Requires a device connected to the host.
    """
    serial = options_for_unittests.GetCopy().device
    if serial:
      device = device_utils.DeviceUtils(serial)
    else:
      devices = device_utils.DeviceUtils.HealthyDevices()
      if not devices:
        raise device_errors.NoDevicesError()
      device = devices[0]
    cmd_file = '/data/local/tmp/test_cmd'
    backend_settings = _MockBackendSettings('/data/local/tmp/test_cmd')
    startup_args = ['--some', '--test', '--args']
    device.WriteFile(cmd_file, 'chrome --args --to --save')
    with android_command_line_backend.SetUpCommandLineFlags(
        device, backend_settings, startup_args):
      self.assertEqual('chrome --some --test --args',
                       device.ReadFile(cmd_file).strip())
    self.assertEqual('chrome --args --to --save',
                     device.ReadFile(cmd_file).strip())
    device.RunShellCommand(['rm', '-f', cmd_file], check_return=True)

  @benchmark.Enabled('android')
  def testSetUpCommandLineFlagsCmdRemoved(self):
    """Test that the command line file is removed if it did not exist before.

    Requires a device connected to the host.
    """
    serial = options_for_unittests.GetCopy().device
    if serial:
      device = device_utils.DeviceUtils(serial)
    else:
      devices = device_utils.DeviceUtils.HealthyDevices()
      if not devices:
        raise device_errors.NoDevicesError()
      device = devices[0]
    cmd_file = '/data/local/tmp/test_cmd'
    backend_settings = _MockBackendSettings('/data/local/tmp/test_cmd')
    startup_args = ['--some', '--test', '--args']
    device.RunShellCommand(['rm', '-f', cmd_file], check_return=True)
    with android_command_line_backend.SetUpCommandLineFlags(
        device, backend_settings, startup_args):
      self.assertEqual('chrome --some --test --args',
                       device.ReadFile(cmd_file).strip())
    self.assertFalse(device.FileExists(cmd_file))
