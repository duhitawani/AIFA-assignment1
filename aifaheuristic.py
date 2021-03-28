#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8
import copy
# In[4]:



class City:
    def __init__(self):
        self.Evs = {
            'C1' : {
                'source' : 'MB',
                'destination': 'LBS',
                'init_battery' : 4,
                'charging' : 3,
                'discharging' : 5,
                'max' : 200,
                'speed' : 24
            },
            "C2": {
                "source": "LLR",
                "destination": "SNIG",
                "init_battery": 15,
                "charging": 8,
                "discharging": 9,
                "max": 100,
                "speed": 25
            },
            "C3": {
                "source": "PAN",
                "destination": "CCD",
                "init_battery": 6,
                "charging": 2,
                "discharging": 3,
                "max": 160,
                "speed": 30
            },
            "C4": {
                "source": "BCRH",
                "destination": "RP",
                "init_battery": 8,
                "charging": 4,
                "discharging": 6,
                "max": 120,
                "speed": 22
            },
            "C5": {
                "source": "MT",
                "destination": "TSG",
                "init_battery": 10,
                "charging": 1,
                "discharging": 2,
                "max": 150,
                "speed": 26
            }
        }
        
        # KGP MAP
        self.graph = {
            'RP' : {
                'MB' : 4,      # MB stands for Main Building
                'LLR' : 16
            },
            "LLR": {
                "LBS": 8,
                "CCD": 6,
                "TSG": 10,
                "RP" : 16
            },
            "LBS": {
                "LLR": 8,
                "PAN": 4
            },
            "PAN": {
                "LBS": 4,
                "BCRH": 8
            },
            "BCRH": {
                "PAN": 8,
                "TSG": 12,
                "SNIG": 20
            },
            "SNIG": {
                "TSG": 14,
                "BCRH": 20,
                "MT": 10
            },
            "MT": {
                "SNIG": 10,
                "MB": 20
            },
            "MB": {
                "RP": 4,
                "MT": 20,
                "CCD": 10
            },
            "CCD": {
                "MB": 8,
                "LLR": 6,
                "TSG": 12
            },
            "TSG": {
                "LLR": 10,
                "BCRH": 12,
                "SNIG": 14
            }
        }
        self.cars =list( self.Evs.keys())
        self.cities = list(self.graph.keys())
        self.acceptStates = []

    def getDistanceBetween(self, cityA, cityB):
        return self.graph[cityA][cityB]
    
    def adjacentCities(self, city):
        return self.graph[city].keys()

    def initStateSpace(self):
        self.state = [{}] #state[t] is the state at time t
        for car in self.cars:
            car_data = {}
            car_data["location"] = [self.Evs[car]["source"], None, 0] #(City A, City B, distance on E(A,B)))
            # car_data["location_edge"] = None
            # car_data["distance_edge"] = 0
            car_data["is_charging"] = False 
            car_data["path"] = []
            car_data["charge"] = self.Evs[car]["init_battery"]
            car_data["heuristic"] = -1  # Update if using heuristics
            self.state[0][car] = car_data
        # self.state[0]["time"] = 0
    
    def RejectState(self, state):
        charging = []
        for car in state:
            if (state[car]["charge"] < 0):
                return True
            if (state[car]["charge"] == 0 and state[car]["location"][1] is not None):
                return True
            if (len(state[car]["path"]) > len(set(state[car]["path"])) ):   #loop
                return True
            if(state[car]["is_charging"]):
                city = state[car]["location"][0]
                if city in charging:
                    return True
                else:
                    charging.append(city)
            if(state[car]["location"][1] is None):
                avail_cities = [city for city in self.adjacentCities(state[car]["location"][0]) if city not in state[car]["path"]]
                if not avail_cities:
                    return True

        return False

    def AcceptState(self, state):
        if (self.RejectState(state)):
            return False
        for car in state:
            if not(state[car]["location"][1] is None and state[car]["location"][0] == self.Evs[car]["destination"]):
                return False
        return True

    def ev_charge(self, state, car):
        charge = state[car]["charge"] + self.Evs[car]["charging"]
        state[car]["charge"] = min(charge, self.Evs[car]["max"])
        state[car]["is_charging"] = self.Evs[car]["max"] > charge
        
    def ev_move(self, state, car):
        state[car]["location"][2] += self.Evs[car]["speed"]
        state[car]["charge"] -= self.Evs[car]["speed"]/self.Evs[car]["discharging"]
        if state[car]["location"][2] >= self.getDistanceBetween(state[car]["location"][0], state[car]["location"][1]):
            state[car]["location"][0] = state[car]["location"][1]
            state[car]["location"][1] = None
            state[car]["location"][2] = 0

    def recSearchT(self, state, cars_todo):
        if cars_todo: 
            car = cars_todo[0]
            cars_todo.pop(0)
            if (state[car]["location"][0] != self.Evs[car]["destination"]):
                if(state[car]["charge"] > 0):
                    if(state[car]["location"][1] is None):
                        adjCities = self.adjacentCities(state[car]["location"][0])
                        for city in adjCities:
                            if city not in state[car]["path"]:
                                state_move = copy.deepcopy(state)
                                state_move[car]["location"][1] = city
                                state_move[car]["location"][2] = 0
                                state_move[car]["path"].append(city)
                                self.ev_move(state_move, car)
                                self.recSearchT(state_move, cars_todo)
                    else:
                        state_move = copy.deepcopy(state)
                        self.ev_move(state_move, car)
                        self.recSearchT(state_move, cars_todo)

                if(state[car]["location"][1] is None and state[car]["charge"] < self.Evs[car]["max"]):
                    state_charge = copy.deepcopy(state)
                    self.ev_charge(state_charge, car)
                    self.recSearchT(state_charge, cars_todo)

        else:
                return self.recSearch(state)
        


    def recSearch(self, state = None):
        if not state:
            state = self.state[0]
        if self.RejectState(state):
            return False
        if self.AcceptState(state):
            if state not in self.acceptStates:
                self.acceptStates.append(state)
            print("ACCEPT")
            print(state)
            return True
        
        self.recSearchT(state, copy.deepcopy(self.cars))

        

    def diksaktra(self):
        global large
        for car in self.cars:
            Ev = self.Evs[car]
            max_dist = Ev['max']*Ev['discharging']
            
            #starting dijkastra
            distances={}
            parents={}
            iterate=[] 
            for city in self.cities:
                distances[city]=large
                if(city!=Ev["source"]):
                    iterate.append(city)
            distances[Ev["source"]]=0
            parents[Ev["source"]]=None
            
            n_cities = self.adjacentCities(Ev["source"])
            for n_city in n_cities:
                parents[n_city]=Ev["source"]
                distances[n_city]=self.getDistanceBetween(Ev["source"],n_city)
            while (len(iterate)):
                min=large
                mincity=None
                for city in iterate:
                    dist= distances[city]
                    if(dist<min):
                        min=dist
                        mincity=city
                iterate.remove(mincity)
                n_cities=self.adjacentCities(mincity)
                for n_city in n_cities:
                    if (self.getDistanceBetween(mincity, n_city)>min):
                        pass 
                    upd=min+self.getDistanceBetween(mincity,n_city)
                    if (upd < distances[n_city]):
                        distances[n_city]=upd
                        parents[n_city]=mincity
            pathlist = []            
            chain=Ev['destination']
            
            #joining chain with parents
            
            while(chain!= None):
                        pathlist.append(chain)
                        chain = parents[chain]
            pathlist1 = pathlist[::-1]
            print(pathlist1)
            
            #Calculating Time to reach destination
            
            time=0
            time=time+ (distances[Ev['destination']]/Ev['speed']) 
            req_battery= (distances[Ev['destination']]/Ev['discharging']) - Ev['init_battery']
            if(req_battery>0):
                time = time + req_battery/Ev['charging']
            print(time)

large = 1000000
Kgp = City()
Kgp.initStateSpace()
Kgp.recSearch()
print(Kgp.acceptStates)





# In[ ]:





# In[ ]:




