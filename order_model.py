class Order:
    def __init__(self, student, restaurant):
        self.student = student
        self.restaurant = restaurant
        self.items = []

    def add_item(self, item, quantity):
        self.items.append((item, quantity))

    def calculate_total(self):
        # get the raw total using recursion
        raw_total = self._sum_items(self.items)
        # apply a simple discount rule at the end
        # placeholder rule: 10% off if total is more than GHS 100
        if raw_total > 100:
            return raw_total * 0.9
        else:
            return raw_total

    def _sum_items(self, items):
        # base case: no items left, nothing to add
        if len(items) == 0:
            return 0
        # take the first item off the list
        item, quantity = items[0]
        line_total = item.get_price() * quantity
        # recurse on everything else
        rest_total = self._sum_items(items[1:])
        return line_total + rest_total

    def save_receipt(self, folder="receipts"):
        """Write this order to a .txt receipt file. Returns the file path."""
        import os
        os.makedirs(folder, exist_ok=True)

        student_id = self.student.get_student_id()
        filename = f"{folder}/{student_id}_{self._receipt_timestamp()}.txt"

        with open(filename, "w") as f:
            f.write(f"Student: {self.student.get_name()} ({student_id})\n")
            f.write(f"Restaurant: {self.restaurant.get_name()}\n")
            f.write("Items:\n")
            for item, qty in self.items:
                line_total = item.get_price() * qty
                f.write(f"  {qty} x {item.get_name()} - GHS {line_total:.2f}\n")
            f.write(f"Total: GHS {self.calculate_total():.2f}\n")

        return filename

    def _receipt_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def get_order_history(student_id, folder="receipts"):
        """
        Read back all saved receipts for a given student ID.
        Returns a list of dicts: [{"filename": ..., "content": ...}, ...]
        Ordered oldest to newest (based on filename timestamp).
        """
        import os

        if not os.path.exists(folder):
            return []

        history = []
        for fname in sorted(os.listdir(folder)):
            if fname.startswith(f"{student_id}_") and fname.endswith(".txt"):
                filepath = os.path.join(folder, fname)
                with open(filepath, "r") as f:
                    content = f.read()
                history.append({"filename": fname, "content": content})

        return history
