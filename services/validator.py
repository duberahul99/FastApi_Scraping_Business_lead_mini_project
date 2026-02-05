class Validator:
    def validate(self, c):
        if not c.get("name"):
            return False
        if not c.get("address") and not c.get("phone"):
            return False
        return True
