#!/usr/bin/env python3
import os

import aws_cdk as cdk

from project.EC2Stack import EC2Stack


app = cdk.App()
EC2Stack(app, "ProjectStack")

app.synth()
