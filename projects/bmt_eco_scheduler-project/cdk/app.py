# -*- coding: utf-8 -*-

import aws_cdk as cdk
from bmt_eco_scheduler.iac.define import MainStack
from bmt_eco_scheduler.config.api import config

app = cdk.App()

stack = MainStack(
    app,
    config.env.env_name,
    config=config,
    env=config.env,
    stack_name=config.env.cloudformation_stack_name,
)

app.synth()
