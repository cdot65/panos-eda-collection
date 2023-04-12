# Ansible EDA source plugin for PAN-OS firewalls :fire:

This project is an implementation of an asynchronous webhook receiver that receives firewall log messages from a Palo Alto Networks PAN-OS device, embedded within an Ansible EDA source plugin. :key:

This project started as a modification of the `alertmanager.py` source plugin from the Ansible EDA. The original source plugin can be found [here](https://github.dev/ansible/event-driven-ansible/blob/main/plugins/event_source/alertmanager.py).

## Table of Contents

- [Project Setup](#project-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Building the container image](#building-the-container-image)
- [Usage](#usage)
  - [PAN-OS HTTP Server Profile](#pan-os-http-server-profile)
  - [Ansible Rulebook](#ansible-rulebook)
  - [Example Output](#example-output)
- [Build Process and Usage](#build-process-and-usage)
  - [Poetry](#poetry)
  - [Docker](#docker)
  - [Invoke Script](#invoke-script)

## Project Setup

### Prerequisites

There are two methods to deploying, either locally with Poetry or through a Docker container. These docs will cover the Docker based installation:

- Python 3.6 or higher :snake:
- Python Poetry :books:
- Docker or Podman (RHEL based machines only) :whale:

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

An Ansible rulebook is a YAML file that outlines a set of rules and actions to be executed when certain conditions are met. The following example demonstrates a simple rulebook that listens for log messages from a PAN-OS firewall and takes action when specific conditions are met:

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

#### Example Output

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
2023-03-23 13:47:08,933 - aiohttp.access - INFO - 10.0.2.100 [23/Mar/2023:13:47:08 +0000] "POST / HTTP/1.1" 200 571 "-" "PAN-OS/10.1.0"
2023-03-23 13:47:08,947 - ansible_rulebook.engine - INFO - Event received: {'meta': {'log_type': 'decryption'}, 'event_data': {'source_ip': '10.0.0.10', 'destination_ip': '10.0.1.20', 'protocol': 'SSL', 'action': 'block', 'reason': 'decryption failure'}}
2023-03-23 13:47:08,952 - ansible_rulebook.rule_set_runner - INFO - [rule:Troubleshoot Decryption Failure] Action 'debug' triggered, event: {'meta': {'log_type': 'decryption'}, 'event_data': {'source_ip': '10.0.0.10', 'destination_ip': '10.0.1.20', 'protocol': 'SSL', 'action': 'block', 'reason': 'decryption failure'}}
2023-03-23 13:47:08,955 - ansible_rulebook.actions.debug - INFO - Troubleshoot Decryption Failure:
  - Event data: {'source_ip': '10.0.0.10', 'destination_ip': '10.0.1.20', 'protocol': 'SSL', 'action': 'block', 'reason': 'decryption failure'}
```

In this example, the Ansible rulebook receives an event from the PAN-OS firewall, with a log_type of "decryption." The event data indicates that there was a decryption failure with a source IP of 10.0.0.10 and a destination IP of 10.0.1.20. The action taken by the rulebook upon receiving this event is to output the event data to the console, as shown in the last line of the output.

This is a simple example of how an Ansible rulebook can be used to process and react to events from external sources, such as a firewall. Rulebooks can be extended with more complex conditions and actions to cover various use cases and requirements.
