class WarehouseStorage:
    def __init__(self):
        self._warehouses = {}
        self._next_id = 1

    def create(self, name, capacity, initial_balance=0):
        warehouse_id = self._next_id
        self._next_id += 1
        self._warehouses[warehouse_id] = {
            "id": warehouse_id,
            "name": name,
            "capacity": capacity,
            "balance": min(initial_balance, capacity)
        }
        return warehouse_id

    def get(self, warehouse_id):
        return self._warehouses.get(warehouse_id)

    def get_all(self):
        return list(self._warehouses.values())

    def update(self, warehouse_id, name=None, capacity=None):
        warehouse = self._warehouses.get(warehouse_id)
        if not warehouse:
            return False
        if name is not None:
            warehouse["name"] = name
        if capacity is not None:
            warehouse["capacity"] = capacity
            if warehouse["balance"] > capacity:
                warehouse["balance"] = capacity
        return True

    def add_items(self, warehouse_id, amount):
        warehouse = self._warehouses.get(warehouse_id)
        if not warehouse:
            return False, "Warehouse not found"
        if amount <= 0:
            return False, "Amount must be positive"
        available = warehouse["capacity"] - warehouse["balance"]
        if amount > available:
            return False, f"Not enough space. Available: {available}"
        warehouse["balance"] += amount
        return True, None

    def remove_items(self, warehouse_id, amount):
        warehouse = self._warehouses.get(warehouse_id)
        if not warehouse:
            return False, "Warehouse not found"
        if amount <= 0:
            return False, "Amount must be positive"
        if amount > warehouse["balance"]:
            return False, f"Not enough items. Available: {warehouse['balance']}"
        warehouse["balance"] -= amount
        return True, None

    def delete(self, warehouse_id):
        if warehouse_id in self._warehouses:
            del self._warehouses[warehouse_id]
            return True
        return False

    def clear(self):
        self._warehouses = {}
        self._next_id = 1


warehouse_storage = WarehouseStorage()
