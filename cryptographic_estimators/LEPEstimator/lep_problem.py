from ..base_problem import BaseProblem


class LEPProblem(BaseProblem):
    """
    Construct an instance of Linear Code Equivalence Problem
    
    INPUT:
    
    - ``n`` -- TODO
    """
    def __init__(self, **kwargs): # Fill with parameters
    	super().__init__(**kwargs)
    
    def to_bitcomplexity_time(self, basic_operations: float):
    	pass
    
    def to_bitcomplexity_memory(self, basic_operations: float):
        pass

    def expected_number_solutions(self):
        pass
    
    def __repr__(self):
        pass
    
    def get_parameters(self):
        pass

