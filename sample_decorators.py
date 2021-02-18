from datetime import datetime

def benchmark(func=None, *, file_name=None):
    def decorator_func(func):
        def wrapped_func(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = round((end_time - start_time).total_seconds(), 2)

            message = f"benchmark: {func.__name__} duration: {duration}"

            if file_name:
                with open(file_name, 'a') as f:
                    f.write(message + "\n")
            else:
                print(message)

            return result
        return wrapped_func

    if func:
        return decorator_func(func)
    else:
        return decorator_func

def log(func=None, *, file_name=None):
    def decorator_func(func):
        def wrapped_func(*args, **kwargs):
            result = func(*args, **kwargs)

            message = f"running: {func.__name__} args: {args} kwargs: {kwargs}"

            if file_name:
                with open(file_name, 'a') as f:
                    f.write(message + "\n")
            else:
                print(message)

            return result
        return wrapped_func

    if func:
        return decorator_func(func)
    else:
        return decorator_func