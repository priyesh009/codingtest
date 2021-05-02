#import the required libraries
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators import BashOperator
from airflow.operators import PythonOperator

from cn_data_ing import merge_df


#defining the default arguments dictionary
args = {
	'owner': 'airflow',
	'start_date': datetime(2021,01,26,5,0), 
	'retries': 1,
    "retry_delay": timedelta(seconds=10),
}

dag = DAG('cn_data_ingesation', default_args=args, schedule_interval='@daily', catchup=False)	


#task1 is to check file exist in src1
task1 = BashOperator(task_id='json_file_check', bash_command='shasum ~/airflow/cn_files/src1/data*',retires=2, retry_delay = timedelta(seconds=15), dag=dag)

#task2 is to check file exist in src2
task2 = BashOperator(task_id='csv_file_check', bash_command='shasum ~/airflow/cn_files/src2/eng*',retires=2, retry_delay = timedelta(seconds=15), dag=dag)


#task3 is to merge the source files
task3 = PythonOperator(task_id='merge_files', python_callable=merge_df, dag=dag)


[task1 , task2] >> task3
