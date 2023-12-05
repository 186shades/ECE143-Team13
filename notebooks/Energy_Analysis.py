
import pandas as pd


class EnergySupplyAnalysisCSV:
    '''
    The class for energy supply analysis for given capacity and GHI data

    Parameter
    ---------
    capacity: int
        Utility-scale solar power capacity
        unit: Mega Watts
    
    solarDataFile: str
        Solar data file path
    '''
    def __init__(self, capacity=17500, solarDataFile: str='../raw_data/midCalifornia_GHI.csv') -> None:
        assert isinstance(capacity, float) or isinstance(capacity, int)
        assert isinstance(solarDataFile, str)

        self.solarData = pd.read_csv(solarDataFile)
        self.capacity = capacity
        self.__energySupply()

    def __energySupply(self) -> pd.DataFrame:
        '''
        Calculate the supply with given solar and solar panel capacity data

        Returns
        -------
        pandas.DataFrame
            | Year | Month | Day | Hour | Minute | GHI | Supply |
            |------|-------|-----|------|--------|-----|--------|
        
            Year: int
            Month: int
            Day: int
            Hour: int
            Minute: int
            GHI: int
            Supply: float
        '''
        self.__supplyDF = self.solarData
        self.__supplyDF['Supply'] = self.__supplyDF['GHI'] * self.capacity / 1000
    
    def getEnergySupply(self) -> pd.DataFrame:
        return self.__supplyDF
    


class EnergyDemandAnalysis:
    '''
    The class for energy demand analysis for given electrical data

    Parameter
    ---------
    energyDataFile: str
        Electrical demand data file path
    '''
    def __init__(self, energyDataFile: str='../raw_data/CAISOactualLoad.csv') -> None:
        assert isinstance(energyDataFile, str)

        self.demandData = pd.read_csv(energyDataFile)
        self.__energyDemand()

    def __energyDemand(self) -> pd.DataFrame:
        '''
        Calculate the demand with electrical data

        Returns
        -------
        pandas.DataFrame
            | Date | Demand |
            |------|--------|
        
            Date: datetime
            Demand: float
        '''

        data = self.demandData[self.demandData['zone'] == 'CA ISO']
        data['date'] = pd.to_datetime(data['Date'])
        self.__demandDF = data[['date', 'load']]
        self.__demandDF = self.__demandDF.rename(columns={"date": "Date", "load": "Demand"})
    
    def getEnergyDemand(self) -> pd.DataFrame:
        return self.__demandDF


