import re


class ModelClass(type):
    def __new__(cls, name, bases, dct):
        final = super().__new__(cls, name, bases, dct)

        defaults = {
            key: value
            for key, value in final.__dict__.items()
            if not key.startswith("_")
        }

        init = final.__create_init(final.__annotations__, defaults)

        if not final.__dict__.get("__tablename__"):
            setattr(final, "__tablename__", final.__snake_case(final.__name__))

        tablename = final.__dict__["__tablename__"]

        setattr(final, "__init__", init)

        for field_name, field_type in final.__annotations__.items():
            (func_name, func) = final.__create_get_by(tablename, field_name, field_type)
            setattr(final, func_name, func)

        return final

    @staticmethod
    def __create_init(annotations, defaults, *, return_type=None):
        name = "__init__"
        args = ["self"]
        default_args = []
        body_lines = []
        for key, value in annotations.items():
            if key in defaults.keys():
                default_args.append(f"{key}:{value.__name__}={repr(defaults[key])}")
            else:
                args.append(f"{key}:{value.__name__}")

            body_lines.append(f"self.{key} = {key}")

        args = ", ".join(args + default_args)
        body = "\n ".join(body_lines)

        text = f"def {name}({args})->{return_type}:\n {body}"
        exec(text)
        return locals()[name]

    @staticmethod
    def __create_get_by(tablename, field_name, field_type):
        base_query = f"select * from {tablename} where {field_name} = "
        body = None

        name = f"get_by_{field_name}"

        if field_type == str:
            body = f' value = value.replace("\'", "\'\'")\n return f"{base_query}\'{{value}}\'"'
        elif field_type == bool:
            body = f" value = 'true' if value else 'false'\n return f\"{base_query}{{value}}\""
        else:
            body = f' return f"{base_query}{{value}}"'

        text = f"def {name}(value): \n{body}"

        exec(text)
        return (name, locals()[name])

    @staticmethod
    def __snake_case(value):
        return re.sub("([A-Z])", r"_\1", value).lower().strip("_")
