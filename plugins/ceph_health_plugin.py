import collectd
import traceback
import subprocess

import base


class CephHealthPlugin(base.Base):

    def __init__(self):
        base.Base.__init__(self)

    def get_stats(self):
        """Retrieves ceph status"""

        ceph_cluster = "%s.%s" % (self.prefix, self.cluster)

        data = {ceph_cluster: {
            'health': {'ok': 0},
        }}
        output = None
        try:
            ceph_health_cmdline = 'ceph health'
            output = subprocess.check_output(ceph_health_cmdline, shell=True)
        except Exception as exc:
            collectd.error("ceph-osd: failed to ceph health :: %s :: %s"
                           % (exc, traceback.format_exc()))
            return

        output = output.strip()
        if output is None:
            collectd.error('ceph-health: failed to ceph health :: output was None')

        if output == 'HEALTH_OK':
            data[ceph_cluster]['health']['ok'] = 1
        return data

try:
    plugin = CephHealthPlugin()
except Exception as exc:
    collectd.error("ceph-health: failed to initialize ceph health plugin :: %s :: %s"
                   % (exc, traceback.format_exception()))


def configure_callback(conf):
    """Received configuration information"""
    plugin.config_callback(conf)


def read_callback():
    """Callback triggerred by collectd on read"""
    plugin.read_callback()

collectd.register_config(configure_callback)
collectd.register_read(read_callback, plugin.interval)