#Energy storage analysis:
class StorageAnalysis:
    """
        This class takes in a pandas dataframe in the form of 
            | date | hour | supply |
            |------|------|--------|
            and
            | date | hour | demand |
            |------|------|--------|

            and creates a dataframe in the form of:
            Dataframe: | Year | Month | Day | Hour | Total Demand | Solar Supply | storage demand | storage supplied | storage Left | Curtailed supply | Total Supplied |
                       |------|-------|-----|------|--------------|--------------|----------------|------------------|--------------|------------------|----------------|

            
            Total Demand: Total demand of grid at given hour

            Solar Supply: Total supply of solar energy at given hour

            Storage Demand: Supply - Demand. a positive number indicates the needed power beyond solar supply to meet demand
                            a negative number represents excess supply that ideally would be sent to storage.

            Storage Supplied: Actual power supplied by storage. Only differs from Storage Demand when the battery
                            empties or gets full.

            Storage Left: The current MWh stored in the grid storage

            Curtailed supply: Excess generation that was not able to be stored in the battery. Always positive or zero.
                                only positive when storage is full

            Total Supplied: Total amount of energy supplied to the grid through solar and storage, only differs from total demand when demand cannot 
                                be met by solar and storage.

                                
            By running an hourly simulation of an all-solar plus storage enery grid.
            
    """
    def __init__(self, the_supply: pd.DataFrame, the_demand: pd.DataFrame, the_storageMWh: int):
        """
        Takes in dataframes for supply and demand in the format:
        | Year | Month | Day | Hour | Minute | ... | Supply | ... |
        |------|-------|-----|------|--------|-----|--------|-----|
        and 
        | Year | Month | Day | Hour | Minute | ... | Demand | ... |
        |------|-------|-----|------|--------|-----|--------|-----|
        both in MW and initilizes 

        self.sized_demand: pd.Series[int]
        self.supply: pd.Series[int]
        self.storage_left: pd.Series[int]
        self.storage_demand: pd.Series[int]
        self.storage_supplied: pd.Series[int]
        self.curtailed_supply: pd.Series[int]
        self.total_supplied = pd.Series[int]

        Args:
            the_supply (pd.DataFrame): Input pandas Dataframe that includes supply data and date information
            the_demand (pd.DataFrame): Input pandas dataframe that includes overlapping dates with supply and contains demand data
            the_storageMWh (int): Energy storage amount in simulated grid
        """
        self.supplyDF = the_supply
        self.demandDF = the_demand
        self.storage_max = the_storageMWh

        self.supply: pd.Series[int] = self.supplyDF["Supply"]
        self.demand: pd.Series[int] = self.demandDF["Demand"] 
        self.sized_demand: pd.Series[int]
        self.storage_left: pd.Series[int]
        self.storage_demand: pd.Series[int]
        self.storage_supplied: pd.Series[int]
        self.curtailed_supply: pd.Series[int]
        self.total_supplied: pd.Series[int]
        self.supply_defecit: pd.Series[int]

        self.__set_storage_series()
        

    def __set_storage_series(self):
        """
        This internal method sets all of the pandas series objects with all of the data necessary for analysis
        """
        sized_demand_list: list[int] = [self.demand.iat[0]]
        storage_demand_list: list[int] = [self.demand.iat[0] - self.supply.iat[0]]
        storage_supplied_list: list[int] = [min(self.storage_max, self.demand.iat[0] - self.supply.iat[0])]
        storage_left_list: list[int] = [self.storage_max - storage_supplied_list[0]]
        curtailed_supply_list: list[int] = [max(0, storage_supplied_list[0] - storage_demand_list[0])]
        total_supplied_list: list[int] = [storage_supplied_list[0] + self.supply.iat[0]]

        #Try doing this with something faster than for loop
        for i in range(1,len(self.supply)):
            net_storage_Demand: int = self.demand.iat[i] - self.supply.iat[i]

            #Setting sized demand:
            sized_demand_list.append(self.demand.iat[i])

            #getting storage demand, negative implies oversupply:
            storage_demand_list.append(net_storage_Demand)

            #getting storage left
            storage: int = storage_left_list[i-1] - net_storage_Demand
            if storage < 0:
                storage = 0
            elif storage > self.storage_max:
                storage = self.storage_max
            storage_left_list.append(storage)

            #getting storage supplied:
            if net_storage_Demand > 0:
                storage_supplied_list.append(min(storage_left_list[i-1], net_storage_Demand))
            else:
                storage_supplied_list.append(max(storage_left_list[i-1] - self.storage_max, net_storage_Demand))

            #getting curtailed supply:
            curtailed_supply_list.append(max(0, storage_supplied_list[i] - storage_demand_list[i]))

            #Getting total supplied:
            total_supplied_list.append(self.supply.iat[i] - curtailed_supply_list[i] + storage_supplied_list[i])

            

        self.sized_demand = pd.Series(sized_demand_list)
        self.storage_left = pd.Series(storage_left_list)
        self.storage_demand = pd.Series(storage_demand_list)
        self.storage_supplied = pd.Series(storage_supplied_list)
        self.curtailed_supply = pd.Series(curtailed_supply_list)
        self.total_supplied = pd.Series(total_supplied_list)
        
    def get_storage_data(self):
        """
        Returns:
            Dataframe: | Year | Month | Day | Hour | Total Demand | Solar Supply | storage demand | storage supplied | storage Left | Curtailed supply | Total Supplied |
                       |------|-------|-----|------|--------------|--------------|----------------|------------------|--------------|------------------|----------------|

            
            Total Demand: Total demand of grid at given hour

            Solar Supply: Total supply of solar energy at given hour

            Storage Demand: Supply - Demand. a positive number indicates the needed power beyond solar supply to meet demand
                            a negative number represents excess supply that ideally would be sent to storage.

            Storage Supplied: Actual power supplied by storage. Only differs from Storage Demand when the battery
                            empties or gets full.

            Storage Left: The current MWh stored in the grid storage

            Curtailed supply: Excess generation that was not able to be stored in the battery. Always positive or zero.
                                only positive when storage is full

            Total Supplied: Total amount of energy supplied to the grid through solar and storage, only differs from total demand when demand cannot 
                                be met by solar and storage.
        """
        return_dict = {"Total Demand" : self.sized_demand,
                       "Solar Supply" : self.supply,
                       "Storage Demand" : self.storage_demand,
                       "Storage Supplied" : self.storage_supplied,
                       "Storage Left" : self.storage_left,
                       "Curtailed Supply" : self.curtailed_supply,
                       "Total Supplied" : self.total_supplied
                       }
        
        return_dates = self.supplyDF[["Year","Month","Day","Hour"]]
        
        return pd.concat([return_dates, pd.DataFrame(return_dict)], axis=1)
        # print(self.storage_left)
        # print(self.storage_demand)
        # print(self.storage_supplied)
        # print(self.curtailed_supply)
    
    

#https://assessingsolar.org/notebooks/solar_power_modeling.html