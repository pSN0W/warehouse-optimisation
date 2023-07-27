from src.inventory import Inventory
from src.warehouse import Warehouse
from src.warehouse_optimizer import Optimizer

inventory = Inventory(
    config_file_path = './configs/product_config.yaml',
    number_of_order = 400
)

warehouse = Warehouse(
    config_file_path = './configs/warehouse_config.yaml',
    inventory=inventory
)

optimizer = Optimizer(
    warehouse = warehouse
)

optimizer.optimize()