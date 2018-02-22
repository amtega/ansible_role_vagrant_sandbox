# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re, sys
from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    def get_playbook(self):
        """Return playbook file.

        Returns:
            str: playbook file name.
        """
        # Setup argument parser

        for arg in sys.argv:
            if re.search('.*\.yml', arg):
                playbook = arg
                break

        return playbook

    def run(self, tmp=None, task_vars=None):
        """Ansible action plugin main run method."""

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        result['changed'] = False
        result['failed'] = False
        result['playbook'] = self.get_playbook()

        return result
