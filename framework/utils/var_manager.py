import re

class VarManager:
    def __init__(self):
        self.variables = {}

    def resolve_var_name(self, var_name):
        match = re.match(r"\$Var\.(\w+)", var_name)
        if match:
            return match.group(1)
        return var_name

    def set_variable(self, var_name, value):
        real_name = self.resolve_var_name(var_name)
        self.variables[real_name] = value

    def get_variable(self, var_name):
        real_name = self.resolve_var_name(var_name)
        return self.variables.get(real_name)
