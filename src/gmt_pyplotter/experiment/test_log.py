from datetime import datetime, timedelta
import os


def app_usage_log(*args):
    log_path = os.path.join(os.path.dirname(__file__), "app_usage.log")
    with open(log_path, "r") as original:
        temp = original.read()
        print(temp)
    with open(log_path, "w") as new:

        new.write(
            f"""{datetime.now()}
	File name  = {args[0]}.png
	Location   = {args[1]}
 	Coordinate = {args[2]}
	Layers     = {args[3]}
{temp}"""
        )


def system_check(args):
    log_path = os.path.join(os.path.dirname(__file__), "app_usage.log")
    try:
        with open(log_path, "r") as file:
            file.seek(0)
            last_time = file.readline().strip()
            print(last_time)
            if last_time:

                date_time_obj = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S.%f")
                if datetime.now() < date_time_obj + timedelta(days=1):
                    args
                else:
                    pass
    except:
        FileNotFoundError(args)


# app_usage_log(
#     "aasdfasdf",
#     [1, 2, 3, 4],
#     ["abc/bin/basdf"],
#     ["coast"],
# )

system_check()
