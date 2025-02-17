# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yquPvMYp6VKhia4Kvcm3TMRZyZ_v9Hnz
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB2'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB2'], args)

# Load the source data
datasource = glueContext.create_dynamic_frame.from_catalog(database="ecommerce_db", table_name="raw_transactions", transformation_ctx="datasource")

# Perform transformations
applymapping = ApplyMapping.apply(frame=datasource, mappings=[
    ("invoice_no", "string", "invoice_no", "string"),
    ("stock_code", "string", "stock_code", "string"),
    ("description", "string", "description", "string"),
    ("quantity", "int", "quantity", "int"),
    ("invoice_date", "string", "invoice_date", "string"),
    ("unit_price", "double", "unit_price", "double"),
    ("customer_id", "string", "customer_id", "string"),
    ("country", "string", "country", "string")
], transformation_ctx="applymapping")

# Save the processed data to S3
datasink = glueContext.write_dynamic_frame.from_options(frame=applymapping, connection_type="s3", connection_options={"path": "s3://ecommerce-data-platform/processed/transactions/"}, format="json", transformation_ctx="datasink")
job.commit()