from .warehouse import Warehouse
from tqdm import tqdm
import numpy as np
import pandas as pd
import itertools
import time

class Optimizer:
    """Optimizer to get the optimium values for the given warehouse
    """
    
    def __init__(
        self,
        warehouse: Warehouse,
        max_lane_depth: int = 5,
        max_rake_level: int = 20,
        min_aspect_ratio: float = 0.1,
        max_aspect_ratio: float = 2.0
        ) -> None:
        """Constructor for optimizing the warehouse

        Args:
            warehouse (Warehouse): The warehouse to perform optimisation on
            max_lane_depth (int, optional): max number of pallets allowed. Defaults to 5.
            max_rake_level (int, optional): max number of level in rake. Defaults to 20.
            min_aspect_ratio (float, optional): minimum aspect ratio. Defaults to 0.2.
            max_aspect_ratio (float, optional): maximum aspect ratio. Defaults to 1.0.
        """
        self.warehouse: Warehouse = warehouse
        self.max_lane_depth: int = max_lane_depth
        self.max_rake_level: int = max_rake_level
        self.min_aspect_ratio: float = min_aspect_ratio
        self.max_aspect_ratio: float = max_aspect_ratio
        
        self.min_cost = 1e18
        self.lane_depth = -1
        self.rake_level = -1
        self.aspect_ratio = -1
        
    def optimize(self) -> None:
        """Function to optimize the warehouse layout
        """
        possible_lane_depth = list(range(1,self.max_lane_depth+1))
        possible_rake_level = list(range(1,self.max_rake_level+1))
        possible_aspect_ratio = list(np.arange(self.min_aspect_ratio,self.max_aspect_ratio,0.1))
        data = []
        
        for num,(lane_depth,rake_level,aspect_ratio) in tqdm(enumerate(itertools.product(possible_lane_depth,possible_rake_level,possible_aspect_ratio))):
            self.warehouse.initialise_hyperparameter(lane_depth,rake_level,aspect_ratio)
            curr_cost = self.warehouse.compute_total_cost()
            parameters = self.warehouse.get_warehouse_params()
            parameters["export const COST = "] = curr_cost
            if num%50==0:
                self.change_js_file(parameters)
            #     time.sleep(5)
            if curr_cost < self.min_cost:
                self.min_cost = curr_cost
                self.lane_depth = lane_depth
                self.rake_level = rake_level
                self.aspect_ratio = aspect_ratio
            data.append([lane_depth,rake_level,aspect_ratio,curr_cost])
        df = pd.DataFrame(data,columns=['lane_depth','rack_level','aspect_ratio','cost'])
        print(f"Minumum cost {self.min_cost} | Parameters :- lane depth : {self.lane_depth} rack level : {self.rake_level} aspect ratio : {round(self.aspect_ratio,2)}")
        df.to_csv('./cost_data.csv',index=False)
        
        # get the most optimal warehouse
        self.warehouse.initialise_hyperparameter(self.lane_depth, self.rake_level, self.aspect_ratio)
        parameters = self.warehouse.get_warehouse_params()
        parameters["export const COST = "] = self.min_cost
        self.change_js_file(parameters)
        self.warehouse.print_all_params()
        
    def change_js_file(self,data):
        string_data = "\n".join([f"{k}{v}" for k,v in data.items()])
        with open("/home/sn0w/Desktop/IIITA/Sem6/mini/C3/warehouse-layout/public/input.js","w") as f:
            f.write(string_data)