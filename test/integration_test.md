## Testing
Before carrying out integration testing, please make sure to perform installation by colcon build and sourcing the workspace.
To test only this package, perform ```colcon build --packages-select localization path_planning lateral_and_longitudinal_control custom_msg ``` and ```source install/setup.bash``` is sufficient, without building other packages.
### Integration Tests
0. Follow this installtion step to clone every repository of paxauto
[Intallation](https://git.hs-coburg.de/pax_auto/pax_auto_main#-installation) : Installation of every componenet.

1. Setup pytest tool:
```bash
pip3 install pytest
```
2. Open separate terminal to run every nodes (make sure to source the workspace). Ctrl + C to kill the node and rerun it for each test case:

3. Run the integration tests for each of the test script and extract the log message, use the following command as an example:
```bash
python3 -m pytest -s -v TC_Int005.py > TC_Int005.log
```
