import logging
import azure.functions as func
from prices.prices.spiders import run

app = func.FunctionApp()
run.run_process()

@app.timer_trigger(schedule="0 0 14 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=True) 
def get_prices(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')