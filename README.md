Example Project Loading different yml files dynamically and paramertizing variables



Using this project:

Run:

```
snow snowpark build
```

You will get an output like: `Build done. Artifact path: /Users/tkmal/Documents/dg_parameters_sample/app.zip`

Then run

```
snow snowpark deploy --connection mobilize --replace
```

This will display:

```
+----------------------------------------------------------------------------------+
| object                                                     | type      | status  |
|------------------------------------------------------------+-----------+---------|
| MLOPS. PUBLIC. run_commands(yam_file_path string)          | procedure | created |
| MLOPS. PUBLIC. run_training(yam_file_path string)          | procedure | created |
+----------------------------------------------------------------------------------+

```

And to run it use:

```
snow snowpark execute procedure "run_training('dsa_parameters.yml')" --connection mobilize
```
Result:

```
+----------------------------------------------------------------------------------------------------------+
| key              | value                                                                                 |
|------------------+---------------------------------------------------------------------------------------|
| RUN_TRAINING     | Done                                                                                  |
|                  | Attempting to fetch parameters from: dsa_parameters.yml                               | 
|                  | Successfully fetched parameters: {'churn_days': {'training': 60, 'inference': 0}}     |
|                  | Churn days for training: 60                                                           |
|                  | Churn days for inference: 0                                                           |
|                  | Training model with churn_days = 60                                                   |
+----------------------------------------------------------------------------------------------------------+

```

To run the yaml sql code you can execute like this: 

```
snow snowpark execute procedure "run_commands('sample1.yml')" --connection mobilize
```
```
snow snowpark execute procedure "run_commands('sample2.yml')" --connection mobilize
```
