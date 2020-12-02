Simple tracker for perf analyse for odoo
=============================================


Example of use with click-odoo

.. code-block:: python

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
            # name of the directory where the anylyse will be generated
            "result",
            # name of the file generated
            "pattern",
            # method that should be called
            env["pattern.config"].browse(16)._generate_import_with_pattern_job,
            # params for the method, you can pass an args and kwargs
            patterned)
        env.cr.rollback()

    if __name__ == '__main__':
        main()


3 files will be generated in the folder "result"
  - pattern.cprof
  - pattern.csv
  - pattern.xdot

You can read the xdot file with "sudo apt install xdot"

