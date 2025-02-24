# Simple tracker for perf analysis for Odoo

## Example of use with click-odoo

```python
#!/usr/bin/env python3

import click
import click_odoo
from odoo import models
from odoo_tracker import tracker, profile_call

models.Model.search = tracker(models.Model.search)

@click.command()
@click_odoo.env_options(default_log_level="info")
def main(env):
    patterned = env["pattern.file"].browse(163)
    profile_call(
        # name of the directory where the analysis will be generated
        "result",
        # name of the file generated
        "pattern",
        # method that should be called
        env["pattern.config"].browse(16)._generate_import_with_pattern_job,
        # params for the method, you can pass args and kwargs
        patterned
    )
    env.cr.rollback()

if __name__ == '__main__':
    main()
```
