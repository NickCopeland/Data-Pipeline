
# Go to DBT website
[DBT website](https://www.getdbt.com/)

# Set up
Create a free tier account and connect to your Redshift database. 
Create a project and locate the models folder. Delete the examples folder in the models folder.


# dbt_project.yml
    # Name your project! Project names should contain only lowercase characters
    # and underscores. A good package name should reflect your organization's
    # name or the intended use of these models
    name: 'reddit_data_pipeline_project'
    version: '1.0.0'
    config-version: 2

    # This setting configures which "profile" dbt uses for this project.
    profile: 'default'

    # These configurations specify where dbt should look for different types of files.
    # The `source-paths` config, for example, states that models in this project can be
    # found in the "models/" directory. You probably won't need to change these!
    model-paths: ["models"]
    analysis-paths: ["analyses"]
    test-paths: ["tests"]
    seed-paths: ["seeds"]
    macro-paths: ["macros"]
    snapshot-paths: ["snapshots"]

    target-path: "target"  # directory which will store compiled SQL files
    clean-targets:         # directories to be removed by `dbt clean`
    - "target"
    - "dbt_packages"


    # Configuring models
    # Full documentation: https://docs.getdbt.com/docs/configuring-models

    # In this example config, we tell dbt to build all models in the example/ directory
    # as tables. These settings can be overridden in the individual model files
    # using the `{{ config(...) }}` macro.
    models:
    reddit_data_pipeline_project:
        materialized: table

# data_engineering_transformed.sql
Create this .sql file in the models folder

    SELECT 
    id
    , title
    , comment_sum
    , score
    , author
    , created_utc
    , url
    , upvote_ratio
    , TIMESTAMP 'epoch' + (trunc(created_utc::numeric,2)::integer) * INTERVAL '1 second' as created_utc_timestamp
    FROM Data_Engineering

# schema.yml
Create this .yml file in the models folder

    version: 2

    models:
    - name: reddit_transform_data
        description: transforms epoch to timestamp
        columns:
        - name: id
            description: id of post
            tests:
            - not_null
        - name: title
            description: title of post
        - name: comment_sum
            description: total number of comments on post
        - name: score
            description: score of post
        - name: author
            description: author of post
        - name: created_epoch
            description: epoch of post creation
        - name: url
            description: url of post on reddit
        - name: upvote_ratio
            description: post ratio of upvotes to downvotes
        - name: created_utc_timestamp
            description: Timestamp of post creation

# Type this command in dbt
    dbt run