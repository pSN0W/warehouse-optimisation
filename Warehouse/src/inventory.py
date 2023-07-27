from .product import Product
import yaml
from typing import List

class Inventory:
    """Class for keeping the products
    """
    
    def __init__(self,
                config_file_path: str,
                number_of_order: int) -> None:
        """Create an inventory from a list of products

        Args:
            config_file_path (str): path of the file containing the products
        """
        with open(config_file_path,'r') as f:
            self.config_file = yaml.safe_load(f)
        self.number_of_order = number_of_order
        self.product_list: List[Product] = []
        self.build_inventory()
        
    def build_inventory(self):
        for product in self.config_file["products"]:
            self.product_list.append(
                Product(
                    product["number_of_line_for_case"],
                    product["average_num_demanded_per_line_for_case"],
                    product["volume_of_case"],
                    product["number_of_line_for_unit"],
                    product["average_num_demanded_per_line_for_unit"],
                    product["volume_of_unit"]
                )
            )
            
    def get_total_required_volume(self)->int:
        """Total space required for the inventory

        Returns:
            int: total space
        """
        return sum([product.get_total_volume() for product in self.product_list])
    
    def get_total_number_of_order_line(self)->int:
        """Total number of order line

        Returns:
            int: total order line
        """ 
        return sum([product.get_total_order_lines() for product in self.product_list])
    
    def get_total_number_of_product(self)->int:
        """Total number of products in the inventory

        Returns:
            int: total number of product
        """
        return sum([product.get_total_number_of_product() for product in self.product_list])
    
    def get_average_pick_per_order(self)->int:
        """Average pick per order

        Returns:
            int: Averager pick
        """
        return self.get_total_number_of_order_line() / self.number_of_order