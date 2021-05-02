#  Data Engineer: Coding Exercise Solution
In this readme file, I have shared my coding exercise experience, setup instructions, and thoughts.

## Excerise files location
Inside airflow directory.
- **Airflow Dag:**  airflow/dags/cn_dag.py
- **Merge logic python file:**  airflow/dags/cn_data_ing.py
- **Final Merged CSV file:** airflow/cn_files/processed/final_2021-05-02.csv 
- **Source files:** airflow/cn_files/src*

## Quick Airflow Setup Steps
- Setup and start t2.large AWS EC2 instance.
- Login to the instance via putty and Install python, airflow, pandas, etc
- Modify airflow.cfg file if required 
- Create directories for source files and processed files and copy the source files.
- Create airflow dag (cn_dag.py) and python callable (cn_data_ing.py)and put it in dags directory.
- Instantiate airflow DB, run airflow scheduler and the airflow webserver command in putty.

## Coding exercise experience

The coding exercise was fun and challenging. It was challenging mainly because of the limited amount of recommended time to spend on this exercise. 

- First, I started to work on the logic to merge to source files in my local using pandas, python, and Pycharm IDE and created **cn_data_ing.py**. 
- I used pandas as I believe it can process large files efficiently.
- **Processing JSON:** While working on processing JSON files I noticed src1 JSON files were invalid JSON files. so I found a workaround using readlines method and read them as files and iterated over each row and processed the data.  
- I also used the String IO module to get rid of "ValueError: Protocol not known" error in one of the source JSON file
- **Processing CSV:** processing csv was straightforward. 
- I build the logic in such a way that it will process all existing files in the source folder.
- Luckily I already had an EC2 instance in my AWS account with airflow set up so I made use of the same for this exercise(which saved my time in setup) and added cn_data_ing.py in the **airflow/dags** folder.
- **Airflow Dag:** Then I started working on the airflow dag **airflow/cn_dag.py**  Here I have created 3 tasks. task1 and task2 are the checks if the source files exist using BashOperator and task3 uses PythonOperator to execute the python callable.
- schedule interval is set to daily and the start date for all tasks is 26th Jan 2021 in such a way that the task starts only after we receive files in both sources.
- Then I created multiple folders under **airflow/cn_files/** to store source and processed files. 
- At the end dag was successfully executed and the final result is stored in **airflow/cn_files/processed/final_{Date on which file was processed}.csv**

## Improment areas/thoughts

If I had more time and resources then I would have done the following things to improve the code and try to make it production-ready and scalable.

- The source files could be moved to another folder after processing in parquet format to save space.
- Celery executor can be used in airflow.cfg to handle large workflows with ability to scale infinitely. 
- Postgres or MySql for Airflow Metadata DB.
- As per my understanding schdule_interval applies at Dag level so, I would have created 3 Dags. one to process JSON files and moved processed file in some archive folder in parquet format with appropriate schedule interval, similarly for CSV files and 3rd Dags to merge files which will have a dependency on first two Dags.
- Logic to process only CSV and JSON files and ignore other files from the source folder,  some data quality checks, more focus on data cleansing.
- Error handling, logging module, testing scripts and would have used Xcom, Sub-dags, etc if it makes sense. 
- I would have done more reserch on airflow and optimised the code.
