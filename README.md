# Ansible EDA source plugin for PAN-OS firewalls

This project is an implementation of a FastAPI application that receives firewall log messages from a Palo Alto Networks PAN-OS device, embedded within an Ansible EDA source plugin.

This project started as a modification of the `alertmanager.py` source plugin from the Ansible EDA. The original source plugin can be found [here](https://github.dev/ansible/event-driven-ansible/blob/main/plugins/event_source/alertmanager.py).

## Project Setup

### Prerequisites

There are two methods to deploying, either locally with Poetry or through a Docker container. These docs will cover the Docker based installation:

- Python 3.6 or higher
- Python Poetry
- Docker or Podman (RHEL based machines only)

### Installation

1. Clone the repository from GitHub.
2. Create a virtual environment using the command `poetry install`.
3. Activate the virtual environment using the command `poetry shell`.

### Building the container image

Build the Docker image using the command `invoke build`; macOS users on Apple silicon can use the command `invoke build --arm`.

Run the container using the command `invoke local` (or `invoke local --arm` for Apple silicon).

## Usage

Once the Ansible rule book is up and running, you can send a firewall log message to the `/endpoint` endpoint using a POST request. The request should contain the firewall log message in JSON format.

### PAN-OS HTTP Server Profile

You will need to structure your HTTP Server Profile to send the firewall log message to the Ansible rule book. The following example shows the configuration for a decryption log message:

```json
{
    "category": "network",
    "details": {
        "action": "$action",
        "app": "$app",
        "cn": "$cn",
        "dst": "$dst",
        "device_name": "$device_name",
        "error": "$error",
        "issuer_cn": "$issuer_cn",
        "root_cn": "$root_cn",
        "root_status": "$root_status",
        "sni": "$sni",
        "src": "$src",
        "srcuser": "$srcuser"
    },
    "receive_time": "$receive_time",
    "rule": "$rule",
    "rule_uuid": "$rule_uuid",
    "serial": "$serial",
    "sessionid": "$sessionid",
    "severity": "informational",
    "type": "decryption"
}
```

### Ansible Rulebook

Here is an example rule-book

```yaml
---
- name: "Receive logs sourced from HTTP Server Profile in PAN-OS"
  hosts: "localhost"

  ## Define how our plugin should listen for logs from the PAN-OS firewall
  sources:
    - cdot65.panos.logs:
        host: 0.0.0.0
        port: 5000
        type: decryption

  ## Define the conditions we are looking for
  rules:
    - name: "Troubleshoot Decryption Failure"
      condition: event.meta.log_type == "decryption"

      ## Define the action we should take should the condition be met
      action:
        debug:
```

### example output

Below is the console output of a healthy running rule-book.

```bash
2023-03-23 13:46:56,780 - ansible_rulebook.app - INFO - Starting sources
2023-03-23 13:46:56,781 - ansible_rulebook.app - INFO - Starting rules
2023-03-23 13:46:56,781 - ansible_rulebook.engine - INFO - run_ruleset
2023-03-23 13:46:58,040 - ansible_rulebook.engine - INFO - ruleset define: {"name": "Receive logs sourced from HTTP Server Profile in PAN-OS", "hosts": ["localhost"], "sources": [{"EventSource": {"name": "cdot65.panos.logs", "source_name": "cdot65.panos.logs", "source_args": {"host": "0.0.0.0", "port": 5000, "type": "decryption"}, "source_filters": []}}], "rules": [{"Rule": {"name": "Troubleshoot Decryption Failure", "condition": {"AllCondition": [{"EqualsExpression": {"lhs": {"Event": "meta.log_type"}, "rhs": {"String": "decryption"}}}]}, "actions": [{"Action": {"action": "debug", "action_args": {}}}], "enabled": true}}]}
2023-03-23 13:46:58,064 - ansible_rulebook.engine - INFO - load source
2023-03-23 13:46:59,055 - ansible_rulebook.engine - INFO - load source filters
2023-03-23 13:46:59,056 - ansible_rulebook.engine - INFO - Calling main in cdot65.panos.logs
2023-03-23 13:46:59,058 - ansible_rulebook.engine - INFO - Waiting for all ruleset tasks to end
2023-03-23 13:46:59,058 - ansible_rulebook.rule_set_runner - INFO - Waiting for actions on events from Receive logs sourced from HTTP Server Profile in PAN-OS
2023-03-23 13:46:59,058 - ansible_rulebook.rule_set_runner - INFO - Waiting for events, ruleset: Receive logs sourced from HTTP Server Profile in PAN-OS
2023-03-23 13:46:59 060 [drools-async-evaluator-thread] INFO org.drools.ansible.rulebook.integration.api.io.RuleExecutorChannel - Async channel connected
2023-03-23 13:47:08,933 - aiohttp.access - INFO - 10.0.2.100 [23/Mar/2023:13:47:08 +0000] "POST /endpoint HTTP/1.1" 202 200 "-" "-"
2023-03-23 13:47:09 001 [main] INFO org.drools.ansible.rulebook.integration.api.rulesengine.RegisterOnlyAgendaFilter - Activation of effective rule "Troubleshoot Decryption Failure" with facts: [Event DROOLS_PROTOTYPE with values = {payload.details.root_status=trusted, payload.receive_time=2023/03/23 08:47:08, payload.details.action=allow, payload.severity=informational, payload.details.srcuser=, payload.details={app=incomplete, srcuser=, issuer_cn=R3, device_name=hou-vfw-01, dst=89.238.73.97, src=10.0.11.100, action=allow, root_cn=ISRG Root X1, cn=www.eicar.org, error=Received fatal alert CertificateUnknown from client. CA Issuer URL: http://r3.i.lencr.org/, root_status=trusted, sni=www.eicar.org}, payload.details.dst=89.238.73.97, payload.details.device_name=hou-vfw-01, payload.details.root_cn=ISRG Root X1, payload={severity=informational, rule_uuid=8c7b2be2-9ed1-4d29-889d-7f4c44fce857, serial=007051000214256, receive_time=2023/03/23 08:47:08, rule=LAN Outbound, details={app=incomplete, srcuser=, issuer_cn=R3, device_name=hou-vfw-01, dst=89.238.73.97, src=10.0.11.100, action=allow, root_cn=ISRG Root X1, cn=www.eicar.org, error=Received fatal alert CertificateUnknown from client. CA Issuer URL: http://r3.i.lencr.org/, root_status=trusted, sni=www.eicar.org}, sessionid=17791, category=network, type=decryption}, payload.details.sni=www.eicar.org, meta.headers.Content-Type=application/json, payload.details.app=incomplete, payload.category=network, meta.headers.Accept=*/*, meta.headers.Host=10.0.11.101:5000, payload.serial=007051000214256, meta.device_name=hou-vfw-01, payload.rule=LAN Outbound, meta.headers.Content-Length=745, payload.details.src=10.0.11.100, payload.rule_uuid=8c7b2be2-9ed1-4d29-889d-7f4c44fce857, payload.type=decryption, meta.headers={Accept=*/*, Host=10.0.11.101:5000, Content-Length=745, Content-Type=application/json}, payload.details.issuer_cn=R3, payload.sessionid=17791, payload.details.cn=www.eicar.org, meta={headers={Accept=*/*, Host=10.0.11.101:5000, Content-Length=745, Content-Type=application/json}, device_name=hou-vfw-01, endpoint=endpoint, log_type=decryption}, meta.endpoint=endpoint, meta.log_type=decryption, payload.details.error=Received fatal alert CertificateUnknown from client. CA Issuer URL: http://r3.i.lencr.org/}]
2023-03-23 13:47:09,021 - ansible_rulebook.rule_generator - INFO - calling Troubleshoot Decryption Failure
2023-03-23 13:47:09,021 - ansible_rulebook.rule_set_runner - INFO - call_action debug
2023-03-23 13:47:09,021 - ansible_rulebook.rule_set_runner - INFO - substitute_variables [{}] [{'event': {'payload': {'severity': 'informational', 'rule_uuid': '8c7b2be2-9ed1-4d29-889d-7f4c44fce857', 'serial': '007051000214256', 'receive_time': '2023/03/23 08:47:08', 'rule': 'LAN Outbound', 'details': {'app': 'incomplete', 'srcuser': '', 'issuer_cn': 'R3', 'device_name': 'hou-vfw-01', 'dst': '89.238.73.97', 'src': '10.0.11.100', 'action': 'allow', 'root_cn': 'ISRG Root X1', 'cn': 'www.eicar.org', 'error': 'Received fatal alert CertificateUnknown from client. CA Issuer URL: http://r3.i.lencr.org/', 'root_status': 'trusted', 'sni': 'www.eicar.org'}, 'sessionid': '17791', 'category': 'network', 'type': 'decryption'}, 'meta': {'headers': {'Accept': '*/*', 'Host': '10.0.11.101:5000', 'Content-Length': '745', 'Content-Type': 'application/json'}, 'device_name': 'hou-vfw-01', 'endpoint': 'endpoint', 'log_type': 'decryption'}}}]
2023-03-23 13:47:09,022 - ansible_rulebook.rule_set_runner - INFO - action args: {}
===================================================================================================================================================================================================================================================================================
kwargs:
{'hosts': ['localhost'],
 'inventory': 'all:\n'
              '  hosts:\n'
              '    localhost:\n'
              '      ansible_connection: local\n',
 'project_data_file': None,
 'ruleset': 'Receive logs sourced from HTTP Server Profile in PAN-OS',
 'source_rule_name': 'Troubleshoot Decryption Failure',
 'source_ruleset_name': 'Receive logs sourced from HTTP Server Profile in '
                        'PAN-OS',
 'variables': {'event': {'meta': {'device_name': 'hou-vfw-01',
                                  'endpoint': 'endpoint',
                                  'headers': {'Accept': '*/*',
                                              'Content-Length': '745',
                                              'Content-Type': 'application/json',
                                              'Host': '10.0.11.101:5000'},
                                  'log_type': 'decryption'},
                         'payload': {'category': 'network',
                                     'details': {'action': 'allow',
                                                 'app': 'incomplete',
                                                 'cn': 'www.eicar.org',
                                                 'device_name': 'hou-vfw-01',
                                                 'dst': '89.238.73.97',
                                                 'error': 'Received fatal '
                                                          'alert '
                                                          'CertificateUnknown '
                                                          'from client. CA '
                                                          'Issuer URL: '
                                                          'http://r3.i.lencr.org/',
                                                 'issuer_cn': 'R3',
                                                 'root_cn': 'ISRG Root X1',
                                                 'root_status': 'trusted',
                                                 'sni': 'www.eicar.org',
                                                 'src': '10.0.11.100',
                                                 'srcuser': ''},
                                     'receive_time': '2023/03/23 08:47:08',
                                     'rule': 'LAN Outbound',
                                     'rule_uuid': '8c7b2be2-9ed1-4d29-889d-7f4c44fce857',
                                     'serial': '007051000214256',
                                     'sessionid': '17791',
                                     'severity': 'informational',
                                     'type': 'decryption'}}}}
===================================================================================================================================================================================================================================================================================
facts:
[]
===================================================================================================================================================================================================================================================================================
```
