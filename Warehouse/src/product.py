class Product:
    def __init__(
        self,
        number_of_line_for_case=0,
        average_num_demanded_per_line_for_case=0,
        volume_of_case=0,
        number_of_line_for_unit=0,
        average_num_demanded_per_line_for_unit=0,
        volume_of_unit=0,
        ) -> None:
        """Constructor for product

        Args:
            number_of_line_for_case (int, optional): Number of order line for case. Defaults to 0.
            average_num_demanded_per_line_for_case (int, optional): Average demand for each case. Defaults to 0.
            volume_of_case (int, optional): Volume of each case. Defaults to 0.
            number_of_line_for_unit (int, optional): Number of order line for unit of product. Defaults to 0.
            average_num_demanded_per_line_for_unit (int, optional): Average demand for each unit. Defaults to 0.
            volume_of_unit (int, optional): Volume of each unit. Defaults to 0.
        """
        self.number_of_line_for_case = number_of_line_for_case
        self.average_num_demanded_per_line_for_case = average_num_demanded_per_line_for_case
        self.volume_of_case = volume_of_case
        self.number_of_line_for_unit = number_of_line_for_unit
        self.average_num_demanded_per_line_for_unit = average_num_demanded_per_line_for_unit
        self.volume_of_unit = volume_of_unit
        
    def get_total_volume(self) -> int:
        """Total required volume for this product

        Returns:
            int: Total Volume
        """
        volume_for_case =  self.number_of_line_for_case*self.average_num_demanded_per_line_for_case*self.volume_of_case 
        volume_for_unit = self.number_of_line_for_unit*self.average_num_demanded_per_line_for_unit*self.volume_of_unit
        return volume_for_case + volume_for_unit
    
    def get_total_order_lines(self)->int:
        """Total number of order lines considering cases and units

        Returns:
            int: Total order line
        """
        return self.number_of_line_for_case+self.number_of_line_for_unit
    
    def get_total_number_of_product(self)->int:
        """Total number of product in demand including case and units

        Returns:
            int: Total number of product
        """ 
        num_of_case = self.number_of_line_for_case*self.average_num_demanded_per_line_for_case
        num_of_unit = self.number_of_line_for_unit*self.average_num_demanded_per_line_for_unit
        return num_of_case + num_of_unit