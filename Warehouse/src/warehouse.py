from .inventory import Inventory
from tabulate import tabulate
import yaml
import math

class Warehouse:
    """Warehouse 
    """
    
    def __init__(
        self,
        config_file_path: str,
        inventory:Inventory) -> None:
        """Constructor for the warehouse

        Args:
            config_file_path (str): file with configurations for warehouse
            inventory (Inventory): Inventory to be stored in the warehouse
        """
        self.inventory = inventory
        
        with open(config_file_path,'r') as f:
            warehouse_config = yaml.safe_load(f)
            
            self.height_of_rack_level = warehouse_config["height_of_rack_level"]
            self.clearance_percentage = warehouse_config["clearance_percentage"]
            self.clearance_allowance = self.clearance_percentage / 100
            self.depth_of_pallet = warehouse_config["depth_of_pallet"]
            self.aisle_width = warehouse_config["aisle_width"]
            self.horizantal_velocity_of_picker = warehouse_config["horizantal_velocity_of_picker"]
            self.vertical_velocity_of_picker = warehouse_config["vertical_velocity_of_picker"]
            self.cost_of_labor_per_hr = warehouse_config["cost_of_labor_per_hr"]
            self.extraction_constant = warehouse_config["extraction_constant"]
            self.rent_per_unit_area = warehouse_config["rent_per_unit_area"]
            
    def initialise_hyperparameter(
        self,
        lane_depth: int,
        num_of_rack_level: int,
        aspect_ratio: int
        ) -> None:
        """Initialise the parameters for the optimisation problem

        Args:dic = yaml.safe_dump(fin_dic,f)
            lane_depth (int): Number of pallets of a rack
            num_of_rack_level (int): number of levels in the rack (vertical)
            aspect_ration (int): ratio of width to the depth of the warehouse
        """
        self.lane_depth = lane_depth
        self.num_of_rack_level = num_of_rack_level
        self.aspect_ratio = aspect_ratio
        self.compute_related_params()
        
    def compute_related_params(self) -> None:
        """Computes other related parameters for the optimisation problem
        """
        self.num_racks_with_warehouse_depth = self.compute_num_racks_with_warehouse_depth()
        self.area = self.compute_area()
        self.x = (self.area / self.aspect_ratio)**(1/2) # warehouse length
        self.y = (self.area * self.aspect_ratio)**(1/2) # warehouse depth
        self.num_of_racks = self.num_racks_with_warehouse_depth // self.y
        
    def get_warehouse_params(self) -> dict:
        """Get the warehouse parameters

        Returns:
            dict: Dictionary with warehouse parameters
        """
        data = {
            "export const WIDTH_OF_RACK = " : self.lane_depth,
            "export const HEIGHT_OF_RACK = " : self.num_of_rack_level,
            "export const NUMBER_OF_RACK = " : self.num_of_racks,
            "export const WAREHOUSE_LENGTH = " : self.x,
            "export const WAREHOUSE_DEPTH = " : self.y
        }
        data = {k:min([100,v]) for k,v in data.items()}
        return data
        
    def print_all_params(self):
        """Prints all the hyperparemeter for the model
        """
        data = [
            [1,"width of warehouse",round(self.x,2)],
            [2,"depth of warehouse",round(self.y,2)],
            [3,"number of racks", round(self.num_of_racks,2)],
            [4,"number of level on rack", round(self.num_of_rack_level,2)],
            [5,"lane depth", round(self.lane_depth,2)],
        ]
        print(tabulate(data,headers=["Si. No.","Parameter","Value"]))
        
    def compute_total_cost(self)->int:
        """Total cost in the current setting

        Returns:
            int: total cost
        """
        return self.compute_area_cost() + \
            self.compute_extraction_cost() + \
                self.compute_horizantal_cost() + \
                    self.compute_vertical_travel_cost()
        
    def compute_num_racks_with_warehouse_depth(self) -> int:
        """Computes num_of_racks * depth of the warehouse

        Returns:
            int: num_racks * depth of warehouse
        """
        required_volume = self.inventory.get_total_required_volume()
        """
        volume_of_warehouse >= required_volume
        Since considering minimising cost
        volume_of_warehouse = required_volume
        volume_of_warehouse = 
            (2*lane_depth*depth_of_pallet) * numb_of_rack_level * (1 - clearance_allowance) * num_racks * depth
        num_racks * depth = required_volume / ((2*lane_depth*depth_of_pallet) * num_of_rack_level * (1 - clearance_allowance))
        """
        denom = (2 * self.lane_depth * self.depth_of_pallet) * self.num_of_rack_level *\
            (1 - self.clearance_allowance)
        return math.ceil( required_volume / denom )
    
    def compute_area(self) -> int:
        """Area of the ware house

        Returns:
            int: area
        """
        one_rake_area = 2*self.lane_depth*self.depth_of_pallet + self.aisle_width
        total_area = one_rake_area * self.num_racks_with_warehouse_depth
        return total_area
        
    def compute_area_cost(self)->int:
        """Computes the cost for area

        Returns:
            int: Total cost for for building a warehouse of the given area
        """
        
        return self.rent_per_unit_area * self.area
    
    def compute_vertical_travel_cost(self)->int:
        """Cost of vertical traveling to get the item

        Returns:
            int: cost
        """
        total_vertical_height = self.num_of_rack_level * self.height_of_rack_level
        time_taken_to_extract_one_unit = total_vertical_height / self.vertical_velocity_of_picker
        cost_of_one_order = self.cost_of_labor_per_hr * time_taken_to_extract_one_unit
        total_cost = cost_of_one_order * self.inventory.get_total_number_of_order_line()
        return total_cost
    
    def compute_extraction_cost(self)->int:
        """Once at the correct location cost of extracting from the rack

        Returns:
            int: cost for extracting an item once at the current location
        """
        max_dist_to_move = self.depth_of_pallet * self.lane_depth
        cost_associated_with_movement_per_unit = max_dist_to_move*self.extraction_constant*self.cost_of_labor_per_hr
        total_cost = cost_associated_with_movement_per_unit * self.inventory.get_total_number_of_product()
        return total_cost
    
    def compute_horizantal_cost(self)->int:
        """Cost of horizantal movement to reach to a specified location according to Hall 1993

        Returns:
            int: horizantal movement cost
        """
        avg_pick_per_order = self.inventory.get_average_pick_per_order()
        avg_x_dist = 2 * self.x * (avg_pick_per_order - 1)/(avg_pick_per_order + 1)
        avg_y_dist = self.y * self.num_of_racks * \
            (1 - ((self.num_of_racks - 1)/self.num_of_racks)**avg_pick_per_order) + 0.5 * self.y
        total_horizantal_distance = avg_x_dist + avg_y_dist
        total_horizantal_cost = (total_horizantal_distance / self.horizantal_velocity_of_picker) * \
            self.inventory.number_of_order * self.cost_of_labor_per_hr
        return total_horizantal_cost
    