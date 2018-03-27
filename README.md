# Ansible vagrant_sandbox role

This is an [Ansible](http://www.ansible.com) role that wraps vagrant_provisioner and idempotence_tester roles to make easy to run unit tests.

The role will provisione a vagrant based sandbox and run idempotence tests on the deployed vms.

## Requirements

- Ansible >= 2.4

## Role Variables

A list of all the default variables for this role is available in `defaults/main.yml`.

Also, the role setup the following facts during execution:

- vagrant_sandbox_boxes: contains the list of vagrant boxes provisioned on the sandbox.
- vagrant_sandbox_vms: contains the list of randomized vagrant vms provisioned on the sandbox.
- vagrant_sandbox_inventory: contains the path to a inventory file with the vagrant vms deployed in the sandbox.
- vagrant_sandbox_idempotence_result: contains the result of the idempotence tests.

## Dependencies

- amtega.vagrant_provisioner
- amtega.idempotence_tester

You can tune the behaviour of this dependant roles with their respective settings.

## Example Playbook

This is an example playbook:

```yaml
---
- name: sample vagrant_sandbox usage
  hosts: localhost
  roles:
    - role: amtega.vagrant_presets
    - role: amtega.vagrant_sandbox
      vagrant_sandbox_state: started
  tasks:
    - name: assert that idempotence test was ok
      assert:
        that: not vagrant_sandbox_idempotence_result is failed

- name: simple idempotence test
  hosts: vagrant_sandbox_vms
  tasks:
    - name: create an empty file
      copy:
        content: ""
        dest: /tmp/emptyfile
        force: no
  tags:
    - idempotence

- name: cleanup vagrant vagrant sandbox
  hosts: localhost
  roles:
    - role: vagrant_sandbox
      vagrant_sandbox_state: absent
```

If you want to create a temporary sandbox to work you can use the two sample playbooks provided in the `files` dir. First call the create sandbox playbook.

```
ansible-playbook files/create_sandbox.yml
```

Previous playbook should print the path to the inventory managed by the sandbox:

```
TASK [debug] **************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "vagrant_sandbox_inventory": "/tmp/ansible.oAxX3B.inventory"
}
```

You can work with this sandbox passing this inventory path to ansible-playbook using "-e" flag to fill the variable `vagrant_sandbox_inventory`:

```
ansible-playbook main.yml -i /tmp/ansible.oAxX3B.inventory
```

When you want to drop the sandbox use the provided cleanup playbook passing the vagrant_sandbox_inventory variable in the command line or entering it in the prompt that will be showed:

```
ansible-playbook files/cleanup_sandbox.yml -e "vagrant_sandbox_inventory=/tmp/ansible.oAxX3B.inventory"
```

## Testing

Test are based on vagrant vms. You can run the tests with the following commands:

```shell
$ cd amtega.vagrant_sandbox/tests
$ ansible-playbook main.yml
```

If you have vagrant engine configured you can avoid running dependant 'vagrant_engine' role (that usually requries root privileges) with the following commands:

```shell
$ cd amtega.vagrant_sandbox/tests
$ ansible-playbook --skip-tags "role::vagrant_engine" main.yml
```

## License

Copyright (C) 2017 AMTEGA - Xunta de Galicia

This role is free software: you can redistribute it and/or modify
it under the terms of:
GNU General Public License version 3, or (at your option) any later version;
or the European Union Public License, either Version 1.2 or – as soon
they will be approved by the European Commission ­subsequent versions of
the EUPL;

This role is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details or European Union Public License for more details.

## Author Information

- Juan Antonio Valiño García.
