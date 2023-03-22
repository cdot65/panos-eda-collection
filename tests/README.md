# Tests

The simplest test is to just run the source plugin directly from the interpreter. The [source plugin](../plugins/event_source/logs.py) can be executed locally without the need to run a full ansible-rulebook command.

First step would be to active the `poetry shell`.  This will put you into a python poetry virtualenv.

```bash
▶ poetry shell
Creating virtualenv cdot65-panos-eda-collection-1cp9JgNv-py3.11 in /home/cdot/.cache/pypoetry/virtualenvs
Spawning shell within /home/cdot/.cache/pypoetry/virtualenvs/cdot65-panos-eda-collection-1cp9JgNv-py3.11

(cdot65-panos-eda-collection-py3.11) 
~/home/cdot/cdot65-panos-eda-collection
```

Next, install the dependencies.

```sh
(cdot65-panos-eda-collection-py3.11) 
▶ poetry install
Installing dependencies from lock file

Package operations: 62 installs, 1 update, 0 removals

<----output omitted---->
```

Run the source plugin from within our virtual environment.

```sh
(cdot65-panos-eda-collection-py3.11) 
~/home/cdot/cdot65-panos-eda-collection
▶ poetry run python plugins/event_source/logs.py

2023-03-22 12:53:51,098 - ansible_rulebook.app - INFO - Starting sources
2023-03-22 12:53:51,099 - ansible_rulebook.app - INFO - Starting rules
2023-03-22 12:53:51,099 - ansible_rulebook.engine - INFO - run_ruleset
2023-03-22 12:53:52,367 - ansible_rulebook.engine - INFO - ruleset define: {"name": "Watch for new changelog entries", "hosts": ["localhost"], "sources": [{"EventSource": {"name": "cdot65.panos_eda.logs", "source_name": "cdot65.panos_eda.logs", "source_args": {"host": "0.0.0.0", "port": 5000}, "source_filters": []}}], "rules": [{"Rule": {"name": "New changelog created", "condition": {"AllCondition": [{"IsDefinedExpression": {"Event": "payload"}}]}, "actions": [{"Action": {"action": "debug", "action_args": {}}}], "enabled": true}}]}
2023-03-22 12:53:52,389 - ansible_rulebook.engine - INFO - load source
2023-03-22 12:53:53,365 - ansible_rulebook.engine - INFO - load source filters
2023-03-22 12:53:53,365 - ansible_rulebook.engine - INFO - Calling main in cdot65.panos_eda.logs
2023-03-22 12:53:53,367 - ansible_rulebook.engine - INFO - Waiting for all ruleset tasks to end
2023-03-22 12:53:53,367 - ansible_rulebook.rule_set_runner - INFO - Waiting for actions on events from Watch for new changelog entries
2023-03-22 12:53:53,367 - ansible_rulebook.rule_set_runner - INFO - Waiting for events, ruleset: Watch for new changelog entries
2023-03-22 12:53:53 368 [drools-async-evaluator-thread] INFO org.drools.ansible.rulebook.integration.api.io.RuleExecutorChannel - Async channel connected
<----output omitted---->
```
